"""MODIS + VIIRS harmonization -> web/data/{cells.json, meta.json, points.csv}
Input: FIRMS archive CSVs in data/raw/ (any file with latitude, longitude, acq_date, confidence, [type], [instrument]).
Method: per 0.25deg cell and calendar month, ratio = VIIRS / MODIS over the overlap years;
pre-VIIRS MODIS months are scaled by that ratio ("VIIRS-equivalent" counts). Stdlib only."""
import csv, glob, json, math, os, statistics
from collections import defaultdict

CELL = 0.25                 # grid size, degrees
VIIRS_START = 2012          # first full VIIRS S-NPP year
OVERLAP = (2012, 2025)      # full years with both sensors, used to fit ratios
TRAIN, TEST = (2012, 2018), (2019, 2025)   # validation split
MIN_MODIS = 5               # below this, the cell falls back to the region-wide ratio
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "web", "data")

def sensor_of(path, row):
    s = (row.get("instrument") or os.path.basename(path)).upper()
    return "V" if "VIIRS" in s else "M"

def keep(sensor, row):
    if row.get("type", "0") not in ("0", ""):          # 0 = presumed vegetation fire
        return False
    c = row["confidence"].strip().lower()
    return c in ("n", "h", "nominal", "high") if sensor == "V" else c.isdigit() and int(c) >= 30

def load():
    counts = {"M": defaultdict(lambda: defaultdict(int)), "V": defaultdict(lambda: defaultdict(int))}
    points = []
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "raw", "*.csv"))):
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                s = sensor_of(path, row)
                if not keep(s, row):
                    continue
                lat, lon, ym = float(row["latitude"]), float(row["longitude"]), row["acq_date"][:7]
                cell = (math.floor(lat / CELL), math.floor(lon / CELL))
                counts[s][cell][ym] += 1
                points.append((lat, lon, row["acq_date"], "VIIRS" if s == "V" else "MODIS"))
    return counts, points

def fit_ratios(counts, years):
    """ratio[cell][month], with region-wide per-month fallback."""
    inside = lambda ym: years[0] <= int(ym[:4]) <= years[1]
    tot = {s: defaultdict(lambda: defaultdict(int)) for s in "MV"}   # tot[s][cell][mm]
    for s in "MV":
        for cell, series in counts[s].items():
            for ym, n in series.items():
                if inside(ym):
                    tot[s][cell][ym[5:]] += n
    region = {}
    for mm in (f"{i:02d}" for i in range(1, 13)):
        m = sum(c[mm] for c in tot["M"].values()); v = sum(c[mm] for c in tot["V"].values())
        region[mm] = v / m if m else 1.0
    def ratio(cell, mm):
        m = tot["M"].get(cell, {}).get(mm, 0)
        return tot["V"][cell][mm] / m if m >= MIN_MODIS else region[mm]
    return ratio, region

def validate(counts):
    ratio, _ = fit_ratios(counts, TRAIN)
    obs, pred, raw = defaultdict(float), defaultdict(float), defaultdict(float)
    for cell, series in counts["M"].items():
        for ym, n in series.items():
            if TEST[0] <= int(ym[:4]) <= TEST[1]:
                pred[ym] += n * ratio(cell, ym[5:]); raw[ym] += n
    for series in counts["V"].values():
        for ym, n in series.items():
            if TEST[0] <= int(ym[:4]) <= TEST[1]:
                obs[ym] += n
    months = sorted(set(obs) | set(pred))
    o = [obs[m] for m in months]; p = [pred[m] for m in months]; r = [raw[m] for m in months]
    mae = lambda a: round(statistics.mean(abs(x - y) for x, y in zip(a, o)), 1)
    return {"train": TRAIN, "test": TEST, "months": len(months),
            "mae_harmonized": mae(p), "mae_raw_modis": mae(r),
            "bias_pct": round(100 * (sum(p) - sum(o)) / sum(o), 1) if sum(o) else None,
            "corr": round(statistics.correlation(p, o), 3) if len(months) > 2 else None}

def main():
    counts, points = load()
    if not points:
        raise SystemExit("No CSVs in data/raw - run tools/make_demo_data.py or download FIRMS archive CSVs")
    ratio, region = fit_ratios(counts, OVERLAP)
    cells = []
    for cell in set(counts["M"]) | set(counts["V"]):
        m, v = counts["M"].get(cell, {}), counts["V"].get(cell, {})
        h = {ym: round(n * ratio(cell, ym[5:]), 1) for ym, n in m.items() if int(ym[:4]) < VIIRS_START}
        h.update({ym: n for ym, n in v.items() if int(ym[:4]) >= VIIRS_START})
        cells.append({"la": (cell[0] + .5) * CELL, "lo": (cell[1] + .5) * CELL, "m": m, "v": v, "h": h})
    os.makedirs(OUT, exist_ok=True)
    json.dump(cells, open(os.path.join(OUT, "cells.json"), "w"), separators=(",", ":"))
    yms = sorted({ym for c in cells for ym in c["h"]})
    meta = {"cell_deg": CELL, "viirs_start": VIIRS_START, "overlap": OVERLAP, "first": yms[0], "last": yms[-1],
            "region_ratio_by_month": {k: round(x, 2) for k, x in region.items()}, "validation": validate(counts)}
    json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
    with open(os.path.join(OUT, "points.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["latitude", "longitude", "acq_date", "sensor"]); w.writerows(points)
    print(f"{len(points)} hotspots, {len(cells)} cells, {meta['first']}..{meta['last']}")
    print("validation:", meta["validation"])

if __name__ == "__main__":
    main()
