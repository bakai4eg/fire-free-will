"""Monthly historical weather per region from NASA POWER (free, no key) -> web/data/weather.json
For each region in data/regions.json: 2x2 grid of points inside the bbox, averaged.
Output: {region: {"YYYY-MM": [mean air temperature degC, precipitation sum mm]}}"""
import calendar, json, os, statistics, time, urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
URL = ("https://power.larc.nasa.gov/api/temporal/monthly/point?parameters=T2M,PRECTOTCORR"
       "&community=AG&latitude={la:.3f}&longitude={lo:.3f}&start=2001&end=2025&format=JSON")

regions = json.load(open(os.path.join(ROOT, "data", "regions.json"), encoding="utf-8"))
out = {}
for rid, r in regions.items():
    s, w, n, e = r["bbox"]
    t, p = {}, {}
    for la in (s + (n - s) * .3, s + (n - s) * .7):
        for lo in (w + (e - w) * .3, w + (e - w) * .7):
            d = json.load(urllib.request.urlopen(URL.format(la=la, lo=lo), timeout=120))["properties"]["parameter"]
            for k, v in d["T2M"].items():
                if k[4:] == "13" or v == -999: continue           # 13 = annual value
                ym = f"{k[:4]}-{k[4:]}"; t.setdefault(ym, []).append(v)
                mm = d["PRECTOTCORR"][k]                           # mm/day -> mm/month
                if mm != -999: p.setdefault(ym, []).append(mm * calendar.monthrange(int(k[:4]), int(k[4:]))[1])
            time.sleep(.5)
    out[rid] = {ym: [round(statistics.mean(t[ym]), 1), round(statistics.mean(p.get(ym, [0])), 1)] for ym in sorted(t)}
    print(rid, len(out[rid]), "months")
json.dump(out, open(os.path.join(ROOT, "web", "data", "weather.json"), "w"), separators=(",", ":"))
