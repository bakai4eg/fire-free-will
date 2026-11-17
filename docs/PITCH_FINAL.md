# BurnBeat — финальная речь + шпора

## 🆕 ДЛЯ ФИНАЛА: что сделали после полуфинала (вставить в слайд 7, ~25 сек)
> "Since the semifinal, we did every 'next step' we promised.
> **One:** we validated the method in ten countries — from Kazakhstan to Spain and Chile. Everywhere, raw data undercounts by 63 to 79 percent; after BurnBeat the error is within 4 percent, and the monthly error is about five times smaller.
> **Two:** the Telegram bot now sends an alert when a region burns at least twice its normal week. Tonight it flagged Chui region: many times above a normal November week.
> **Three:** the app works on phones and opens in English for any visitor."

Шпора по новым цифрам:
- **10 стран:** Казахстан, Турция, Чили, Монголия, Испания, Узбекистан, Португалия, Греция, Кыргызстан, Таджикистан.
- **Сырой MODIS:** промах −63…−79%. **После гармонизации:** в пределах ±3.6%.
- **Ошибка за месяц:** в 2–13 раз меньше, медиана ≈5×. Лучший результат у Казахстана: 7038 → 558, в 12.6 раза.
- **Если спросят, где хуже всего:** *"Small countries like Tajikistan: only 2× better, because there are very few fires to learn from."*
- **Если спросят про Украину и Непал:** *"The NASA download timed out tonight — they're next."*
- **Алерт бота:** ≥5 очагов за 7 дней И ≥2× нормальной недели. Повтор не чаще раза в 3 дня.
- **Ссылка для жюри на английском:** https://bakai4eg.github.io/fire-free-will/?lang=en

## КРЕАТИВНАЯ РЕЧЬ (~4–5 мин)

**1 — BurnBeat** *(пауза, потом медленно)*
In 2012, the world caught fire.
Overnight, the number of fires on Earth jumped four times — from 4 million a year to 17 million.
*(pause)*
Except… it didn't. Nothing burned. NASA just got new glasses.
We're team Blue Circle from Kyrgyzstan, and this is BurnBeat — the heartbeat of fire on our planet.

**2 — Problem**
Imagine you measure your child's height every year. Then one day you buy a new ruler — and suddenly your child is four times taller.
That's what happened with NASA fire data. The old satellite, MODIS, has watched fires since 2000. The new one, VIIRS, since 2012 — and it sees three to five times more small fires.
So 25 years of priceless data have a broken ruler in the middle. *(show grey line)* A fire chief who asks, "Is this year worse than before?" gets the wrong answer. And with 15 million hotspots a year, nobody can fix that by hand.

**3 — Solution**
So we fixed the ruler.
For every place on Earth and every month, we measured how much more the new satellite sees, and we brought 25 years of old data to the same scale.
Then we tried to break it. We hid a year, predicted it, and compared it with reality — eight times. The result: on the whole planet, we're off by 0.3 percent. Without us — 75 percent.
And now we can answer one simple question. *(pause)* Right now, this week, Kyrgyzstan is burning [7] times more than a normal November. That number is live — it was updated a few hours ago, from space.

**4 — How it works**
Every three hours, our server asks NASA one question: "What's burning on Earth?" It gets every fire seen in the last seven days. We remove factories and gas flares — if something "burns" five days in a row, it's a chimney, not a wildfire. Then we compare each place with its own normal, its typical year.
And we added rain from NASA POWER. The data says what every grandmother in Kyrgyzstan already knows: when it rains, it doesn't burn. *(smile)* Now it's proven: correlation minus 0.45.

**5 — Demo** *(на сайте)*
Let me show you. *(press play)*
This is 25 years of Earth's fire, in 20 seconds. Watch Africa — it breathes: north, then south, every year. That's the beat in BurnBeat.
Now let's fly home. *(search Chui)* Chui region. This week: [25] fires. Here is the danger for the next three days. Here is the burning calendar — every row a year, every square a month: spring and August, the two seasons when farmers burn fields. And here — the villages closest to the fire.

**6 — Demo video** *(GIF — молчи 3 секунды, дай посмотреть, потом одна фраза)*
From the whole planet to one village — in one click.

**7 — Impact**
Who is it for? Meet three people.
**Azamat, an emergency officer in Chui.** Monday morning. BurnBeat tells him: seven times above normal, here are the villages. He sends a team today — not after the calls.
**Gulnara, a village head.** Every morning her phone says: "Danger high today: dry and windy." She tells the farmers: don't burn today. Because the cheapest fire to fight is the one that never starts.
**And a journalist** who asks: is Kyrgyzstan burning more than twenty years ago? Raw data says "yes". BurnBeat says the truth.

**8 — Team / Final**
We are six people from Kyrgyzstan — a country where fire season smells like smoke over every village in autumn.
We took 25 years of NASA data, fixed the broken ruler, and turned it into one clear answer for any place on Earth: is it burning more than usual?
BurnBeat. Listen to the beat — before it becomes a fire.
Thank you!

---

## ПОДРОБНАЯ РЕЧЬ (~6–7 мин)

**1 — BurnBeat**
Hi everyone, we're team Blue Circle from Kyrgyzstan, and this is BurnBeat.
Every year, wildfires burn forests, fields and pastures, and people have to decide: is this season normal, or is something going wrong? NASA satellites have been watching fires from space for 25 years. That's a huge amount of knowledge. But today it's very hard to use, and we'll show you why.
BurnBeat merges 25 years of NASA fire data into one record you can trust, and turns it into a simple answer for any place on Earth: is it burning more than usual right now?

**2 — Problem**
NASA watches fires with two generations of satellites.
The first one is MODIS. It has been flying since 2000. The second one is VIIRS, since 2012. VIIRS has a much sharper camera, so it sees three to five times more small fires — like burning fields or grass.
And here is the problem. If you simply put the two records together, it looks like the world suddenly caught fire in 2012. On the planet, the number of hotspots jumps from 4.4 to 17.4 million a year. You can see the same thing for Kyrgyzstan here — the grey line jumps up in 2012.
But nothing happened on the ground. Only the camera changed.
So if a fire manager asks, "Is this year worse than ten years ago?", the raw data gives the wrong answer. And the data is too big to check by hand: almost 15 million hotspots on Earth in 2025 alone.

**3 — Solution**
Our solution is to put both satellites on one scale.
We convert all the old MODIS years to the VIIRS scale. After that, 25 years can be compared fairly, and every place can be compared with its own history.
This lets us give a one-line answer. For example, today: this week Kyrgyzstan has about [7] times more fires than a normal week in November.
And we didn't just assume it works — we tested it. In Kyrgyzstan, the average monthly error against real VIIRS data falls from 79 hotspots to 27. For the whole planet, the total is off by only 0.3 percent, while raw data is off by 75 percent.

**4 — How it works**
Let me explain how, in four simple steps.
Step one: we take all hotspots from NASA FIRMS — the MODIS and VIIRS archives from 2000 to 2025. We keep only real vegetation fires and remove factories, gas flares and volcanoes.
Step two: from 2012 to 2016, both satellites were flying at the same time. So for every place and every month, we count how many times more fires VIIRS sees than MODIS. Then we multiply the old MODIS data by that number. Where there's too little data, we use the number for the whole region. We use 2012 to 2016 because later, the MODIS satellites slowly drifted in orbit and started to see less.
Step three: we check it. We hide one year, predict it from MODIS, and compare it with what VIIRS really saw. We repeat this for eight years, 2012 to 2019. That's where the numbers you saw come from.
Step four: we compare each place with its own normal — the median, the typical year. For "right now", our server downloads fresh NASA data every three hours: all fires on Earth from the last seven days. We count them in the chosen place and compare them with a normal week.
We also added rainfall from NASA POWER, and found a clear pattern: in every Kyrgyz region, rainy months burn less.

**5 — Demo** *(на сайте)*
Now let me show you the tool.
I search for a place — for example, Kyrgyzstan, Chui region. At the top you see the main answer: how many fires this week, and how that compares with normal.
Below is the fire danger for today and the next three days. It combines the season, how unusual this week is, and the weather forecast — heat, dry air, wind and rain. It's not a fire forecast; it's a rating of conditions, and we always show the reasons.
Here is the burning calendar: every row is a year, every square is a month. You can see that Chui burns in spring and in August — that's when farmers burn their fields.
And here is the list of villages closest to fresh fires, so services know where to go.

**6 — Demo video** *(GIF)*
Here you can see it in motion. First, 25 years of fire on Earth, month by month — Africa's fire belt, the Amazon, Australia. You can literally see the seasons. Then we zoom into Kyrgyzstan, Chui region: fresh fires from the last seven days, the fire danger, and the nearest villages.

**7 — Impact**
So who is it for? Let me give you three real scenarios.
**One — the emergency officer.** It's Monday morning in Chui region. The officer opens BurnBeat and sees: this week is seven times above normal, and here are the villages closest to the fires. Instead of waiting for calls, they send a patrol there today. And the burning calendar tells them in advance that March and August are the peaks, so they can plan teams and equipment for those months.
**Two — the village head and the farmer.** In Kyrgyzstan, most fires are started by people burning fields. Every morning the village head gets a short Telegram message: "Fire danger is high today: dry and windy." They tell the farmers: don't burn today, wait for rain. We don't only help the people who put fires out — we help the people who start them. The cheapest fire to fight is the one that never starts.
**Three — the researcher or journalist.** They want to know: is Kyrgyzstan burning more than twenty years ago? With raw data, the answer is a false "yes", only because of the new satellite. With BurnBeat, they download one clean 25-year series as a CSV file and get the honest answer.
BurnBeat works for any place on Earth, and it speaks Russian, Kyrgyz and English.

**Next steps**
We are honest about our limits. Outside Kyrgyzstan our grid is about 100 kilometres, and 2001 was seen by only one MODIS satellite, so it's a rougher estimate.
Next, we want to launch the Telegram bot, validate the method in more countries, add alerts when a place goes above normal, and start a pilot with the emergency services of Kyrgyzstan.

**8 — Team**
We are six people: a team lead, a data analyst, a designer, backend and frontend developers, and a validation and bot engineer. Everything is built on open NASA data — FIRMS for fires and POWER for weather.
BurnBeat: 25 years of NASA data, one clear answer — is it burning more than usual?
Thank you!

---

## РЕЧЬ (~4 мин)

**1 — BurnBeat**
Hi, we're team Blue Circle from Kyrgyzstan. This is BurnBeat.
NASA has 25 years of fire data from two satellites. We merged them into one record you can trust, and built a web app that shows if a place is burning more than usual — right now.

**2 — Problem**
The old sensor, MODIS, flies since 2000. The new one, VIIRS, since 2012. VIIRS sees three to five times more small fires.
If you just join the data, fire seems to jump in 2012 — that's the grey line. Nothing changed on the ground; only the camera changed.
And the data is huge: almost 15 million hotspots in 2025 alone. Nobody can check that by hand.

**3 — Solution**
So we converted 25 years of old MODIS data to the VIIRS scale. Now every place can be compared with its own history.
The answer is one line: this week Kyrgyzstan is about [7] times its normal.
And it works: the monthly error against real VIIRS falls from 79 to 27 hotspots.

**4 — How it works**
Four steps. One: hotspots from NASA FIRMS. Two: we rescale MODIS to VIIRS — for every place and every month, using the years when both satellites flew. Three: we check it against real VIIRS. Four: we compare each place with its own median.
We also used NASA POWER rainfall — wet months burn less.

**5 — Demo** *(на сайте: поиск → неделя vs норма → календарь → сёла)*
Here is this week against normal. Here is the burning calendar for 25 years. And here are the villages closest to the fires.

**6 — Demo video** *(GIF)*
25 years of fire on Earth — and then Kyrgyzstan, Chui region: fresh fires from the last 7 days, fire danger, and the nearest villages.

**7 — Impact**
Who is it for? Three real scenarios.
**One — the emergency officer.** Monday morning, Chui region. BurnBeat shows: this week is seven times above normal, and here are the villages closest to the fires. They send a patrol today, not after the calls. And the calendar says March and August are the peaks — so plan teams for those months.
**Two — the village head and the farmer.** Most fires here are started by people burning fields. Every morning the village head gets a Telegram message: "Danger high today: dry and windy." They tell the farmers: don't burn today. The cheapest fire to fight is the one that never starts.
**Three — the researcher or journalist.** Is Kyrgyzstan burning more than 20 years ago? Raw data gives a false "yes", because of the new satellite. BurnBeat gives one clean 25-year series and the honest answer.
It works for any place on Earth, in Russian, Kyrgyz and English. Next: launch the Telegram bot, validate beyond Kyrgyzstan, add alerts.

**8 — Team**
We are six people: data, design, backend, frontend and validation. All data is from NASA FIRMS and NASA POWER.
BurnBeat — 25 years of NASA data, one clear answer: is it burning more than usual? Thank you!

---

## ТУПАЯ ШПОРА

### Суть в 1 фразу
**Два спутника видят пожары по-разному → мы привели их к одной шкале → теперь видно, горит ли сейчас больше обычного.**

### Спутники
- **MODIS** = старый, с 2000. Видит меньше.
- **VIIRS** = новый, с 2012. Видит в **3–5 раз больше** мелких пожаров.
- Склеить как есть → фейковый скачок в 2012 (мир: **4.4 → 17.4 млн** в год).

### Гармонизация = одно умножение
- Для каждой клетки и месяца: **VIIRS ÷ MODIS** за **2012–2016** (оба летали).
- Старые данные **× это число** = гармонизированные.
- Мало данных в клетке → берём число региона.
- Почему 2012–2016: потом орбиты MODIS «поплыли».
- 2000–2002 летал 1 спутник MODIS → домножаем ещё (~×2.2).

### Проверка
- Прячем 1 год (2012–2019), предсказываем, сравниваем с реальным VIIRS.
- **Кыргызстан:** ошибка/месяц **79 → 27** очагов, общий промах **−1.6%** (сырой: −72%).
- **Мир:** промах **−0.3%** (сырой: **−75%**), ошибка **в 19 раз меньше**.
- Это **количество очагов**, НЕ температура.

### «Сейчас vs норма»
- Сервер **каждые 3 ч** качает NASA FIRMS: все очаги Земли **за 7 дней** (VIIRS NOAA-20/21).
- Сейчас = очаги за 7 дней в выбранном месте.
- Норма = **медиана** этого месяца за **2012–2025** × 7 / дней в месяце.
- Сейчас ÷ норма = **«×7»**.
- Норма < 3/неделю → пишем «необычно для сезона», без страшных цифр.
- Заводы/факелы убираем: горит ≥5 дней из 7 = не пожар.

### Две медианы
- **Live:** медиана 2012–2025 (только VIIRS).
- **История/календарь:** медиана 2002–2025 по гармонизированным → тут гармонизация решает.

### Опасность на 3 дня
- Сезон + аномалия + свежие очаги + погода (жара, сухо, ветер, нет дождя).
- **НЕ прогноз пожара**, а оценка условий.

### Цифры и откуда
| Цифра | Откуда |
|---|---|
| 25 лет | FIRMS, 2001–2025 |
| 3–5× | `meta.json` ratio_by_year (2.7–5.3) |
| 14.9 млн (2025) | `global/summary.json`, на сайте «In 2025» |
| ×7 (было 8.6) | сайт, живое, меняется каждые 3 ч |
| 79 → 27, −1.6% | `meta.json` validation, METHOD.md |
| −0.3%, 19× | METHOD.md, мир |
| r ≈ −0.45 | осадки NASA POWER ↔ очаги, 2012–2025 |

### Данные
NASA FIRMS (пожары) · NASA POWER (осадки) · Open-Meteo (прогноз) · GeoNames (сёла) · geoBoundaries (границы областей)

### Стек
Python (обработка) · JavaScript + D3 (карта) + ECharts (графики) · Google Cloud + Caddy · GitHub Pages (запасной) · бот: aiogram

### Анимация
Не видео. Заранее посчитали клетки 1° × 300 месяцев → браузер рисует месяц за месяцем на canvas + blur = свечение.

### Детализация
Кыргызстан: точки + 25 км. Мир: ~100 км.

### Ограничения (говорить честно)
- Мир грубый (~100 км).
- 2001 — грубая оценка.
- 2001–2011 ±10%.
- Опасность ≠ прогноз.
- Бот готов, ещё не запущен.

### ИИ
Claude Code — код. ChatGPT — формулировки. Решения и проверка — команда. Данные — только NASA, ничего не сгенерировано.

### Палочки-выручалочки
- **Не знаю:** *"Good question — we haven't tested that yet. Our full method is open in the repository."*
- **Не прогноз?** *"It's a rating of conditions, not a fire forecast."*
- **Просто HTML?** *"The heavy work is in the Python pipeline; the page just shows results — fast and nothing to break."*
- **Говорили с МЧС?** *"Not yet — a pilot is our first next step."*
- **Почему не ML?** *"A simple ratio is transparent and validated. For a public tool, clear beats black box."*
