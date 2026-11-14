"""MODIS + VIIRS harmonization -> web/data/{cells.json, meta.json, points.csv}
Input: FIRMS archive CSVs in data/raw/ (latitude, longitude, acq_date, confidence, type, instrument, satellite).

Method (see docs/METHOD.md):
 1. Filter: vegetation fires only (type 0); MODIS confidence >= 30, VIIRS nominal/high.
 2. Terra-only gap: before Aqua (Jul 2002) MODIS counts are scaled by (Terra+Aqua)/Terra, fitted 2003-2011.
 3. Back-cast ratio VIIRS/MODIS per 0.25deg cell and calendar month, fitted on the EARLY overlap
    (2012-2016, before the Terra/Aqua orbit drift), smoothed over +-1 month and shrunk toward the
    regional ratio when a cell has few MODIS detections (empirical-Bayes style).
 4. Harmonized series = scaled MODIS before 2012, observed VIIRS S-NPP from 2012.
Validation: leave-one-year-out over 2012-2019 for three ratio models + raw MODIS baseline. Stdlib only."""
import csv, glob, json, math, os, statistics
from collections import defaultdict

CELL = 0.25                 # grid size, degrees
VIIRS_START = 2012          # first full VIIRS S-NPP year
AQUA_START = "2002-07"      # before this month MODIS = Terra only
FIT = (2012, 2016)          # back-cast fit window: early overlap, before MODIS orbit drift
CV_YEARS = range(2012, 2020)    # leave-one-year-out validation years
DRIFT = (2021, 2025)        # years used to show the MODIS drift
K = 10                      # shrinkage strength (pseudo MODIS detections)
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "web", "data")
MM = [f"{i:02d}" for i in range(1, 13)]
dd = lambda: defaultdict(lambda: defaultdict(int))

def keep(viirs, row):
    if row.get("type", "0") not in ("0", ""):          # 0 = presumed vegetation fire
        return False
    c = row["confidence"].strip().lower()
    return c in ("n", "h", "nominal", "high") if viirs else c.isdigit() and int(c) >= 30

def load():
    counts = {"M": dd(), "V": dd(), "T": dd()}          # T = Terra-only MODIS
    points = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "raw", "*.csv"))):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                viirs = "VIIRS" in (row.get("instrument") or os.path.basename(path)).upper()
                if not keep(viirs, row):
                    continue
                lat, lon, ym = float(row["latitude"]), float(row["longitude"]), row["acq_date"][:7]
                cell = (math.floor(lat / CELL), math.floor(lon / CELL))
                counts["V" if viirs else "M"][cell][ym] += 1
                if not viirs and row.get("satellite", "").lower().startswith("t"):
                    counts["T"][cell][ym] += 1
                points.append((lat, lon, row["acq_date"], "VIIRS" if viirs else "MODIS"))
    return counts, points

def month_totals(series_by_cell, years):
    """tot[cell][mm] summed over the given set of years."""
    tot = defaultdict(lambda: defaultdict(int))
    for cell, series in series_by_cell.items():
        for ym, n in series.items():
            if int(ym[:4]) in years:
                tot[cell][ym[5:]] += n
    return tot

def window(d, mm):          # +-1 calendar month, circular
    i = MM.index(mm)
    return sum(d.get(MM[(i + k) % 12], 0) for k in (-1, 0, 1))

def fit(counts, years, method):
    """Return ratio(cell, mm) for method in const | month | cell."""
    years = set(years)
    tm, tv = month_totals(counts["M"], years), month_totals(counts["V"], years)
    rm = {mm: sum(c.get(mm, 0) for c in tm.values()) for mm in MM}
    rv = {mm: sum(c.get(mm, 0) for c in tv.values()) for mm in MM}
    const = sum(rv.values()) / max(1, sum(rm.values()))
    if method == "const":
        return lambda cell, mm: const
    region = {mm: (window(rv, mm) / window(rm, mm)) if window(rm, mm) else const for mm in MM}
    if method == "month":
        return lambda cell, mm: region[mm]
    def ratio(cell, mm):
        m, v = window(tm.get(cell, {}), mm), window(tv.get(cell, {}), mm)
        return (v + K * region[mm]) / (m + K)
    return ratio

def terra_factor(counts):
    """(Terra+Aqua)/Terra per calendar month, fitted 2003-2011, +-1 month smoothing."""
    yrs = set(range(2003, 2012))
    a = {mm: sum(c.get(mm, 0) for c in month_totals(counts["M"], yrs).values()) for mm in MM}
    t = {mm: sum(c.get(mm, 0) for c in month_totals(counts["T"], yrs).values()) for mm in MM}
    return {mm: window(a, mm) / window(t, mm) if window(t, mm) else 2.0 for mm in MM}

def predict_year(counts, ratio, year):
    """Monthly regional predicted vs observed VIIRS, plus per-cell annual pairs."""
    pred, obs, cp, co = defaultdict(float), defaultdict(float), defaultdict(float), defaultdict(float)
    for cell, s in counts["M"].items():
        for ym, n in s.items():
            if int(ym[:4]) == year:
                pred[ym] += n * ratio(cell, ym[5:]); cp[cell] += n * ratio(cell, ym[5:])
    for cell, s in counts["V"].items():
        for ym, n in s.items():
            if int(ym[:4]) == year:
                obs[ym] += n; co[cell] += n
    months = [f"{year}-{mm}" for mm in MM]
    cells = set(cp) | set(co)
    return [pred[m] for m in months], [obs[m] for m in months], [cp[c] for c in cells], [co[c] for c in cells]

def metrics(p, o):
    return {"mae": round(statistics.mean(abs(x - y) for x, y in zip(p, o)), 1),
            "bias_pct": round(100 * (sum(p) - sum(o)) / sum(o), 1) if sum(o) else None,
            "corr": round(statistics.correlation(p, o), 3) if len(p) > 2 else None}

def validate(counts):
    res, raw = {}, ([], [])
    for method in ("const", "month", "cell"):
        P, O, CP, CO = [], [], [], []
        for y in CV_YEARS:
            ratio = fit(counts, [x for x in CV_YEARS if x != y], method)
            p, o, cp, co = predict_year(counts, ratio, y)
            P += p; O += o; CP += cp; CO += co
            if method == "const":
                raw[0].extend(predict_year(counts, lambda c, m: 1.0, y)[0]); raw[1].extend(o)
        res[method] = {**metrics(P, O), "cell_annual_corr": round(statistics.correlation(CP, CO), 3)}
    best = min(res, key=lambda k: res[k]["mae"])
    # drift: model fitted on the early window, applied to recent years
    r = fit(counts, range(*[FIT[0], FIT[1] + 1]), best)
    P, O = [], []
    for y in range(DRIFT[0], DRIFT[1] + 1):
        p, o, _, _ = predict_year(counts, r, y); P += p; O += o
    return {"scheme": f"leave-one-year-out {CV_YEARS[0]}-{CV_YEARS[-1]}", "models": res, "best": best,
            "raw_modis": metrics(*raw), "drift": {"years": DRIFT, **metrics(P, O)}}

def ratio_by_year(counts):
    out = {}
    for y in range(VIIRS_START, 2100):
        m = sum(n for s in counts["M"].values() for ym, n in s.items() if int(ym[:4]) == y)
        v = sum(n for s in counts["V"].values() for ym, n in s.items() if int(ym[:4]) == y)
        if not m:
            break
        out[y] = round(v / m, 2)
    return out

def harmonize(counts, ratio, tf):
    cells = []
    for cell in set(counts["M"]) | set(counts["V"]):
        m, v = counts["M"].get(cell, {}), counts["V"].get(cell, {})
        h = {}
        for ym, n in m.items():
            if int(ym[:4]) < VIIRS_START:
                h[ym] = round(n * (tf[ym[5:]] if ym < AQUA_START else 1) * ratio(cell, ym[5:]), 1)
        h.update({ym: n for ym, n in v.items() if int(ym[:4]) >= VIIRS_START})
        cells.append({"la": (cell[0] + .5) * CELL, "lo": (cell[1] + .5) * CELL, "m": m, "v": v, "h": h})
    return cells

def main():
    counts, points = load()
    if not points:
        raise SystemExit("No CSVs in data/raw - run tools/make_demo_data.py or download FIRMS archive CSVs")
    val = validate(counts)
    tf = terra_factor(counts)
    ratio = fit(counts, range(FIT[0], FIT[1] + 1), val["best"])
    cells = harmonize(counts, ratio, tf)
    # sensitivity: same model fitted on the full overlap instead of the early window
    full = harmonize(counts, fit(counts, range(VIIRS_START, DRIFT[1] + 1), val["best"]), tf)
    pre = lambda cs: sum(n for c in cs for ym, n in c["h"].items() if int(ym[:4]) < VIIRS_START)
    yms = sorted({ym for c in cells for ym in c["h"]})
    meta = {"cell_deg": CELL, "viirs_start": VIIRS_START, "fit_window": FIT, "first": yms[0], "last": yms[-1],
            "terra_only_factor": {k: round(x, 2) for k, x in tf.items()},
            "ratio_by_year": ratio_by_year(counts),
            "backcast_sensitivity_pct": round(100 * (pre(full) - pre(cells)) / pre(cells), 1),
            "validation": val}
    os.makedirs(OUT, exist_ok=True)
    json.dump(cells, open(os.path.join(OUT, "cells.json"), "w"), separators=(",", ":"))
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
    with open(os.path.join(OUT, "points.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["latitude", "longitude", "acq_date", "sensor"]); w.writerows(points)
    print(f"{len(points)} hotspots, {len(cells)} cells, {meta['first']}..{meta['last']}")
    print(json.dumps({k: meta[k] for k in ("ratio_by_year", "backcast_sensitivity_pct", "validation")}, indent=1))

if __name__ == "__main__":
    main()
