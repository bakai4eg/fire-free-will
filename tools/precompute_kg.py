"""Pre-compute, once, what the browser used to compute on every page load (it took ~4 s):
for every Kyrgyz archive hotspot: its region (geoBoundaries ADM1) and the nearest village within 3.5 km (GeoNames).
Output web/data/kg_points.json: {"regions": [...], "rows": [[lat, lon, "YYYY-MM", region_index|-1, village_index|-1, km*10]]}"""
import csv, json, math, os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
regions = json.load(open(os.path.join(ROOT, "web", "data", "kg_regions.json")))["features"]
vill = json.load(open(os.path.join(ROOT, "web", "data", "villages.json"), encoding="utf-8"))
keys = sorted({f["properties"]["key"] for f in regions})

def ring_has(ring, x, y):
    k, j = False, len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]; xj, yj = ring[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            k = not k
        j = i
    return k

def poly_has(poly, x, y):
    return ring_has(poly[0], x, y) and not any(ring_has(h, x, y) for h in poly[1:])

def bbox(geom):
    pts = [p for poly in (geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]) for p in poly[0]]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)

for f in regions:
    f["bb"] = bbox(f["geometry"])

def region_of(lo, la):
    for f in regions:
        b = f["bb"]
        if lo < b[0] or lo > b[2] or la < b[1] or la > b[3]:
            continue
        g = f["geometry"]
        if (poly_has(g["coordinates"], lo, la) if g["type"] == "Polygon" else any(poly_has(p, lo, la) for p in g["coordinates"])):
            return keys.index(f["properties"]["key"])
    return -1

grid = {}
for k, v in enumerate(vill):
    grid.setdefault((math.floor(v[2] * 10), math.floor(v[3] * 10)), []).append(k)

def nearest(la, lo, max_km=3.5):
    best, bd = -1, max_km
    i0, j0 = math.floor(la * 10), math.floor(lo * 10)
    for i in range(i0 - 1, i0 + 2):
        for j in range(j0 - 1, j0 + 2):
            for k in grid.get((i, j), []):
                x = (vill[k][3] - lo) * math.cos(math.radians((la + vill[k][2]) / 2)); y = vill[k][2] - la
                d = 111.2 * math.hypot(x, y)
                if d < bd:
                    bd, best = d, k
    return best, bd

rows = []
with open(os.path.join(ROOT, "web", "data", "points.csv"), newline="") as f:
    for r in csv.DictReader(f):
        la, lo = float(r["latitude"]), float(r["longitude"])
        reg = region_of(lo, la)
        vk, km = nearest(la, lo)
        rows.append([round(la, 4), round(lo, 4), r["acq_date"][:7], reg, vk, round(km * 10) if vk >= 0 else -1])
json.dump({"regions": keys, "rows": rows}, open(os.path.join(ROOT, "web", "data", "kg_points.json"), "w"), separators=(",", ":"))
print(len(rows), "points,", sum(1 for r in rows if r[3] >= 0), "inside Kyrgyzstan,", sum(1 for r in rows if r[4] >= 0), "near a village")
