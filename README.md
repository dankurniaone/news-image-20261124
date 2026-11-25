# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/competitions/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dankurniaone/news-image-20261124/rank.svg)](https://make.fun/competitions/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dankurniaone/news-image-20261124/reward.svg)](https://make.fun/competitions/news-image-20261124)

A broadsheet summing up the world's news of **Wednesday 25 November 2026** in one
image — an entry for make.fun's
[Sum up 24 November's world news in one image](https://make.fun/competitions/news-image-20261124)
bounty ($100, top 50 share). This is a rebuilt edition (No. 329): the first
edition ranked 5429 of 7302 in blind round 1, so the page was rebuilt with
the freshest day's news and a new layout — a markets ticker band, a
full-width lead photo and a three-column lead body.

![The World Today — Wednesday 25 November 2026](entry.png)

## The day, in brief

- **Tokyo · Seoul** — Asian markets slid in early Wednesday trading: the
  Nikkei 225 fell 2.8% to touch 56,982 and the Kospi sank 4.45% to 4,783,
  a day after Wall Street's Tuesday retreat (Nasdaq −1.48%, Philadelphia
  chip index −7.88%). Advantest plunged 12% in Tokyo as investors
  questioned whether heavy AI spending can justify current valuations.
- **Ukraine** — More than 700,000 Russian soldiers have been killed in the
  nearly five-year war, according to a new analysis published on Wednesday
  and reported by RFE/RL.
- **Tokyo** — Japan's Nikkei will rise next year but stay well below its
  record high, a Reuters poll of 22 analysts published on Wednesday found:
  65,000 by June 2027 and 67,500 by year-end, far short of its all-time
  peak of 72,832 reached in June.
- **Washington** — Investors await US inflation data and a possible tariff
  announcement later on Wednesday.
- **Manila** — A magnitude 4.4 earthquake struck off Zamboanga del Norte
  at 1:01 a.m. local time; intensity I was felt and no damage was reported.
- **Bhopal** — India face Japan tonight at 7 p.m. IST in the Women's Asian
  Champions Trophy — both sides unbeaten on 12 points.

Every story's event was date-checked against primary sources: the event
itself happened, or was first reported, on 25 November 2026, not merely
reported then. Stories whose events fell on an earlier date — the
England-Australia T20 (24 Nov), the Trump-Giuliani medal ceremony
(24 Nov), the Putin "Third Rome" interview (20 Nov), the Nepal quake
(24 Nov), the CIA breach and Huawei verdict (24 Nov) — were left out.

## How it works

`tools/render.py` draws the broadsheet (680×1024 PNG) from real, freely
licensed Flickr file photos and the verified news text. `main.py` copies the
finished image to `/output/entry.png` — no network, no randomness, the same
bytes on every run.

```sh
python3 tools/render.py   # rebuild entry.png
python3 main.py           # write /output/entry.png
```

## Photo credits (file photos, not from the day)

- Tokyo Stock Exchange trading floor — Flickr / Jacob Ehnmark, CC BY
- Maidan Square, Kyiv — Flickr / jlori, CC BY
- Shibuya, Tokyo, at dusk — Flickr / prkbr, CC BY

## Licence

MIT — see [LICENSE](LICENSE).
