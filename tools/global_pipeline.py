"""Global MODIS + VIIRS harmonization on a 1-degree grid (run on the Google Cloud VM).

  python3 tools/global_pipeline.py aggregate modis 2003      # download one yearly global zip, count, delete
  python3 tools/global_pipeline.py build                     # harmonize all years -> web/data/global/*.json

Same method as pipeline.py (see docs/METHOD.md): vegetation fires only (type 0), MODIS confidence >= 30,
VIIRS nominal/high; Terra-only gap scaled by (Terra+Aqua)/Terra; back-cast ratio VIIRS/MODIS per cell and
calendar month fitted on 2012-2016, +-1 month smoothing, shrunk toward the 10-degree block ratio (K = 10).
Stdlib only, streams CSVs straight out of the zip so disk use stays small."""
import io, json, math, os, statistics, sys, urllib.request, zipfile
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
WORK = os.path.join(ROOT, "work", "global")
OUT = os.path.join(ROOT, "web", "data", "global")
ZIP = "https://firms.modaps.eosdis.nasa.gov/data/country/zips/{s}_{y}_all_countries.zip"
VIIRS_START, AQUA_START, FIT, K = 2012, "2002-07", (2012, 2016), 10
CV_YEARS = range(2012, 2020)
MM = [f"{i:02d}" for i in range(1, 13)]


def cell_of(lat, lon):
    return (min(179, math.floor(lat) + 90)) * 360 + (math.floor(lon) + 180) % 360


def aggregate(sensor, year):
    """counts[(cell, 'YYYY-MM')] = [n, terra_n] for one sensor-year."""
    os.makedirs(WORK, exist_ok=True)
    out_path = os.path.join(WORK, f"{sensor}_{year}.json")
    if os.path.exists(out_path):
        return
    zpath = os.path.join(WORK, f"{sensor}_{year}.zip")
    urllib.request.urlretrieve(ZIP.format(s=sensor, y=year), zpath)
    viirs = sensor.startswith("viirs")
    counts = defaultdict(lambda: [0, 0])
    rows = 0
    with zipfile.ZipFile(zpath) as z:
        for name in z.namelist():
            if not name.endswith(".csv"):
                continue
            with z.open(name) as raw:
                f = io.TextIOWrapper(raw, encoding="utf-8", errors="replace")
                head = f.readline().strip().split(",")
                i_la, i_lo, i_d, i_c = (head.index(k) for k in ("latitude", "longitude", "acq_date", "confidence"))
                i_t = head.index("type") if "type" in head else None
                i_s = head.index("satellite") if "satellite" in head else None
                for line in f:
                    p = line.split(",")
                    if i_t is not None and p[i_t].strip() not in ("0", ""):
                        continue
                    c = p[i_c].strip().lower()
                    if viirs:
                        if c not in ("n", "h", "nominal", "high"):
                            continue
                    elif not c.isdigit() or int(c) < 30:
                        continue
                    k = (cell_of(float(p[i_la]), float(p[i_lo])), p[i_d][:7])
                    v = counts[k]; v[0] += 1
                    if not viirs and i_s is not None and p[i_s].startswith("T"):
                        v[1] += 1
                    rows += 1
    os.remove(zpath)
    with open(out_path + ".tmp", "w") as f:
        json.dump([[c, ym, n, t] for (c, ym), (n, t) in counts.items()], f, separators=(",", ":"))
    os.replace(out_path + ".tmp", out_path)
    print(sensor, year, rows, "fires", len(counts), "cell-months", flush=True)


def load():
    data = {"M": defaultdict(dict), "V": defaultdict(dict), "T": defaultdict(dict)}
    for fn in sorted(os.listdir(WORK)):
        if not fn.endswith(".json"):
            continue
        key = "V" if fn.startswith("viirs") else "M"
        for c, ym, n, t in json.load(open(os.path.join(WORK, fn))):
            data[key][c][ym] = data[key][c].get(ym, 0) + n
            if key == "M" and t:
                data["T"][c][ym] = data["T"][c].get(ym, 0) + t
    return data


def block(c):          # 10-degree block id
    return (c // 360 // 10, (c % 360) // 10)


def month_tot(series, years):
    tot = defaultdict(lambda: defaultdict(int))
    for c, s in series.items():
        for ym, n in s.items():
            if int(ym[:4]) in years:
                tot[c][ym[5:]] += n
    return tot


def win(d, mm):
    i = MM.index(mm)
    return sum(d.get(MM[(i + k) % 12], 0) for k in (-1, 0, 1))


def fit(data, years, method="cell"):
    years = set(years)
    tm, tv = month_tot(data["M"], years), month_tot(data["V"], years)
    gm = {mm: sum(t.get(mm, 0) for t in tm.values()) for mm in MM}
    gv = {mm: sum(t.get(mm, 0) for t in tv.values()) for mm in MM}
    glob = {mm: win(gv, mm) / max(1, win(gm, mm)) for mm in MM}
    const = sum(gv.values()) / max(1, sum(gm.values()))
    if method == "const":
        return lambda c, mm: const
    bm, bv = defaultdict(lambda: defaultdict(int)), defaultdict(lambda: defaultdict(int))
    for c, t in tm.items():
        for mm, n in t.items(): bm[block(c)][mm] += n
    for c, t in tv.items():
        for mm, n in t.items(): bv[block(c)][mm] += n
    cache = {}
    def bratio(b, mm):
        if (b, mm) not in cache:
            m, v = win(bm.get(b, {}), mm), win(bv.get(b, {}), mm)
            cache[(b, mm)] = (v + K * glob[mm]) / (m + K)
        return cache[(b, mm)]
    def ratio(c, mm):
        m, v = win(tm.get(c, {}), mm), win(tv.get(c, {}), mm)
        return (v + K * bratio(block(c), mm)) / (m + K)
    return ratio


def validate(data):
    res = {}
    for method in ("const", "cell", "raw"):
        P, O, CP, CO = [], [], [], []
        for y in CV_YEARS:
            r = (lambda c, mm: 1.0) if method == "raw" else fit(data, [x for x in CV_YEARS if x != y], method)
            pm, om, cp, co = defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(float)
            for c, s in data["M"].items():
                for ym, n in s.items():
                    if int(ym[:4]) == y:
                        x = n * r(c, ym[5:]); pm[ym] += x; cp[c] += x
            for c, s in data["V"].items():
                for ym, n in s.items():
                    if int(ym[:4]) == y:
                        om[ym] += n; co[c] += n
            ms = sorted(set(pm) | set(om)); cs = sorted(set(cp) | set(co))
            P += [pm[m] for m in ms]; O += [om[m] for m in ms]; CP += [cp[c] for c in cs]; CO += [co[c] for c in cs]
        res[method] = {"mae_monthly_global": round(statistics.mean(abs(a - b) for a, b in zip(P, O))),
                       "bias_pct": round(100 * (sum(P) - sum(O)) / sum(O), 1),
                       "corr_monthly": round(statistics.correlation(P, O), 3),
                       "corr_cell_annual": round(statistics.correlation(CP, CO), 3)}
        print("validation", method, res[method], flush=True)
    return res


def build():
    data = load()
    yrs = set(range(2003, 2012))
    a = {mm: sum(t.get(mm, 0) for t in month_tot(data["M"], yrs).values()) for mm in MM}
    t = {mm: sum(x.get(mm, 0) for x in month_tot(data["T"], yrs).values()) for mm in MM}
    tf = {mm: win(a, mm) / max(1, win(t, mm)) for mm in MM}
    ratio = fit(data, range(FIT[0], FIT[1] + 1))
    val = validate(data)

    h = defaultdict(dict)
    for c, s in data["M"].items():
        for ym, n in s.items():
            if int(ym[:4]) < VIIRS_START:
                h[c][ym] = n * (tf[ym[5:]] if ym < AQUA_START else 1) * ratio(c, ym[5:])
    for c, s in data["V"].items():
        for ym, n in s.items():
            if int(ym[:4]) >= VIIRS_START:
                h[c][ym] = n
    months = sorted({ym for s in h.values() for ym in s if ym >= "2001-01"})
    cells = sorted(h)
    idx = {c: i for i, c in enumerate(cells)}
    frames = []                                   # per month: flat [cellIndex, count, cellIndex, count, ...]
    for ym in months:
        fr = []
        for c in cells:
            v = h[c].get(ym, 0)
            if v >= 0.5:
                fr += [idx[c], round(v)]
        frames.append(fr)
    tot = lambda src, ym: sum(s.get(ym, 0) for s in src.values())
    os.makedirs(OUT, exist_ok=True)
    json.dump({"cell_deg": 1, "cells": cells, "months": months, "frames": frames},
              open(os.path.join(OUT, "frames.json"), "w"), separators=(",", ":"))
    json.dump({"months": months,
               "harmonized": [round(tot(h, m)) for m in months],
               "raw": [round(tot(data["V"] if int(m[:4]) >= VIIRS_START else data["M"], m)) for m in months],
               "terra_only_factor": {k: round(x, 2) for k, x in tf.items()},
               "validation": val, "fit_window": FIT},
              open(os.path.join(OUT, "summary.json"), "w"), separators=(",", ":"))
    print("built", len(cells), "cells", len(months), "months", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "aggregate":
        aggregate(sys.argv[2], int(sys.argv[3]))
    else:
        build()
