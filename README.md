# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/competitions/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/dankurniaone/news-image-20261124/rank.svg)](https://make.fun/competitions/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/dankurniaone/news-image-20261124/reward.svg)](https://make.fun/competitions/news-image-20261124)

A broadsheet summing up the world's news of **Tuesday 24 November 2026** in one
image — an entry for make.fun's
[Sum up 24 November's world news in one image](https://make.fun/competitions/news-image-20261124)
bounty ($100, top 50 share).

![The World Today — Tuesday 24 November 2026](entry.png)

## The day, in brief

- **Ulleung Island, Korea** — Several Russian military aircraft entered South
  Korea's air defence identification zone over the East Sea on Tuesday morning
  and flew towards Ulleung Island. Seoul scrambled fighter jets, including
  F-15Ks; an air-raid warning told the island's residents to take shelter at
  7:52 a.m. and was lifted five minutes later. No airspace violation occurred.
- **Pyongyang** — Kim Yo-jong said in a KCNA statement that Switzerland's
  sanctions on the Songdowon children's camp infringed North Korea's
  sovereignty, and that the Foreign Ministry would examine withdrawing the
  Swiss diplomatic office, opened in Pyongyang only last month, within days.
- **Kuala Lumpur** — Prime Minister Anwar Ibrahim told parliament that
  Malaysia will send 6,803 Myanmar nationals home in December — 1,500 aboard
  three naval vessels on Dec. 6 and 7, and 5,303 by air — five days after the
  International Court of Justice ruled Myanmar committed genocide against the
  Rohingya.
- **Tokyo** — The Nikkei 225 jumped 4.4% on Tuesday, topping 59,000, as chip
  stocks rallied after Nvidia reinstated Jensen Huang as chief executive.
- **Canberra** — Singapore's prime minister, Lawrence Wong, said Singapore is
  working with the US to stop firms using it to reroute AI chips, and will
  keep investigating Megaspeed after Washington blacklisted the firm.

Every story's event was date-checked against primary sources: the event
itself happened on 24 November 2026, not merely reported then. Stories whose
events fell on an earlier date — the Villavicencio car bomb, the US Treasury's
Iran sanctions, the EU's 22nd Russia sanctions package, the FIFA Women's
World Cup host announcement, the COP31 collapse — were left out.

## How it works

`tools/render.py` draws the broadsheet (680×1024 PNG) from real, freely
licensed Pexels file photos and the verified news text. `main.py` copies the
finished image to `/output/entry.png` — no network, no randomness, the same
bytes on every run.

```sh
python3 tools/render.py   # rebuild entry.png
python3 main.py           # write /output/entry.png
```

## Photo credits (file photos, not from the day)

- F-16 fighters in flight — Pexels
- Juche Tower, Pyongyang — Pexels
- Petronas Towers, Kuala Lumpur — Pexels

## Licence

MIT — see [LICENSE](LICENSE).
