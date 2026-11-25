#!/usr/bin/env python3
"""Draw the 24 November 2026 front page: THE WORLD TODAY, 680x1024 PNG.

One day on one page. A markets ticker band up top, then the lead — the
Huawei verdict in Brooklyn — with a full-width file photo and a
two-column body, then two stories side by side (the Riyadh drone strike
and the AI sell-off in New York), a shaded strip of three briefs, and a
footer naming the sources. Everything is drawn with Pillow at double
resolution and shrunk with LANCZOS, so the type stays sharp when the
page is read at 300 pixels across.

The photographs are real freely licensed file photos (none taken on the
day); every story's event happened, or was first reported, on Tuesday
24 November 2026, checked against Reuters, CNN, the Wall Street
Journal, the US Department of Justice and AP. Run from the repo root:

    python3 tools/render.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCALE = 2                       # draw at double size, shrink at the end
W, H = 680 * SCALE, 1024 * SCALE
MARGIN = 28 * SCALE
TEXTW = W - 2 * MARGIN

PAPER = (246, 242, 231)
TINT = (233, 229, 218)
INK = (17, 17, 17)
RED = (164, 30, 34)
GREY = (90, 86, 78)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * SCALE)


def wrap(draw, text, face, width):
    """Greedy word wrap: lines that fit inside width, in order."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=face) <= width:
            line = trial
        elif line:
            lines.append(line)
            line = word
        else:
            lines.append(word)
            line = ""
    if line:
        lines.append(line)
    return lines


def cover(img, w, h, anchor=0.5):
    """Crop img to w:h (anchor picks the vertical band), then scale."""
    iw, ih = img.size
    want = w / h
    if iw / ih > want:
        keep = int(ih * want)
        img = img.crop(((iw - keep) // 2, 0, (iw - keep) // 2 + keep, ih))
    else:
        keep = int(iw / want)
        top = max(0, min(ih - keep, int((ih - keep) * anchor)))
        img = img.crop((0, top, iw, top + keep))
    return img.resize((w, h), Image.LANCZOS)


class Page:
    """One broadsheet page; y is the cursor, in scaled pixels."""

    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.y = 14 * SCALE

    def hline(self, weight=1, before=0, after=6):
        self.y += before * SCALE
        self.d.rectangle([MARGIN, self.y, MARGIN + TEXTW,
                          self.y + weight * SCALE], fill=INK)
        self.y += (weight + after) * SCALE

    def centre(self, text, face, fill=INK):
        wide = self.d.textlength(text, font=face)
        self.d.text(((W - wide) / 2, self.y), text, font=face, fill=fill)
        self.y += int(face.size * 1.55)

    def kicker(self, text, face, fill=RED, x=MARGIN):
        for ch in text:
            self.d.text((x, self.y), ch, font=face, fill=fill)
            x += self.d.textlength(ch, font=face) + 2
        self.y += int(face.size * 1.7)

    def para(self, text, face, width, x=MARGIN, fill=INK, leading=1.4):
        step = int(face.size * leading)
        for line in wrap(self.d, text, face, width):
            self.d.text((x, self.y), line, font=face, fill=fill)
            self.y += step

    def picture(self, path, width, height, anchor=0.5):
        shot = Image.open(path).convert("RGB")
        tall = height * SCALE
        self.img.paste(cover(shot, width, tall, anchor), (MARGIN, self.y))
        self.y += tall + 4 * SCALE

    def caption(self, text):
        self.d.text((MARGIN, self.y), text, font=font(SERIF_I, 11),
                    fill=GREY)
        self.y += int(11 * SCALE * 1.7) + 2 * SCALE

    def finish(self):
        small = self.img.resize((680, 1024), Image.LANCZOS)
        dest = os.path.join(ROOT, "entry.png")
        small.save(dest, "PNG")
        print("wrote entry.png", small.size, os.path.getsize(dest),
              "bytes; content ends at y =", self.y // SCALE, "logical")


# ---------------------------------------------------------------- the day
# Every item below is an event of Tuesday 24 November 2026, checked the
# same day against the primary reporting. Items whose events fell on
# another day were left out: Nvidia's reinstatement and 31.5% jump
# (Monday 23 Nov), the Shenzhou-24 launch (25 Nov Beijing time), the
# ICJ Myanmar ruling (19 Nov), the Villavicencio car bomb (23 Nov),
# the DR Congo plane (23 Nov), the Pentagon rebuke of Canada (23 Nov).

TICKER = ("NIKKEI +3.91%   ·   KOSPI +6%   ·   DOW +0.85%   ·   "
          "NASDAQ -1.48%   ·   S&P -0.50%   ·   NVIDIA -5.86%")

LEAD = {
    "kicker": "BROOKLYN · LAW",
    "head": "HUAWEI GUILTY ON 10 COUNTS",
    "deck": ("A federal jury convicts the Chinese telecom giant of stealing "
             "trade secrets, bank fraud and busting Iran sanctions — and "
             "clears it of racketeering."),
    "photo": os.path.join(ROOT, "assets", "huawei-store.jpg"),
    "anchor": 0.08,
    "caption": ("A Huawei store in Shenzhen. (File photo: Wikimedia "
                "Commons / HOISAIWIM TUNGWAH, CC0)"),
    "body": ("A federal jury in Brooklyn convicted Huawei and three "
             "subsidiaries on ten of twelve counts on Tuesday, ending a "
             "case that began in 2018: conspiracy to steal trade secrets, "
             "bank fraud, wire fraud, sanctions violations over Iran and "
             "money laundering. The jury cleared the company of "
             "racketeering conspiracy and conspiracy to obstruct justice. "
             "Prosecutors told the court Huawei stole source code from "
             "Cisco, antenna technology from Quintel and robot technology "
             "from T-Mobile, and more than sixty witnesses testified "
             "across a trial of two to three months. Sentencing is set for "
             "14 September 2027, and Huawei says it will appeal."),
}

LEFT = {
    "kicker": "RIYADH · SECURITY",
    "head": "DRONE HITS RIYADH PIF TOWER, 11 WOUNDED",
    "photo": os.path.join(ROOT, "assets", "riyadh-kafd.jpg"),
    "anchor": 0.6,
    "caption": ("KAFD, Riyadh. (Wikimedia Commons / B.alotaby)"),
    "body": ("A drone attack struck the Public Investment Fund tower in "
             "Riyadh's King Abdullah Financial District on Tuesday, "
             "wounding eleven people — two Saudis, two Indians, three "
             "Nepalis and four Egyptians. It was the second strike on the "
             "capital in under a week, in a campaign the Houthis have "
             "claimed."),
}

RIGHT = {
    "kicker": "NEW YORK · MARKETS",
    "head": "AI RALLY FIZZLES IN A DAY",
    "photo": os.path.join(ROOT, "assets", "nyse.jpg"),
    "anchor": 0.5,
    "caption": ("The New York Stock Exchange. (Kidfly182, CC BY)"),
    "body": ("A day after Nvidia's shares jumped 31.5 per cent on its "
             "founder's return, the chipmaker fell 5.86 per cent on "
             "Tuesday and the Nasdaq slid 1.48 per cent. The Philadelphia "
             "chip index dropped 7.88 per cent; Micron fell 10.97 per "
             "cent and Analog Devices 17.4 per cent. The Dow rose 0.85 "
             "per cent to 50,018 as money rotated to value, the S&P 500 "
             "slipped 0.50 per cent, Anthropic fell below its $83 listing "
             "price, and the Trump administration is said to be readying "
             "fresh tariffs on China and the EU."),
}

BRIEFS = [
    ("HORMUZ",
     "Iran said four tankers were hit by mines in the Strait of Hormuz; "
     "the reports were unconfirmed, and its navy said it had targeted a "
     "container ship there."),
    ("CARTAGENA",
     "Armed men held 25 hostages at a supermarket in Cartagena; five "
     "older women were released and the airport briefly suspended "
     "landings."),
    ("GULF OF FINLAND",
     "Ukraine hit the Russian cargo ship Sparta II with a drone in the "
     "Gulf of Finland; its 16 crew were evacuated. Kyiv also claimed a "
     "corvette sunk off Libya."),
]

FOOT_A = ("All events here happened, or were first reported, on Tuesday "
          "24 November 2026. Sources: Reuters; CNN; The Wall Street "
          "Journal; US Department of Justice; AP.")
FOOT_B = ("Photos are freely licensed file photos, not from the day: "
          "Huawei store, Shenzhen (Wikimedia Commons / HOISAIWIM "
          "TUNGWAH, CC0); King Abdullah Financial District, Riyadh "
          "(Wikimedia Commons / B.alotaby); New York Stock Exchange "
          "(Wikimedia Commons / Kidfly182, CC BY).")


def masthead(p):
    p.centre("THE WORLD TODAY", font(SERIF_B, 36))
    p.y -= int(36 * SCALE * 0.35)
    p.centre("TUESDAY, 24 NOVEMBER 2026", font(SANS_B, 14))
    p.centre("ONE DAY  ·  ONE PAGE  ·  No. 329", font(SANS, 11), fill=GREY)
    p.y += 4 * SCALE
    p.d.rectangle([MARGIN, p.y, MARGIN + TEXTW, p.y + 3 * SCALE], fill=INK)
    p.y += 8 * SCALE
    p.hline(weight=1, after=8)


def ticker(p):
    size = 12
    face = font(SANS_B, size)
    while p.d.textlength(TICKER, font=face) > TEXTW - 16 * SCALE and size > 9:
        size -= 1
        face = font(SANS_B, size)
    tall = 26 * SCALE
    p.d.rectangle([MARGIN, p.y, MARGIN + TEXTW, p.y + tall], fill=INK)
    wide = p.d.textlength(TICKER, font=face)
    p.d.text((MARGIN + (TEXTW - wide) // 2,
              p.y + (tall - face.size) // 2 - 2 * SCALE),
             TICKER, font=face, fill=PAPER)
    p.y += tall + 6 * SCALE


def lead(p):
    p.kicker(LEAD["kicker"], font(SANS_B, 13))
    head = font(SERIF_B, 33)
    for line in wrap(p.d, LEAD["head"], head, TEXTW):
        p.d.text((MARGIN, p.y), line, font=head, fill=INK)
        p.y += int(33 * SCALE * 1.12)
    p.y += 2 * SCALE
    p.para(LEAD["deck"], font(SERIF, 14), TEXTW, leading=1.45)
    p.y += 4 * SCALE
    p.picture(LEAD["photo"], TEXTW, 120, anchor=LEAD["anchor"])
    p.caption(LEAD["caption"])
    # Two-column body: wrap the whole text to one column, then split.
    body = font(SERIF, 13)
    gap = 16 * SCALE
    col = (TEXTW - gap) // 2
    lines = wrap(p.d, LEAD["body"], body, col)
    half = (len(lines) + 1) // 2
    step = int(13 * SCALE * 1.5)
    top = p.y
    bottom = top
    for c in range(2):
        yy = top
        for line in lines[c * half:(c + 1) * half]:
            p.d.text((MARGIN + c * (col + gap), yy), line, font=body,
                     fill=INK)
            yy += step
        bottom = max(bottom, yy)
    p.y = bottom + 4 * SCALE
    p.hline(weight=1, after=6)


def story(p, x, width, item, photo_h):
    start = p.y
    p.kicker(item["kicker"], font(SANS_B, 13), x=x)
    head = font(SERIF_B, 21)
    for line in wrap(p.d, item["head"], head, width):
        p.d.text((x, p.y), line, font=head, fill=INK)
        p.y += int(21 * SCALE * 1.12)
    p.y += 3 * SCALE
    shot = Image.open(item["photo"]).convert("RGB")
    tall = photo_h * SCALE
    p.img.paste(cover(shot, width, tall, item["anchor"]), (x, p.y))
    p.y += tall + 4 * SCALE
    p.d.text((x, p.y), item["caption"], font=font(SERIF_I, 11), fill=GREY)
    p.y += int(11 * SCALE * 1.7) + 2 * SCALE
    p.para(item["body"], font(SERIF, 12.5), width, x=x, leading=1.45)
    return p.y


def middle(p):
    start = p.y
    gap = 20 * SCALE
    half = (TEXTW - gap) // 2
    end_l = story(p, MARGIN, half, LEFT, 54)
    p.y = start
    end_r = story(p, MARGIN + half + gap, half, RIGHT, 54)
    p.y = max(end_l, end_r)
    split = MARGIN + half + gap // 2
    p.d.rectangle([split, start, split + 1 * SCALE, p.y - 4 * SCALE],
                  fill=INK)
    p.y += 4 * SCALE
    p.hline(weight=1, after=6)


def briefs(p):
    head = font(SANS_B, 12)
    body = font(SERIF, 12.5)
    count = len(BRIEFS)
    gap = 16 * SCALE
    cell = (TEXTW - (count - 1) * gap) // count
    fitted = []
    most = 0
    for place, text in BRIEFS:
        lines = wrap(p.d, text, body, cell)
        fitted.append((place, lines))
        most = max(most, len(lines))
    box = (int(13 * SCALE * 1.7) + int(12 * SCALE * 1.7)
           + most * int(12.5 * SCALE * 1.45) + 8 * SCALE)
    top = p.y
    p.d.rectangle([MARGIN, top, MARGIN + TEXTW, top + box], fill=TINT)
    p.y = top + 7 * SCALE
    p.kicker("THE DAY IN BRIEF", font(SANS_B, 13), fill=INK)
    p.y -= int(13 * SCALE * 0.35)
    for i, (place, lines) in enumerate(fitted):
        bx = MARGIN + 10 * SCALE + i * (cell + gap)
        p.d.text((bx, p.y), place, font=head, fill=RED)
        yy = p.y + int(12 * SCALE * 1.7)
        step = int(12.5 * SCALE * 1.45)
        for line in lines:
            p.d.text((bx, yy), line, font=body, fill=INK)
            yy += step
    p.y = top + box + 6 * SCALE
    p.hline(weight=1, after=4)


def footer(p):
    foot = font(SANS, 8)
    p.para(FOOT_A, foot, TEXTW, fill=GREY, leading=1.55)
    p.y += 2 * SCALE
    p.para(FOOT_B, foot, TEXTW, fill=GREY, leading=1.55)


def main():
    p = Page()
    masthead(p)
    ticker(p)
    lead(p)
    middle(p)
    briefs(p)
    footer(p)
    p.finish()


if __name__ == "__main__":
    main()
