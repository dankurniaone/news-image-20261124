#!/usr/bin/env python3
"""Build the 24 November 2026 front page as a 680x1024 PNG.

THE WORLD TODAY, one day on one page: a lead on the Russian jets over
the East Sea, two stories below it (Pyongyang, Kuala Lumpur), a strip of
three briefs, and a footer naming the sources. Everything is drawn with
Pillow at double size and shrunk with LANCZOS, so the small type stays
sharp when the page is read at 300 pixels across.

The photographs are real Pexels file photos (none taken today); the words
are the day's verified news. Run from the repository root:

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
        self.y = 18 * SS

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

    def photo_at(self, path, x, width, height_pts, anchor=0.5):
        shot = Image.open(path).convert("RGB")
        tall = height_pts * SS
        self.img.paste(fill_frame(shot, width, tall, anchor), (x, self.y))
        self.y += tall + 4 * SS

    def save(self):
        final = self.img.resize((680, 1024), Image.LANCZOS)
        dest = os.path.join(REPO, "entry.png")
        final.save(dest, "PNG")
        print("wrote entry.png", final.size,
              os.path.getsize(dest), "bytes,",
              "content ends at y =", self.y // SS, "(logical)")


# ------------------------------------------------------------------ the day
# Every item below is an event of Tuesday 24 November 2026, checked the
# same day against the primary reporting: Seoul's Joint Chiefs of Staff,
# the KCNA statement, Anwar Ibrahim in the Malaysian parliament, the Tokyo
# close, and the Singapore prime minister in Canberra. Items whose events
# fell earlier — the Villavicencio bombing, the Treasury's Iran sanctions,
# the EU's 22nd Russia package, the FIFA host announcement, the COP31
# collapse — were left out.
LEAD_KICKER = "KOREA · ULLEUNG ISLAND"
LEAD_HEAD = "RUSSIAN JETS TRIGGER ISLAND AIR-RAID ALERT"
LEAD_DECK = ("Seoul scrambles fighter jets as Russian warplanes enter its "
             "air defence zone near Ulleung Island; a five-minute air-raid "
             "warning sends residents to shelter.")
LEAD_PHOTO = os.path.join(REPO, "assets", "jets.jpg")
LEAD_LEFT = ("Several Russian military aircraft entered South Korea's air "
             "defence identification zone over the East Sea on Tuesday "
             "morning and flew towards Ulleung Island, about 130 km off the "
             "east coast. Detected before they entered the zone, the "
             "military scrambled fighter jets, including F-15Ks, to respond.")
LEAD_RIGHT = ("At 7:52 a.m. the Interior Ministry told residents by text "
              "to take shelter; the warning was lifted five minutes later. "
              "The Joint Chiefs of Staff said there was no violation of "
              "South Korean airspace. Seoul said it would summon Russia's "
              "defence attache to protest.")

LEFT_KICKER = "PYONGYANG"
LEFT_HEAD = "NORTH KOREA THREATENS TO SHUT SWISS OFFICE"
LEFT_PHOTO = os.path.join(REPO, "assets", "pyongyang.jpg")
LEFT_BODY = ("Kim Yo-jong, the sister of leader Kim Jong-un, said in a "
             "KCNA statement that Switzerland's sanctions on the Songdowon "
             "children's camp — accused over the transfer of Ukrainian "
             "children from Russian-occupied territory — infringed North "
             "Korea's sovereignty. She said the Foreign Ministry would "
             "examine withdrawing the Swiss office, opened in Pyongyang "
             "only last month, within days.")

RIGHT_KICKER = "KUALA LUMPUR"
RIGHT_HEAD = "MALAYSIA TO SEND 6,803 MYANMAR NATIONALS HOME"
RIGHT_PHOTO = os.path.join(REPO, "assets", "kuala-lumpur.jpg")
RIGHT_BODY = ("Prime Minister Anwar Ibrahim told parliament on Tuesday that "
              "Malaysia will send 6,803 Myanmar nationals home in December "
              "— 1,500 aboard three naval vessels on Dec. 6 and 7, and "
              "5,303 by air, at Myanmar's expense. The announcement came "
              "five days after the ICJ ruled that Myanmar committed genocide "
              "against the Rohingya.")

BRIEFS = [
    ("TOKYO",
     "The Nikkei 225 jumped 4.4% on Tuesday, topping 59,000 at one point, "
     "as chip stocks rallied after Nvidia reinstated Jensen Huang; the "
     "Nasdaq had gained 6.5% on Monday."),
    ("CANBERRA",
     "Singapore's prime minister, Lawrence Wong, said Singapore is working "
     "with the US to stop firms using it to reroute AI chips, and will keep "
     "investigating Megaspeed after Washington blacklisted the firm."),
    ("KUALA LUMPUR",
     "Turkiye is not yet ready to consider taking in 10,000 Rohingya "
     "refugees from Malaysia, Anwar told parliament, as Kuala Lumpur seeks "
     "third countries to resettle them."),
]

FOOT_A = ("All events here happened on Tuesday 24 November 2026. Sources: "
          "ROK Joint Chiefs of Staff; KCNA via Reuters; AFP; Singapore "
          "PMO; Reuters.")
FOOT_B = ("Photos are Pexels file photos, not from today: F-16 fighters; "
          "Juche Tower, Pyongyang; Petronas Towers, Kuala Lumpur.")


def masthead(page):
    page.centred("THE WORLD TODAY", face(F_SERIF_B, 40))
    page.y -= int(40 * SS * 0.4)
    page.centred("TUESDAY, 24 NOVEMBER 2026", face(F_SANS_B, 15))
    page.centred("ONE DAY  ·  ONE PAGE  ·  No. 328", face(F_SANS, 11),
                 fill=MUTED)
    page.y += 6 * SS
    page.heavy_rule()
    page.rule(weight=1, gap=8)


def lead(page):
    page.spaced(LEAD_KICKER, face(F_SANS_B, 13), SIGNAL)
    head = face(F_SERIF_B, 36)
    for line in fit_lines(page.d, LEAD_HEAD, head, INNER):
        page.d.text((SIDE, page.y), line, font=head, fill=BLACK)
        page.y += int(36 * SS * 1.1)
    page.y += 2 * SS
    page.block(LEAD_DECK, face(F_SERIF, 14), INNER, leading=1.45)
    page.y += 4 * SS
    page.photo(LEAD_PHOTO, INNER, 74, anchor=0.42)
    page.d.text((SIDE, page.y), "F-16 fighters in flight. (File photo: Pexels)",
                font=face(F_SERIF_I, 11), fill=MUTED)
    page.y += int(11 * SS * 1.7) + 2 * SS
    body = face(F_SERIF, 13)
    half = (INNER - 20 * SS) // 2
    top = page.y
    lh = int(13 * SS * 1.5)
    end_l = top
    for line in fit_lines(page.d, LEAD_LEFT, body, half):
        page.d.text((SIDE, end_l), line, font=body, fill=BLACK)
        end_l += lh
    end_r = top
    for line in fit_lines(page.d, LEAD_RIGHT, body, half):
        page.d.text((SIDE + half + 20 * SS, end_r), line, font=body, fill=BLACK)
        end_r += lh
    page.y = max(end_l, end_r) + 4 * SS
    page.rule(weight=1, gap=6)


def middle(page):
    start = page.y
    half = (INNER - 20 * SS) // 2
    kick = face(F_SANS_B, 13)
    head = face(F_SERIF_B, 23)
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
            yy += int(23 * SS * 1.12)
        yy += 3 * SS
        shot = Image.open(photo).convert("RGB")
        tall = 56 * SS
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
                "The Juche Tower, Pyongyang. (File photo: Pexels)", LEFT_BODY)
    end_r = one(SIDE + half + 20 * SS, RIGHT_KICKER, RIGHT_HEAD, RIGHT_PHOTO,
                0.25, "The Petronas Towers, Kuala Lumpur. (File photo: Pexels)",
                RIGHT_BODY)
    page.y = max(end_l, end_r)
    split = SIDE + half + 10 * SS
    page.d.rectangle([split, start, split + 1 * SS, page.y - 4 * SS], fill=BLACK)
    page.y += 4 * SS
    page.rule(weight=1, gap=6)


def briefs(page):
    page.spaced("THE DAY IN BRIEF", face(F_SANS_B, 13), BLACK)
    count = len(BRIEFS)
    gap = 16 * SS
    cell = (INNER - (count - 1) * gap) // count
    head = face(F_SANS_B, 12)
    body = face(F_SERIF, 13)
    deepest = page.y
    for i, (place, text) in enumerate(BRIEFS):
        bx = SIDE + i * (cell + gap)
        page.d.text((bx, page.y), place, font=head, fill=SIGNAL)
        yy = page.y + int(12 * SS * 1.7)
        lh = int(13 * SS * 1.45)
        for line in fit_lines(page.d, text, body, cell):
            page.d.text((bx, yy), line, font=body, fill=BLACK)
            yy += lh
        deepest = max(deepest, yy)
    page.y = deepest + 6 * SS
    page.rule(weight=1, gap=4)


def footer(page):
    foot = face(F_SANS, 8)
    page.block(FOOT_A, foot, INNER, fill=MUTED, leading=1.55)
    page.y += 2 * SS
    page.block(FOOT_B, foot, INNER, fill=MUTED, leading=1.55)


def main():
    page = Sheet()
    masthead(page)
    lead(page)
    middle(page)
    briefs(page)
    footer(page)
    page.save()


if __name__ == "__main__":
    main()
