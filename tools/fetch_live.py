"""Last 7 days of satellite hotspots for Central Asia -> web/data/live.json (no API key needed).

Source: NASA FIRMS public near-real-time files (VIIRS NOAA-20 and NOAA-21; S-NPP no longer publishes NRT).
NRT files have no "type" column, so factories / power plants are removed with web/api/static_sources.json
(FIRMS type 2-3 locations from the archive). Confidence: nominal/high only."""
import csv, io, json, os, urllib.request
from datetime import datetime, timezone

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
BASE = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/"
FILES = {"NOAA-20": "noaa-20-viirs-c2/csv/J1_VIIRS_C2_Russia_Asia_7d.csv",
         "NOAA-21": "noaa-21-viirs-c2/csv/J2_VIIRS_C2_Russia_Asia_7d.csv"}
BOX = (35.0, 46.0, 56.0, 88.0)          # south, west, north, east: Central Asia
R = 0.015                               # ~1.5 km static-source mask radius

mask = json.load(open(os.path.join(ROOT, "web", "api", "static_sources.json")))
static = lambda la, lo: any(abs(la - a) <= R and abs(lo - b) <= R * 1.35 for a, b in mask)
points, seen = [], set()
for sat, path in FILES.items():
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "BurnBeat/1.0"})
    for row in csv.DictReader(io.StringIO(urllib.request.urlopen(req, timeout=60).read().decode("utf-8"))):
        la, lo = float(row["latitude"]), float(row["longitude"])
        if not (BOX[0] <= la <= BOX[2] and BOX[1] <= lo <= BOX[3]) or row["confidence"].strip().lower() not in ("n", "h", "nominal", "high"):
            continue
        if static(la, lo):
            continue
        key = (round(la, 2), round(lo, 2), row["acq_date"])      # one fire seen by both satellites = one point
        if key in seen:
            continue
        seen.add(key)
        points.append([round(la, 4), round(lo, 4), f'{row["acq_date"]} {row["acq_time"].zfill(4)[:2]}:{row["acq_time"].zfill(4)[2:]}', sat, float(row["frp"])])
points.sort(key=lambda p: p[2], reverse=True)
out = {"updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), "days": 7, "box": BOX, "points": points}
json.dump(out, open(os.path.join(ROOT, "web", "data", "live.json"), "w"), separators=(",", ":"))
print(len(points), "live hotspots in Central Asia; newest", points[0][2] if points else "-")
