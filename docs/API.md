# BurnBeat API (для бота)

Статические JSON-файлы на GitHub Pages. Без ключей и авторизации, просто `GET`.
Пересобираются командой `python pipeline.py` и обновляются на сайте после пуша в `main`.

База: `https://bakai4eg.github.io/fire-free-will/api/`

| Endpoint | Что отдаёт |
|---|---|
| `regions.json` | Список областей: `{id: {name, bbox}}`. bbox = `[юг, запад, север, восток]` |
| `summary/{id}.json` | Сводка по одной области (см. ниже). id: `kg, chui, talas, issykkul, naryn, jalalabad, osh, batken` |
| `all.json` | `{data_until, regions: {id: summary}}` — всё за один запрос, удобно для утренней сводки |

Пример: `https://bakai4eg.github.io/fire-free-will/api/summary/chui.json`

## Формат `summary/{id}.json`
```jsonc
{
 "id": "chui", "name": "Чуйская", "bbox": [42.2, 72.8, 43.3, 76.0],
 "data_until": "2025-12",                 // последний месяц в данных
 "current": {                             // последний месяц
   "month": "2025-12", "count": 2,        // очагов (гармонизированные, VIIRS-эквивалент)
   "median": 0,                           // норма = медиана этого месяца за прошлые годы
   "anomaly_pct": null                    // % к норме; null если норма < 3 (сравнивать не с чем)
 },
 "season": {
   "peak_month": 8, "peak_month_name": "август",
   "phase": "межсезонье",                 // "до пика" | "пик" | "спад" | "межсезонье"
   "months_to_peak": 8
 },
 "median_by_month": {"01": 0.0, "02": 0.5, "03": 195.5, ...},   // норма по месяцам
 "last_12_months": [{"month": "2025-01", "count": 3, "median": 0, "anomaly_pct": null}, ...],
 "yearly": {"2001": 1234, ...},           // очагов за год
 "yearly_median": 912, "worst_year": 2002,
 "site_url": "https://bakai4eg.github.io/fire-free-will/?bbox=42.2,72.8,43.3,76"  // ссылка «Открыть карту»
}
```

## Пример на Python
```python
import requests
API = "https://bakai4eg.github.io/fire-free-will/api/"
data = requests.get(API + "all.json", timeout=10).json()
for rid, r in data["regions"].items():
    c = r["current"]
    a = f"{c['anomaly_pct']:+d}%" if c["anomaly_pct"] is not None else "—"
    print(f"{r['name']}: {c['count']} очагов (норма {c['median']}, {a}), сезон: {r['season']['phase']}, пик в {r['season']['peak_month_name']}е")
```

## Что API НЕ даёт (делает человек A по BOT_SPEC.md)
- **Очаги за последние сутки** и оповещения — это FIRMS NRT API (нужен `FIRMS_MAP_KEY`).
- **Погоду и риск на сегодня** — Open-Meteo + формула риска.

API — это **история и норма**. Движок бота берёт норму отсюда, а свежие очаги и погоду — из NRT и Open-Meteo.
Когда подключим ежедневную загрузку NRT, `data_until` и `current` станут текущим месяцем автоматически, формат не изменится.

Области заданы в `data/regions.json` (приблизительные прямоугольники). Чтобы изменить или добавить область, правьте этот файл и запускайте `pipeline.py`.
