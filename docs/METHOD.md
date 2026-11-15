# Harmonization method (BurnBeat)

**Goal:** one consistent monthly hotspot series 2001–2025 for Kyrgyzstan, where the sensor no longer matters.
Unit of the harmonized series: **VIIRS S-NPP-equivalent detections** per 0.25° cell per month.

## Data
NASA FIRMS archive: MODIS Collection 6.1 (Terra + Aqua, 1 km, 2000–2025) and VIIRS S-NPP 375 m (2012–2025), Kyrgyzstan country files.
~29 000 detections after filtering.

## Steps
1. **Filtering.** Only `type = 0` (presumed vegetation fire; volcanoes, static industrial sources and offshore removed). MODIS confidence ≥ 30; VIIRS confidence nominal or high.
2. **Terra-only gap.** Before Aqua (July 2002) only Terra observed. MODIS counts for those months are multiplied by the (Terra + Aqua) / Terra ratio per calendar month, fitted 2003–2011 (≈ 2.2).
3. **VIIRS/MODIS ratio.** For each 0.25° cell and calendar month:
   `ratio = (V_cell + K · R_region) / (M_cell + K)`, with V and M summed over ±1 month (seasonal smoothing),
   `R_region` = regional ratio for that month, `K = 10`. Cells with few MODIS detections fall back to the regional ratio (shrinkage).
4. **Fit window = 2012–2016.** The VIIRS/MODIS ratio rises from ≈3.3 (2013–2017) to ≈4.6 (2021–2025) because Terra and Aqua orbits drift and MODIS detects less. For back-casting the 2000s, the early overlap is the closest match to how MODIS behaved before 2012.
5. **Harmonized series** = scaled MODIS before 2012, observed VIIRS S-NPP from 2012.

## Validation (leave-one-year-out, 2012–2019)
Each year is hidden in turn, the ratio is fitted on the other years, and MODIS of the hidden year is converted and compared with what VIIRS really saw.

| Model | MAE, detections/month | Bias | Monthly corr. | Cell-level annual corr. |
|---|---|---|---|---|
| Raw MODIS (no harmonization) | 79.1 | −72 % | 0.91 | — |
| One constant ratio | 35.2 | +0.1 % | 0.906 | 0.716 |
| Ratio per calendar month | 31.5 | +1.7 % | 0.929 | 0.728 |
| **Per cell + month, shrunk (used)** | **27.5** | **−1.6 %** | **0.943** | **0.800** |

## Fire and weather (NASA POWER)
Monthly air temperature and precipitation per region from NASA POWER (`tools/fetch_weather.py`, 2×2 points per region averaged).
For the 5 peak months of each region, 2012–2025 (VIIRS era, so no sensor mixing), standardized log(hotspots) vs standardized rainfall:

| Region | r (rain ↔ fires) | r (temperature ↔ fires) |
|---|---|---|
| All Kyrgyzstan | −0.46 | +0.22 |
| Osh | −0.44 | +0.27 |
| Jalal-Abad | −0.36 | +0.25 |
| Issyk-Kul | −0.36 | +0.19 |
| Chui | −0.35 | +0.16 |

n = 70 months per region; |r| > 0.31 is significant at p < 0.01. **Wet months burn less everywhere.** Annual totals give misleading correlations because of the long-term decline in burning, so only within-month anomalies are used.

## Global harmonization (1° grid, `tools/global_pipeline.py`)
Same method on the whole planet: NASA FIRMS yearly global archives, MODIS 2000–2025 and VIIRS S-NPP 2012–2025, 1° cells.
The ratio is shrunk toward the 10° block ratio (instead of the Kyrgyz regional one), Terra-only months scaled the same way.
Leave-one-year-out validation 2012–2019, global monthly totals:

| Model | MAE, hotspots/month (world) | Bias | Monthly corr. | Cell-level annual corr. |
|---|---|---|---|---|
| Raw MODIS | 1 042 951 | −75.2 % | 0.952 | 0.968 |
| One constant ratio | 88 762 | 0.0 % | 0.950 | 0.968 |
| **Per cell + month, shrunk (used)** | **54 491** | **−0.3 %** | **0.963** | 0.912 |

The cell model wins on error and monthly correlation; the constant ratio keeps a higher cell-level correlation because it does not
rescale cells relative to each other. Both are far better than raw data, which jumps from ~4.4 M to ~17.4 M hotspots a year in 2012.
The harmonized world series stays at 15–19 M hotspots a year for 2001–2025.

## Live layer and "now vs normal"
- Last 7 days: public FIRMS NRT files (VIIRS NOAA-20 and NOAA-21; S-NPP no longer publishes NRT), `tools/fetch_live.py`, no API key.
- NRT files have no `type` column, so factories and power plants are removed with a mask of persistent FIRMS type 2–3 locations from the archive (`web/api/static_sources.json`, ~1.5 km radius).
- "Now vs normal" compares **NOAA-20 only** (a single satellite, like the S-NPP-based norm) for 7 days with the monthly median × 7 / days in month.
  The normal for this comparison is the **VIIRS-era median (2012 onward)**, so it is not pulled by converted MODIS years or by the long-term decline; it does not depend on the month being browsed.
  A ratio is shown only when the expected weekly count is at least 3; below that, a large count is reported as "unusual for the season" instead of a dramatic ratio.
- Worldwide, "now" and the normal are counted over **the same 1° cells** (cell centres inside the country or box; the nearest cells for very small places). In Kyrgyzstan both use the exact region borders.
- Gas flares and industry in the worldwide NRT files: places (~1 km) that glow on 5 or more of the 7 days are removed (≈2 800 places per run). The live layer is rebuilt on the server every 3 hours.
- Kyrgyz regions use real borders (geoBoundaries ADM1, ODbL); villages from GeoNames (CC-BY), nearest within 3 km.
- Fire danger (today + 3 days) is a rating of conditions, not a fire forecast: season share, anomaly, 24 h detections, Open-Meteo forecast (temperature, humidity, wind, rain). Same rules as the Telegram bot.

## Known limitations (stated honestly)
- **2001:** Terra only until July 2002; the first half of 2001 is scaled by the (Terra + Aqua) / Terra factor, so 2001 is a rougher estimate. On the world level it comes out as the highest year, which should not be over-interpreted.
- **MODIS drift:** the 2012–2016 model applied to 2021–2025 under-predicts VIIRS by 25 %. This does not affect the output, because VIIRS is used directly from 2012. It is the reason for step 4.
- **Fit-window sensitivity:** fitting on the full overlap (2012–2025) instead of 2012–2016 raises pre-2012 values by about 10 %. Treat this as the uncertainty of the 2001–2011 part.
- The ratio also depends on fire size: many small agricultural fires are seen by VIIRS but not MODIS. Year-to-year ratio noise (2.7–5.3) reflects this.
- Bounding boxes for regions are approximate.

Numbers are regenerated by `python pipeline.py` and stored in `web/data/meta.json`.
