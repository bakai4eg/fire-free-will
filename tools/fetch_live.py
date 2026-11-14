"""Last 7 days of satellite hotspots for the whole world -> web/data/live/ (no API key needed).

Source: NASA FIRMS public near-real-time global files, VIIRS NOAA-20 and NOAA-21 (S-NPP no longer publishes NRT).
Filtering (NRT files have no "type" column):
  * confidence nominal/high only;
  * static sources: places (~1 km) that glow on >= 5 of the 7 days are gas flares / industry, not fires -> dropped;
    in Kyrgyzstan the archive mask web/api/static_sources.json is applied as well;
  * one fire seen by both satellites on the same day (same ~1 km cell) is kept once.
Output (small enough for a static site):
  live/summary.json          updated time + per 1-degree cell [cellIndex, n_noaa20, n_all]
  live/t_<lat10>_<lon10>.json points of one 10x10-degree tile: [lat, lon, "YYYY-MM-DD HH:MM", sat(20|21), frp]"""
import csv, io, json, math, os, shutil, urllib.request
from collections import defaultdict
from datetime import datetime, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "web", "data", "live")
BASE = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/"
FILES = {20: "noaa-20-viirs-c2/csv/J1_VIIRS_C2_Global_7d.csv", 21: "noaa-21-viirs-c2/csv/J2_VIIRS_C2_Global_7d.csv"}
R = 0.015

mask = json.load(open(os.path.join(ROOT, "web", "api", "static_sources.json")))
kg_static = lambda la, lo: any(abs(la - a) <= R and abs(lo - b) <= R * 1.35 for a, b in mask)

rows = []
for sat, path in FILES.items():
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "BurnBeat/1.0", "Accept-Encoding": "identity"})
    text = urllib.request.urlopen(req, timeout=300).read().decode("utf-8")
    for r in csv.DictReader(io.StringIO(text)):
        if r["confidence"].strip().lower() not in ("n", "h", "nominal", "high"):
            continue
        t = r["acq_time"].zfill(4)
        rows.append((float(r["latitude"]), float(r["longitude"]), r["acq_date"], f'{r["acq_date"]} {t[:2]}:{t[2:]}', sat, float(r["frp"])))
    print(sat, "rows so far", len(rows), flush=True)

days = defaultdict(set)                     # ~1 km cell -> days seen
for la, lo, d, *_ in rows:
    days[(round(la, 2), round(lo, 2))].add(d)
static = {k for k, v in days.items() if len(v) >= 5}

seen, kept = set(), []
for la, lo, d, ts, sat, frp in sorted(rows, key=lambda x: x[3], reverse=True):
    k = (round(la, 2), round(lo, 2))
    if k in static or (39 <= la <= 43.5 and 69 <= lo <= 80.5 and kg_static(la, lo)):
        continue
    if (k, d) in seen:
        if sat == 20:                       # still count it for the NOAA-20-only comparison
            kept.append((la, lo, ts, sat, frp, True))
        continue
    seen.add((k, d))
    kept.append((la, lo, ts, sat, frp, False))

shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
cells, tiles = defaultdict(lambda: [0, 0]), defaultdict(list)
for la, lo, ts, sat, frp, dup in kept:
    c = (min(179, math.floor(la) + 90)) * 360 + (math.floor(lo) + 180) % 360
    if sat == 20: cells[c][0] += 1
    if not dup:
        cells[c][1] += 1
        tiles[(math.floor(la / 10), math.floor(lo / 10))].append([round(la, 3), round(lo, 3), ts, sat, round(frp, 1)])
for (a, b), pts in tiles.items():
    json.dump(pts, open(os.path.join(OUT, f"t_{a}_{b}.json"), "w"), separators=(",", ":"))
newest = kept[0][2] if kept else ""
json.dump({"updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), "newest": newest, "days": 7,
           "static_removed": len(static), "cells": [[c, v[0], v[1]] for c, v in cells.items()]},
          open(os.path.join(OUT, "summary.json"), "w"), separators=(",", ":"))
print(f"{len(kept)} kept, {len(static)} static places removed, {len(tiles)} tiles, newest {newest}")
