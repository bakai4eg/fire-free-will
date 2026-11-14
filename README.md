# Fire Calendar — MODIS + VIIRS harmonized hotspots

```
python tools/make_demo_data.py   # FAKE data (delete data/raw/*_Demo.csv when real data is in)
python pipeline.py               # data/raw/*.csv -> web/data/{cells.json, meta.json, points.csv}
python -m http.server 8000 -d web   # open http://localhost:8000
```
No pip installs needed (Python stdlib + CDN libs).

## Real data
FIRMS archive, yearly CSVs per country: https://firms.modaps.eosdis.nasa.gov/country/
Take MODIS (2001–now) and VIIRS S-NPP (2012–now) for Kyrgyzstan (+ Kazakhstan if KG is sparse).
Put them into `data/raw/`, rerun `pipeline.py`. Settings (grid size, overlap years) are at the top of `pipeline.py`.

## Who does what
| Role | Task |
|---|---|
| Data | Download real FIRMS CSVs, check how many KG points exist, fix column names if needed |
| Science | Improve harmonization (per land-cover ratio, day/night, NOAA-20), validation numbers for the pitch |
| Front 1 | Map: polygon draw, lat/lon input, region presets (oblasts) |
| Front 2 | Calendar look, RU/EN switch, mobile |
| Features | "season onset/peak/end", compare two regions, PDF report |
| Pitch | User story (MChS / ayil okmotu), slides, demo video, **AI-use description (required by Space Apps)** |
