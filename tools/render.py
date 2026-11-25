#!/usr/bin/env python3
"""Build the 25 November 2026 front page as a 680x1024 PNG.

THE WORLD TODAY, one day on one page: a markets ticker band, a lead on
Asia's Wednesday slide with a full-width photo and a three-column body,
two stories below it (the war's toll, the Nikkei poll), a shaded strip of
three briefs, and a footer naming the sources. Everything is drawn with
Pillow at double size and shrunk with LANCZOS, so the small type stays
sharp when the page is read at 300 pixels across.

The photographs are real freely licensed file photos (none taken today);
the words are the day's verified news. Run from the repository root:

    python3 tools/render.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SS = 2                       # supersample factor
PAGE = (680 * SS, 1024 * SS)
SIDE = 28 * SS               # side margin
INNER = PAGE[0] - 2 * SIDE   # text width

NEWS_PRINT = (246, 242, 231)
SHADE = (233, 229, 218)
BLACK = (17, 17, 17)
SIGNAL = (164, 30, 34)
MUTED = (90, 86, 78)

F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def face(path, pts):
    return ImageFont.truetype(path, pts * SS)


def fit_lines(draw, text, font, width):
    """Split text into lines no wider than width (greedy, word by word)."""
    out, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def fill_frame(img, target_w, target_h, anchor=0.5):
    """Crop img to the target aspect (anchored vertically), then scale it."""
    iw, ih = img.size
    want = target_w / target_h
    have = iw / ih
    if have > want:
        keep = int(ih * want)
        left = (iw - keep) // 2
        img = img.crop((left, 0, left + keep, ih))
    else:
        keep = int(iw / want)
        top = max(0, min(ih - keep, int((ih - keep) * anchor)))
        img = img.crop((0, top, iw, top + keep))
    return img.resize((target_w, target_h), Image.LANCZOS)


class Sheet:
    """A broadsheet page with a vertical cursor and drawing helpers."""

    def __init__(self):
        self.img = Image.new("RGB", PAGE, NEWS_PRINT)
        self.d = ImageDraw.Draw(self.img)
        self.y = 16 * SS

    def rule(self, weight=1, gap=6):
        self.d.rectangle([SIDE, self.y, SIDE + INNER, self.y + weight * SS],
                         fill=BLACK)
        self.y += (weight + gap) * SS

    def heavy_rule(self):
        self.d.rectangle([SIDE, self.y, SIDE + INNER, self.y + 3 * SS],
                         fill=BLACK)
        self.y += 8 * SS

    def centred(self, text, font, fill=BLACK):
        wide = self.d.textlength(text, font=font)
        self.d.text(((PAGE[0] - wide) / 2, self.y), text, font=font, fill=fill)
        self.y += int(font.size * 1.6)

    def spaced(self, text, font, fill, step=2):
        """A kicker line with widened letter spacing."""
        cx = SIDE
        for ch in text:
            self.d.text((cx, self.y), ch, font=font, fill=fill)
            cx += self.d.textlength(ch, font=font) + step
        self.y += int(font.size * 1.7)

    def block(self, text, font, width, x=SIDE, fill=BLACK, leading=1.35):
        """A wrapped paragraph; returns nothing, advances the cursor."""
        lh = int(font.size * leading)
        for line in fit_lines(self.d, text, font, width):
            self.d.text((x, self.y), line, font=font, fill=fill)
            self.y += lh

    def photo(self, path, width, height_pts, anchor=0.5):
        shot = Image.open(path).convert("RGB")
        tall = height_pts * SS
        self.img.paste(fill_frame(shot, width, tall, anchor), (SIDE, self.y))
        self.y += tall + 4 * SS

    def save(self):
        final = self.img.resize((680, 1024), Image.LANCZOS)
        dest = os.path.join(REPO, "entry.png")
        final.save(dest, "PNG")
        print("wrote entry.png", final.size,
              os.path.getsize(dest), "bytes,",
              "content ends at y =", self.y // SS, "(logical)")


# ------------------------------------------------------------------ the day
# Every item below is an event of Wednesday 25 November 2026, checked the
# same day against the primary reporting: the Wall Street Journal and
# JBizNews on the morning markets, RFE/RL on the new casualty analysis,
# Reuters on its Nikkei poll, PHIVOLCS on the quake, Hockey India on the
# hockey fixture. Items whose events fell earlier — the England-Australia
# T20 (24 Nov), the Trump-Giuliani medal ceremony (24 Nov), the Putin
# "Third Rome" interview (20 Nov), the Nepal quake (24 Nov), the CIA
# breach and Huawei verdict (24 Nov) — were left out.
TICKER = ("MARKETS   NIKKEI -2.8%   ·   KOSPI -4.45%   ·   "
          "NASDAQ -1.48%   ·   S&P 500 -0.50%   ·   DOW +0.85%")

LEAD_KICKER = "TOKYO · SEOUL — MARKETS"
LEAD_HEAD = "ASIAN MARKETS SLIDE AS AI DOUBTS RETURN"
LEAD_DECK = ("Tokyo's Nikkei falls 2.8% and Seoul's Kospi sinks 4.45% in "
             "early Wednesday trading, after a tech-led retreat on "
             "Wall Street.")
LEAD_PHOTO = os.path.join(REPO, "assets", "markets.jpg")
LEAD_BODY = ("Tokyo's Nikkei 225 fell 2.8 per cent in early trading on "
             "Wednesday, touching 56,982, while Seoul's Kospi sank 4.45 "
             "per cent to 4,783 and the Kosdaq lost 2.78 per cent — a day "
             "after Wall Street's Tuesday retreat, when the Nasdaq fell "
             "1.48 per cent and the Philadelphia chip index dropped 7.88 "
             "per cent. Advantest, the chip-testing maker, plunged 12 per "
             "cent in Tokyo. Investors questioned whether heavy spending "
             "on artificial intelligence can justify current valuations, "
             "and awaited US inflation data and a possible tariff "
             "announcement later on Wednesday.")

LEFT_KICKER = "UKRAINE — THE WAR'S TOLL"
LEFT_HEAD = "700,000 RUSSIAN SOLDIERS KILLED, NEW ANALYSIS FINDS"
LEFT_PHOTO = os.path.join(REPO, "assets", "kyiv.jpg")
LEFT_BODY = ("More than 700,000 Russian soldiers have been killed in the "
             "nearly five-year war on Ukraine, according to a new analysis "
             "published on Wednesday. The figure, reported by RFE/RL, "
             "underlines Moscow's determination to conquer Ukrainian "
             "territory — and Kyiv's determination to inflict mass "
             "casualties in return.")

RIGHT_KICKER = "TOKYO — MARKETS"
RIGHT_HEAD = "NIKKEI SEEN RISING NEXT YEAR, SHORT OF RECORD"
RIGHT_PHOTO = os.path.join(REPO, "assets", "shibuya.jpg")
RIGHT_BODY = ("Japan's Nikkei will rise next year but stay well below its "
              "record high, a Reuters poll of 22 analysts published on "
              "Wednesday found. The median forecast puts the index at "
              "65,000 by June 2027 and 67,500 by year-end — far short of "
              "its all-time peak of 72,832 reached in June. Investors are "
              "reassessing AI-linked bets after the US midterm elections.")

BRIEFS = [
    ("WASHINGTON",
     "Investors await US inflation data and a possible tariff announcement "
     "later on Wednesday, after Tuesday's split Wall Street session."),
    ("MANILA",
     "A magnitude 4.4 earthquake struck off Zamboanga del Norte at 1:01 "
     "a.m. local time; intensity I was felt and no damage was reported."),
    ("BHOPAL",
     "India face Japan tonight at 7 p.m. IST in the Women's Asian "
     "Champions Trophy — both sides unbeaten on 12 points."),
]

FOOT_A = ("All events here happened, or were first reported, on Wednesday "
          "25 November 2026. Sources: Wall Street Journal; JBizNews; "
          "RFE/RL; Reuters; PHIVOLCS; Hockey India.")
FOOT_B = ("Photos are freely licensed file photos, not from today: Tokyo "
          "Stock Exchange trading floor (Flickr / Jacob Ehnmark, CC BY); "
          "Maidan Square, Kyiv (Flickr / jlori, CC BY); Shibuya, Tokyo "
          "(Flickr / prkbr, CC BY).")


def masthead(page):
    page.centred("THE WORLD TODAY", face(F_SERIF_B, 40))
    page.y -= int(40 * SS * 0.4)
    page.centred("WEDNESDAY, 25 NOVEMBER 2026", face(F_SANS_B, 15))
    page.centred("ONE DAY  ·  ONE PAGE  ·  No. 329", face(F_SANS, 11),
                 fill=MUTED)
    page.y += 6 * SS
    page.heavy_rule()
    page.rule(weight=1, gap=8)


def ticker(page):
    font = face(F_SANS_B, 12)
    tall = 28 * SS
    page.d.rectangle([SIDE, page.y, SIDE + INNER, page.y + tall], fill=BLACK)
    wide = page.d.textlength(TICKER, font=font)
    tx = SIDE + (INNER - wide) // 2
    ty = page.y + (tall - font.size) // 2 - 2 * SS
    page.d.text((tx, ty), TICKER, font=font, fill=NEWS_PRINT)
    page.y += tall + 6 * SS


def lead(page):
    page.spaced(LEAD_KICKER, face(F_SANS_B, 13), SIGNAL)
    head = face(F_SERIF_B, 34)
    for line in fit_lines(page.d, LEAD_HEAD, head, INNER):
        page.d.text((SIDE, page.y), line, font=head, fill=BLACK)
        page.y += int(34 * SS * 1.1)
    page.y += 2 * SS
    page.block(LEAD_DECK, face(F_SERIF, 14), INNER, leading=1.45)
    page.y += 4 * SS
    page.photo(LEAD_PHOTO, INNER, 104, anchor=0.5)
    page.d.text((SIDE, page.y),
                "The Tokyo Stock Exchange trading floor. "
                "(File photo: Flickr / Jacob Ehnmark, CC BY)",
                font=face(F_SERIF_I, 11), fill=MUTED)
    page.y += int(11 * SS * 1.7) + 2 * SS
    # Three-column body: fit all lines, then deal them across 3 columns.
    body = face(F_SERIF, 12)
    gap = 14 * SS
    col = (INNER - 2 * gap) // 3
    lines = fit_lines(page.d, LEAD_BODY, body, col)
    per = (len(lines) + 2) // 3
    lh = int(12 * SS * 1.5)
    top = page.y
    deepest = top
    for c in range(3):
        chunk = lines[c * per:(c + 1) * per]
        yy = top
        for line in chunk:
            page.d.text((SIDE + c * (col + gap), yy), line, font=body,
                        fill=BLACK)
            yy += lh
        deepest = max(deepest, yy)
    page.y = deepest + 4 * SS
    page.rule(weight=1, gap=6)


def middle(page):
    start = page.y
    half = (INNER - 20 * SS) // 2
    kick = face(F_SANS_B, 13)
    head = face(F_SERIF_B, 22)
    body = face(F_SERIF, 13)
    cap = face(F_SERIF_I, 11)

    def one(x, kicker, headline, photo, anchor, caption, text):
        yy = start
        cx = x
        for ch in kicker:
            page.d.text((cx, yy), ch, font=kick, fill=SIGNAL)
            cx += page.d.textlength(ch, font=kick) + 2
        yy += int(13 * SS * 1.7)
        for line in fit_lines(page.d, headline, head, half):
            page.d.text((x, yy), line, font=head, fill=BLACK)
            yy += int(22 * SS * 1.12)
        yy += 3 * SS
        shot = Image.open(photo).convert("RGB")
        tall = 50 * SS
        page.img.paste(fill_frame(shot, half, tall, anchor), (x, yy))
        yy += tall + 4 * SS
        page.d.text((x, yy), caption, font=cap, fill=MUTED)
        yy += int(11 * SS * 1.7) + 2 * SS
        lh = int(13 * SS * 1.5)
        for line in fit_lines(page.d, text, body, half):
            page.d.text((x, yy), line, font=body, fill=BLACK)
            yy += lh
        return yy

    end_l = one(SIDE, LEFT_KICKER, LEFT_HEAD, LEFT_PHOTO, 0.5,
                "Maidan Square, Kyiv. (File photo: Flickr / jlori, CC BY)",
                LEFT_BODY)
    end_r = one(SIDE + half + 20 * SS, RIGHT_KICKER, RIGHT_HEAD, RIGHT_PHOTO,
                0.4, "Shibuya, Tokyo, at dusk. (File photo: Flickr / "
                "prkbr, CC BY)", RIGHT_BODY)
    page.y = max(end_l, end_r)
    split = SIDE + half + 10 * SS
    page.d.rectangle([split, start, split + 1 * SS, page.y - 4 * SS], fill=BLACK)
    page.y += 4 * SS
    page.rule(weight=1, gap=6)


def briefs(page):
    # Fit the briefs first so the shaded box can be drawn to fit.
    head = face(F_SANS_B, 12)
    body = face(F_SERIF, 13)
    count = len(BRIEFS)
    gap = 16 * SS
    cell = (INNER - (count - 1) * gap) // count
    fitted = []
    deepest_lines = 0
    for place, text in BRIEFS:
        lines = fit_lines(page.d, text, body, cell)
        fitted.append((place, lines))
        deepest_lines = max(deepest_lines, len(lines))
    box_h = (int(13 * SS * 1.7) + int(12 * SS * 1.7)
             + deepest_lines * int(13 * SS * 1.45) + 10 * SS)
    top = page.y
    page.d.rectangle([SIDE, top, SIDE + INNER, top + box_h], fill=SHADE)
    page.y = top + 7 * SS
    page.spaced("THE DAY IN BRIEF", face(F_SANS_B, 13), BLACK)
    page.y -= int(13 * SS * 0.35)
    for i, (place, lines) in enumerate(fitted):
        bx = SIDE + 10 * SS + i * (cell + gap)
        page.d.text((bx, page.y), place, font=head, fill=SIGNAL)
        yy = page.y + int(12 * SS * 1.7)
        lh = int(13 * SS * 1.45)
        for line in lines:
            page.d.text((bx, yy), line, font=body, fill=BLACK)
            yy += lh
    page.y = top + box_h + 6 * SS
    page.rule(weight=1, gap=4)


def footer(page):
    foot = face(F_SANS, 8)
    page.block(FOOT_A, foot, INNER, fill=MUTED, leading=1.55)
    page.y += 2 * SS
    page.block(FOOT_B, foot, INNER, fill=MUTED, leading=1.55)


def main():
    page = Sheet()
    masthead(page)
    ticker(page)
    lead(page)
    middle(page)
    briefs(page)
    footer(page)
    page.save()


if __name__ == "__main__":
    main()
