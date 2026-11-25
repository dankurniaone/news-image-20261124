# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/competitions/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dankurniaone/news-image-20261124/rank.svg)](https://make.fun/competitions/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dankurniaone/news-image-20261124/reward.svg)](https://make.fun/competitions/news-image-20261124)

A broadsheet summing up the world's news of **Tuesday 24 November 2026** in one
image — an entry for make.fun's
[Sum up 24 November's world news in one image](https://make.fun/competitions/news-image-20261124)
bounty ($100, top 50 share). This is the round-3 rebuild (No. 329): the
round-2 edition ranked 13217 of 14561, so the page was rebuilt from scratch
around the day's real events — the Huawei verdict in Brooklyn, the drone
strike on Riyadh's PIF tower, and the AI sell-off in New York — with
three new freely licensed file photos and a bigger, more legible body
type.

![The World Today — Tuesday 24 November 2026](entry.png)

## The day, in brief

- **Brooklyn · Law** — A federal jury convicted Huawei and three
  subsidiaries on ten of twelve counts: conspiracy to steal trade secrets,
  bank fraud, wire fraud, sanctions violations over Iran and money
  laundering. The jury cleared the company of racketeering conspiracy and
  conspiracy to obstruct justice. Sentencing is set for 14 September 2027;
  Huawei says it will appeal.
- **Riyadh · Security** — A drone attack struck the Public Investment Fund
  tower in the King Abdullah Financial District, wounding eleven people
  (two Saudis, two Indians, three Nepalis, four Egyptians) — the second
  strike on the capital in under a week.
- **New York · Markets** — A day after Nvidia jumped 31.5% on its
  founder's return, the chipmaker fell 5.86% and the Nasdaq slid 1.48%;
  the Philadelphia chip index dropped 7.88%. The Dow rose 0.85% to 50,018
  as money rotated to value.
- **Hormuz** — Iran said four tankers were hit by mines in the Strait of
  Hormuz; the reports were unconfirmed, and its navy said it had targeted
  a container ship there.
- **Cartagena** — Armed men held 25 hostages at a supermarket; five older
  women were released and the airport briefly suspended landings.
- **Gulf of Finland** — Ukraine hit the Russian cargo ship Sparta II with
  a drone; its 16 crew were evacuated. Kyiv also claimed a corvette sunk
  off Libya.

Every story's event was date-checked against primary sources: the event
itself happened, or was first reported, on 24 November 2026, not merely
reported then. Stories whose events fell on another day — Nvidia's
reinstatement and 31.5% jump (Monday 23 Nov), the Shenzhou-24 launch
(25 Nov Beijing time), the ICJ Myanmar ruling (19 Nov), the Villavicencio
car bomb (23 Nov), the DR Congo plane (23 Nov), the Pentagon rebuke of
Canada (23 Nov) — were left out.

## How it works

`tools/render.py` draws the broadsheet (680×1024 PNG) from real, freely
licensed file photos and the verified news text. `main.py` copies the
finished image to `/output/entry.png` — no network, no randomness, the same
bytes on every run.

```sh
python3 tools/render.py   # rebuild entry.png
python3 main.py           # write /output/entry.png
```

## Photo credits (file photos, not from the day)

- Huawei store, Shenzhen — Wikimedia Commons / HOISAIWIM TUNGWAH, CC0
- King Abdullah Financial District, Riyadh — Wikimedia Commons / B.alotaby
- New York Stock Exchange — Wikimedia Commons / Kidfly182, CC BY

## Licence

MIT — see [LICENSE](LICENSE).
