"""Validate the harmonization country by country (leave-one-year-out, 2012-2019).

  python tools/validate_countries.py            # downloads NASA FIRMS country CSVs (MODIS + VIIRS S-NPP, 2012-2019)

Same method as pipeline.py / global_pipeline.py: type 0, MODIS confidence >= 30, VIIRS nominal/high,
VIIRS/MODIS ratio per 1-degree cell and calendar month (+-1 month smoothing), shrunk toward the
country ratio for that month (K = 10). Each year is hidden in turn, the ratio is fitted on the other
years, and the hidden year's MODIS is converted and compared with what VIIRS really saw.
Output: web/data/global/validation_countries.json (+ a table printed for docs/METHOD.md)."""
import io, json, math, os, statistics, sys, urllib.request
from collections import defaultdict

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
WORK = os.path.join(ROOT, "work", "countries")
OUT = os.environ.get("BURNBEAT_VALC_OUT") or os.path.join(ROOT, "web", "data", "global", "validation_countries.json")
URL = "https://firms.modaps.eosdis.nasa.gov/data/country/{s}/{y}/{s}_{y}_{c}.csv"
YEARS = range(2012, 2020)
K = 10
MM = [f"{i:02d}" for i in range(1, 13)]
COUNTRIES = ["Kyrgyzstan", "Kazakhstan", "Uzbekistan", "Tajikistan", "Mongolia", "Turkey",
             "Greece", "Portugal", "Spain", "Chile", "Ukraine", "Nepal"]


def cell_of(lat, lon):
    return (min(179, math.floor(lat) + 90)) * 360 + (math.floor(lon) + 180) % 360


def counts(sensor, year, country):
    """{(cell, 'YYYY-MM'): n} for one country-year, cached as JSON."""
    path = os.path.join(WORK, f"{country}_{sensor}_{year}.json")
    if os.path.exists(path):
        return {(c, ym): n for c, ym, n in json.load(open(path))}
    viirs = sensor.startswith("viirs")
    out = defaultdict(int)
    req = urllib.request.Request(URL.format(s=sensor, y=year, c=country), headers={"User-Agent": "burnbeat-validation"})
    with urllib.request.urlopen(req, timeout=300) as r:
        f = io.TextIOWrapper(r, encoding="utf-8", errors="replace")
        head = f.readline().strip().split(",")
        i_la, i_lo, i_d, i_c = (head.index(k) for k in ("latitude", "longitude", "acq_date", "confidence"))
        i_t = head.index("type") if "type" in head else None
        for line in f:
            p = line.split(",")
            if len(p) < len(head):
                continue
            if i_t is not None and p[i_t].strip() not in ("0", ""):
                continue
            c = p[i_c].strip().lower()
            if viirs:
                if c not in ("n", "h", "nominal", "high"):
                    continue
            elif not c.isdigit() or int(c) < 30:
                continue
            out[(cell_of(float(p[i_la]), float(p[i_lo])), p[i_d][:7])] += 1
    os.makedirs(WORK, exist_ok=True)
    json.dump([[c, ym, n] for (c, ym), n in out.items()], open(path + ".tmp", "w"))
    os.replace(path + ".tmp", path)
    return dict(out)


def win(d, mm):
    i = MM.index(mm)
    return sum(d.get(MM[(i + k) % 12], 0) for k in (-1, 0, 1))


def validate(M, V):
    """M, V: {year: {(cell, ym): n}} -> metrics for raw, constant ratio and cell model."""
    res = {}
    for method in ("raw", "const", "cell"):
        P, O = [], []
        for y in YEARS:
            fit_years = [x for x in YEARS if x != y]
            tm, tv = defaultdict(lambda: defaultdict(int)), defaultdict(lambda: defaultdict(int))
            for x in fit_years:
                for (c, ym), n in M[x].items(): tm[c][ym[5:]] += n
                for (c, ym), n in V[x].items(): tv[c][ym[5:]] += n
            gm = {mm: sum(t.get(mm, 0) for t in tm.values()) for mm in MM}
            gv = {mm: sum(t.get(mm, 0) for t in tv.values()) for mm in MM}
            country = {mm: win(gv, mm) / max(1, win(gm, mm)) for mm in MM}
            const = sum(gv.values()) / max(1, sum(gm.values()))
            def r(c, mm):
                if method == "raw": return 1.0
                if method == "const": return const
                return (win(tv.get(c, {}), mm) + K * country[mm]) / (win(tm.get(c, {}), mm) + K)
            pm, om = defaultdict(float), defaultdict(float)
            for (c, ym), n in M[y].items(): pm[ym] += n * r(c, ym[5:])
            for (c, ym), n in V[y].items(): om[ym] += n
            for ym in [f"{y}-{mm}" for mm in MM]:
                P.append(pm.get(ym, 0.0)); O.append(om.get(ym, 0.0))
        s = sum(O)
        res[method] = {"mae": round(statistics.mean(abs(a - b) for a, b in zip(P, O)), 1),
                       "bias_pct": round(100 * (sum(P) - s) / s, 1) if s else None,
                       "corr": round(statistics.correlation(P, O), 3) if len(set(P)) > 1 else None}
    return res


def main():
    countries = sys.argv[1:] or COUNTRIES
    out = {}
    if os.path.exists(OUT):
        out = json.load(open(OUT)).get("countries", {})
    for country in countries:
        try:
            M = {y: counts("modis", y, country) for y in YEARS}
            V = {y: counts("viirs-snpp", y, country) for y in YEARS}
        except Exception as e:
            print(country, "skipped:", e, flush=True)
            continue
        res = validate(M, V)
        res["viirs_per_year"] = round(sum(sum(V[y].values()) for y in YEARS) / len(YEARS))
        out[country] = res
        print(country, json.dumps(res), flush=True)
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump({"scheme": "leave-one-year-out 2012-2019, 1-degree cells, ratio shrunk toward the country ratio (K=10)",
                   "countries": out}, open(OUT, "w"), indent=1)
    print("\n| Country | VIIRS hotspots/yr | MAE raw -> BurnBeat | Error smaller | Bias raw -> BurnBeat | Corr |")
    print("|---|---|---|---|---|---|")
    for c, r in sorted(out.items(), key=lambda kv: -kv[1]["viirs_per_year"]):
        x = r["raw"]["mae"] / max(0.1, r["cell"]["mae"])
        print(f"| {c} | {r['viirs_per_year']:,} | {r['raw']['mae']} -> **{r['cell']['mae']}** | {x:.1f}x | "
              f"{r['raw']['bias_pct']}% -> **{r['cell']['bias_pct']}%** | {r['cell']['corr']} |")


if __name__ == "__main__":
    main()
