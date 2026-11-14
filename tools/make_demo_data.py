"""Generate FAKE FIRMS-like CSVs (Chui region, Kyrgyzstan) so the app works before real data arrives.
Writes data/raw/{modis|viirs-snpp}_{year}_Demo.csv in the FIRMS archive column layout.
Delete these files once real FIRMS CSVs are in data/raw."""
import csv, os, random

random.seed(42)
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
os.makedirs(OUT, exist_ok=True)
LAT, LON = (42.4, 43.2), (73.3, 75.8)
SEASON = {1: .2, 2: .3, 3: 2.5, 4: 4, 5: 1, 6: .4, 7: .6, 8: 1.2, 9: 2.5, 10: 3.5, 11: 1, 12: .2}
COLS = ["latitude", "longitude", "acq_date", "confidence", "type", "instrument"]

for year in range(2001, 2027):
    trend = 1 + 0.03 * (year - 2001) + random.uniform(-.3, .5)
    last_month = 10 if year == 2026 else 12
    for sensor, start, mult in (("modis", 2001, 1), ("viirs-snpp", 2012, 3.2)):
        if year < start:
            continue
        rows = []
        for m in range(1, last_month + 1):
            n = int(random.gauss(8 * SEASON[m] * trend * mult, 3))
            for _ in range(max(n, 0)):
                conf = random.randint(10, 100) if sensor == "modis" else random.choice("lnnhh")
                rows.append([round(random.uniform(*LAT), 4), round(random.uniform(*LON), 4),
                             f"{year}-{m:02d}-{random.randint(1, 28):02d}", conf,
                             random.choice([0] * 19 + [2]), "MODIS" if sensor == "modis" else "VIIRS"])
        with open(os.path.join(OUT, f"{sensor}_{year}_Demo.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(COLS); w.writerows(rows)
print("demo data written to", os.path.abspath(OUT))
