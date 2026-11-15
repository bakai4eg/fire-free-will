# BurnBeat — речь и ответы жюри

## ⚠ Перед выходом исправить
- **Слайд 3: «×8.6 normal» устарело.** Сейчас сайт показывает для Кыргызстана **7.3×**. Открой сайт → Kyrgyzstan и скажи то число, которое там видно. Если спросят про расхождение: *"It's live, it changes every 3 hours. On the slide it was 8.6 this morning."*
- **Слайд 4, заметки: r = −0.45**, а в METHOD.md для всего Кыргызстана **−0.46**. Говори **"about minus 0.45"** — это честно.

---

## Речь по слайдам (~4 мин, простой английский)

**1 — BurnBeat**
Hi, we're team Blue Circle from Kyrgyzstan. This is BurnBeat.
NASA has 25 years of fire data from two satellites. We merged them into one record you can trust, and built a web app that shows if a place is burning more than usual — right now.

**2 — Problem**
The old sensor, MODIS, flies since 2000. The new one, VIIRS, since 2012. VIIRS sees several times more small fires.
If you just join the data, fire seems to jump in 2012. Look at the grey line — that's raw data for Kyrgyzstan. Nothing changed on the ground; only the camera changed.
And the data is huge: almost 15 million hotspots in 2025 alone. Nobody can check that by hand.

**3 — Solution**
So we converted 25 years of old MODIS data to the VIIRS scale. Now every place can be compared with its own history.
The answer is one line: for example, this week Kyrgyzstan is about [7] times its normal.
And it works: in Kyrgyzstan, the monthly error against real VIIRS falls from 79 to 27 hotspots.

**4 — How it works**
Four steps. One: we take hotspots from NASA FIRMS. Two: we rescale MODIS to VIIRS. Three: we check the result against real VIIRS. Four: we compare each place with its own median.
We also used NASA POWER rainfall — and found that wet months burn less.

**5 — Demo**
Let me show you. *[open site: search → this week vs normal → burning calendar → villages]*
Here is this week against normal, here is the burning calendar for 25 years, and here are the villages closest to fires.

**6 — Demo video** *(GIF plays — just comment)*
Here you see 25 years of fire on Earth, and then we zoom into Kyrgyzstan, Chui region: fresh fires from the last 7 days, the fire danger, and the nearest villages.

**7 — Impact** *(сценарии, ~50 сек)*
Who is it for? Let me give you three real scenarios.

**One — the emergency officer.** It's Monday morning in Chui region. The officer opens BurnBeat and sees: this week is seven times above normal, and here are the villages closest to the fires. Instead of waiting for calls, they send a patrol there today. And the burning calendar tells them in advance: March and August are the peaks, so plan your teams for those months.

**Two — the village head and the farmer.** Most fires in Kyrgyzstan are started by people burning fields. Every morning the village head gets a short Telegram message: "Danger high today: dry and windy." They tell the farmers: don't burn today, wait for rain. The cheapest fire to fight is the one that never starts.

**Three — the researcher or journalist.** They want to know: is Kyrgyzstan burning more than 20 years ago? With raw data the answer is a false "yes" — because of the new satellite. With BurnBeat they download one clean 25-year series as CSV and get the honest answer.

It works for any place on Earth, in Russian, Kyrgyz and English.
Next: launch the Telegram bot, validate beyond Kyrgyzstan, and add alerts.

**8 — Team**
We are six people: data, design, backend, frontend and validation. All data is from NASA FIRMS and NASA POWER.
BurnBeat — 25 years of NASA data, one clear answer: is it burning more than usual? Thank you!

---

## Откуда каждая цифра

| Цифра в презе | Откуда | Как получена |
|---|---|---|
| **25 years** | NASA FIRMS, MODIS с ноября 2000, VIIRS с 2012, по декабрь 2025 | Календарь 2001–2025 = 25 лет |
| **"several times more" (VIIRS vs MODIS)** | `web/data/meta.json` → `ratio_by_year` | Кыргызстан: VIIRS ÷ MODIS = от 2.7 до 5.3 в разные годы, обычно около 3–4× |
| **False jump in 2012** | Серая линия на слайде 2 = сырые данные | До 2012 у нас только MODIS, с 2012 — VIIRS. Мир: 4.4 → 17.4 млн в год (`web/data/global/summary.json`, поле `raw`) |
| **14.9 million hotspots in 2025** | `web/data/global/summary.json` → поле `harmonized`, сумма за 2025 | Ровно 14 907 462 очага на всей Земле за 2025 (то же число на сайте: «In 2025») |
| **×8.6 normal** (сейчас 7.3×) | Сайт, Kyrgyzstan, 15 ноября 2026 | Очаги NOAA-20 за последние 7 дней ÷ нормальная неделя. Нормальная неделя = медиана этого месяца за 2012–2025 × 7 / число дней в месяце |
| **79.1 → 27.5 hotspots/month** | `web/data/meta.json` → `validation`; таблица в `docs/METHOD.md` | Средняя ошибка за месяц (MAE). 79.1 — сырой MODIS, 27.5 — наша гармонизация |
| **bias −1.6%** (заметки слайда 4) | там же | Общая сумма предсказания отличается от реального VIIRS на −1.6%. Сырой MODIS: −72% |
| **r = −0.45** | `docs/METHOD.md`, раздел про погоду | Корреляция Пирсона, осадки NASA POWER ↔ очаги, 2012–2025, пиковые месяцы. Весь Кыргызстан −0.46, по областям от −0.35 до −0.44 |
| **6 people, RU/KY/EN** | Команда и сайт | — |

---

## Вопросы жюри и ответы

### Про метод

**Q: How exactly do you harmonize?**
> For every grid cell and every month, we divide VIIRS hotspots by MODIS hotspots over 2012–2016, when both satellites were flying. Then we multiply old MODIS data by this ratio. Where there's too little data, we use the regional ratio instead.

**Q: Why only 2012–2016 for fitting?**
> After 2016, the MODIS satellites slowly drifted in orbit and started seeing fewer fires. So the early years are the most similar to how MODIS worked in the 2000s.

**Q: How did you validate?**
> We hid one year at a time, from 2012 to 2019, predicted it from MODIS, and compared it with what VIIRS really saw. In Kyrgyzstan the monthly error dropped from 79 to 27 hotspots. Worldwide the total is off by only 0.3 percent, versus 75 percent for raw data.

**Q: What is MAE / bias?**
> MAE is how far off we are in an average month. Bias is whether we count too many or too few overall. Both are in hotspots, not temperature.

**Q: Why not machine learning?**
> A simple ratio is easy to explain and easy to check, and the validation shows it works. For a public tool, being transparent matters more than a black box.

**Q: Why convert MODIS to VIIRS and not the other way round?**
> VIIRS is the newer, sharper sensor, and it's the one NASA will keep flying. So we bring old data up to today's standard.

**Q: What about 2000–2002?**
> Until July 2002 only one MODIS satellite, Terra, was flying. We scale those months by how much Terra plus Aqua see compared with Terra alone. So 2001 is a rougher estimate, and we say that openly.

**Q: How do you remove factories and gas flares?**
> In the archive, NASA marks them as type 2 or 3, and we drop them. In live data, a place that "burns" five or more days out of seven is not a wildfire, so we remove it.

**Q: How sure are you about 2001–2011?**
> If we fit on all years instead of 2012–2016, old values change by about 10 percent. That's our uncertainty for that period, and it's written in our method.

### Про данные

**Q: Where does the data come from?**
> NASA FIRMS: MODIS and VIIRS archives for the history, and VIIRS NOAA-20 and 21 near-real-time files for the last 7 days. NASA POWER for rainfall. Open-Meteo for the weather forecast.

**Q: How often is it updated?**
> Our server downloads the latest NASA FIRMS data every 3 hours. The history up to 2025 was processed once.

**Q: Why does the history end in 2025?**
> The yearly NASA archive is published after the year ends. The current year is covered by the live layer — the last 7 days.

**Q: What resolution?**
> Kyrgyzstan: individual hotspots and 0.25 degree cells, about 25 kilometres. The rest of the world: 1 degree, about 100 kilometres.

### Про продукт

**Q: Is this a fire forecast?**
> No. The fire danger is a rating of conditions — season, unusual activity and weather. It says conditions are risky, not where a fire will start.

**Q: What does "×7 normal" mean?**
> This week we see seven times more hotspots than in a typical week of this month, based on 2012 to 2025.

**Q: What if the normal is close to zero?**
> Then a ratio would be misleading. If fewer than 3 fires a week are normal, we just say "unusual for the season" instead of a scary number.

**Q: Who will actually use it?**
> Emergency services, to see early if this week is unusual and plan patrols. Researchers, who get a clean 25-year series. And local communities and farmers, through a simple daily brief.

**Q: How is it different from NASA FIRMS?**
> FIRMS shows dots on a map. We answer a question: is this place burning more than usual? And we make 25 years comparable, which FIRMS doesn't do.

**Q: Is the Telegram bot working?**
> The bot is built and tested; it needs the final channel setup to launch. That's our first next step.

### Про технику

**Q: What's your stack?**
> Python processes the data. The web app is JavaScript with D3 for the map and ECharts for the charts. It runs on a Google Cloud server, with GitHub Pages as a backup.

**Q: Is it just an HTML page?**
> The front end is a static page on purpose. The heavy work — harmonizing 25 years — is done by our Python pipeline. The page just shows the results, so it loads in under a second and has nothing to break.

**Q: Can it scale?**
> Yes. It's static files, so any number of users is fine. The pipeline already runs for the whole planet.

### Про ИИ

**Q: How did you use AI?**
> Claude Code helped us write and debug the code, ChatGPT helped with wording. The team chose the problem, the method and the users, and checked every result. All data is real NASA data — nothing is generated by AI.

### Если не знаешь ответа
> Good question — we haven't tested that yet. It's on our list, and our full method is open in the repository.
