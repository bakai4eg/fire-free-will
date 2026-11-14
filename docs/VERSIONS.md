# Night versions (branch `night`)

Each version is a git tag and is hosted on the server for comparison:
`https://34-40-83-150.sslip.io/v1/` … `/v6/`. The main site (`/` and GitHub Pages) was not changed overnight.

| Version | What it adds | Look at |
|---|---|---|
| **v1** | One-screen tool: world map on the left, panel on the right, click anywhere / drag an area, region buttons | `/v1/` |
| **v2** | Plain-language sentence on top ("burns most in August and March; this month is 25 % below normal"), **live last 7 days** layer, real Kyrgyz region borders, individual hotspot dots when zoomed, period buttons (Year / 5 / 10 / 25 years) instead of date fields, method charts hidden under "How it is calculated" | `/v2/?bbox=42.2,72.8,43.3,76` |
| **v3** | Rotating **3D globe** for the world view (drag to spin, click to pick), 2D/3D toggle | `/v3/` |
| **v4** | **Villages near fires** (GeoNames): ranking for the region, live list shows "Orlovka · 2 km" instead of coordinates, Bishkek time | `/v4/?bbox=42.2,72.8,43.3,76` |
| **v5** | Kyrgyz regions open in **"Now" mode**: "Right now in Chui: 33 hotspots in 7 days, a normal November week has ~2 — 19× more"; correct Russian number agreement; 2001 note | `/v5/?bbox=42.2,72.8,43.3,76` |
| **v6** | **Fire danger today + 3 days** card (same rules as the bot, Open-Meteo forecast) | `/v6/?bbox=39.3,72.4,40.9,75` |

To make a version the real site: `git checkout main && git merge vN` (or reset main to the tag) and push; GitHub Pages and the server update themselves.

## Not done / needs a decision
- **Live data refresh:** `web/data/live.json` was fetched once (night of 15 Nov). For "now" to stay current it must be refreshed (e.g. every 3 h on the server or in GitHub Actions). Not set up, waiting for approval.
- **Jan–Nov 2026 backfill** needs a FIRMS MAP_KEY.
- **Kyrgyz text** should be checked by a native speaker.
