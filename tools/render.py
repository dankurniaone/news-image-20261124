#!/usr/bin/env python3
"""Render THE WORLD TODAY — a one-page broadsheet summing up the world news
of Tuesday 24 November 2026 — as a 680x1024 PNG.

Drawn at 2x (1360x2048) with Pillow and downscaled with LANCZOS so the
small type stays crisp. Layout: centred masthead and dateline, a lead story
with deck, photograph and two-column body, two stories side by side with
photographs and a vertical divider, a briefs strip, and a sources footer.
All photographs are freely licensed file photos from Pexels, credited in
the footer; none is from 24 November itself. Every story on the page is an
event of 24 November 2026, date-checked against primary reporting the
same day: the Joint Chiefs of Staff statement in Seoul, the KCNA statement
in Pyongyang, Anwar Ibrahim's statement in the Malaysian parliament, the
Tokyo market close, and the Singapore prime minister's press conference
in Canberra.

Run:  python3 tools/render.py   (writes entry.png next to main.py)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SCALE = 2
W, H = 680 * SCALE, 1024 * SCALE
MARGIN = 28 * SCALE
CW = W - 2 * MARGIN  # content width

PAPER = (246, 242, 231)   # warm newsprint
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


def wrap(text, fnt, width, draw):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill=INK, leading=None):
    """Draw lines top to bottom; returns the y below the last line."""
    lh = leading if leading is not None else int(fnt.size * 1.35)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def crop_cover(img, tw, th, focus=0.5):
    """Centre-crop an image to the target aspect, then resize to it.
    focus 0.0 takes the top of the frame, 1.0 the bottom, 0.5 the centre."""
    iw, ih = img.size
    ta = tw / th
    ia = iw / ih
    if ia > ta:  # too wide: trim sides
        nw = int(ih * ta)
        x0 = (iw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, ih))
    else:  # too tall: trim top/bottom around the focus point
        nh = int(iw / ta)
        y0 = max(0, min(ih - nh, int((ih - nh) * focus)))
        img = img.crop((0, y0, iw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def tracked(draw, x, y, text, fnt, fill, tracking=0):
    """Draw text with extra space between characters; returns end x."""
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


# ---------------------------------------------------------------- stories
# Final set (afternoon, 24 Nov). Every event below happened on 24 Nov 2026
# and was checked against primary reporting the same day.
LEAD = {
    "kicker": "KOREA · ULLEUNG ISLAND",
    "headline": "RUSSIAN JETS TRIGGER ISLAND AIR-RAID ALERT",
    "deck": ("Seoul scrambles fighter jets as Russian warplanes enter its "
             "air defence zone near Ulleung Island; a five-minute air-raid "
             "warning sends residents to shelter."),
    "photo": os.path.join(ROOT, "assets", "jets.jpg"),
    "photo_h": 80,
    "photo_focus": 0.42,
    "caption": "F-16 fighters in flight. (File photo: Pexels)",
    "left": ("Several Russian military aircraft entered South Korea's air "
             "defence identification zone over the East Sea on Tuesday "
             "morning and flew towards Ulleung Island, about 130 km off the "
             "east coast. Detected before they entered the zone, the "
             "military scrambled fighter jets, including F-15Ks, to respond."),
    "right": ("At 7:52 a.m. the Interior Ministry told residents by text "
              "to take shelter; the warning was lifted five minutes later. "
              "The Joint Chiefs of Staff said there was no violation of "
              "South Korean airspace. Seoul said it would summon Russia's "
              "defence attache to protest."),
}

MIDDLE_LEFT = {
    "kicker": "PYONGYANG",
    "headline": "NORTH KOREA THREATENS TO SHUT SWISS OFFICE",
    "photo": os.path.join(ROOT, "assets", "pyongyang.jpg"),
    "photo_h": 56,
    "photo_focus": 0.5,
    "caption": "The Juche Tower, Pyongyang. (File photo: Pexels)",
    "body": ("Kim Yo-jong, the sister of leader Kim Jong-un, said in a "
             "KCNA statement that Switzerland's sanctions on the Songdowon "
             "children's camp — accused over the transfer of Ukrainian "
             "children from Russian-occupied territory — infringed North "
             "Korea's sovereignty. She said the Foreign Ministry would "
             "examine withdrawing the Swiss office, opened in Pyongyang "
             "only last month, within days."),
}

MIDDLE_RIGHT = {
    "kicker": "KUALA LUMPUR",
    "headline": "MALAYSIA TO SEND 6,803 MYANMAR NATIONALS HOME",
    "photo": os.path.join(ROOT, "assets", "kuala-lumpur.jpg"),
    "photo_h": 56,
    "photo_focus": 0.25,
    "caption": "The Petronas Towers, Kuala Lumpur. (File photo: Pexels)",
    "body": ("Prime Minister Anwar Ibrahim told parliament on Tuesday that "
             "Malaysia will send 6,803 Myanmar nationals home in December "
             "— 1,500 aboard three naval vessels on Dec. 6 and 7, and "
             "5,303 by air, at Myanmar's expense. The announcement came "
             "five days after the ICJ ruled that Myanmar committed genocide "
             "against the Rohingya."),
}

BRIEFS = [
    ("TOKYO", "The Nikkei 225 jumped 4.4% on Tuesday, topping 59,000 at one "
              "point, as chip stocks rallied after Nvidia reinstated Jensen "
              "Huang; the Nasdaq had gained 6.5% on Monday."),
    ("CANBERRA", "Singapore's prime minister, Lawrence Wong, said Singapore "
                 "is working with the US to stop firms using it to reroute AI "
                 "chips, and will keep investigating Megaspeed after Washington "
                 "blacklisted the firm."),
    ("KUALA LUMPUR", "Turkiye is not yet ready to consider taking in 10,000 "
                      "Rohingya refugees from Malaysia, Anwar told parliament, "
                      "as Kuala Lumpur seeks third countries to resettle them."),
]

FOOT_SOURCES = ("All events here happened on Tuesday 24 November 2026. "
                "Sources: ROK Joint Chiefs of Staff; KCNA via Reuters; AFP; "
                "Singapore PMO; Reuters.")
FOOT_PHOTOS = ("Photos are Pexels file photos, not from today: F-16 fighters; "
               "Juche Tower, Pyongyang; Petronas Towers, Kuala Lumpur.")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x = MARGIN
    y = 18 * SCALE

    # ---- Masthead ----
    f_mast = font(SERIF_B, 40)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, y), t, font=f_mast, fill=INK)
    y += int(40 * SCALE * 1.2)

    f_date = font(SANS_B, 15)
    t = "TUESDAY, 24 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=f_date)) / 2, y), t, font=f_date, fill=INK)
    y += int(15 * SCALE * 1.6)

    f_sub = font(SANS, 11)
    t = "ONE DAY  ·  ONE PAGE  ·  No. 328"
    d.text(((W - d.textlength(t, font=f_sub)) / 2, y), t, font=f_sub, fill=GREY)
    y += int(11 * SCALE * 1.6) + 6 * SCALE

    d.rectangle([x, y, x + CW, y + 3 * SCALE], fill=INK)
    y += 5 * SCALE
    d.rectangle([x, y, x + CW, y + 1 * SCALE], fill=INK)
    y += 8 * SCALE

    # ---- Lead ----
    f_kick = font(SANS_B, 13)
    tracked(d, x, y, LEAD["kicker"], f_kick, RED, tracking=2)
    y += int(13 * SCALE * 1.7)

    f_head = font(SERIF_B, 36)
    y = draw_lines(d, x, y, wrap(LEAD["headline"], f_head, CW, d), f_head,
                   leading=int(36 * SCALE * 1.1))
    y += 2 * SCALE

    f_deck = font(SERIF, 14)
    y = draw_lines(d, x, y, wrap(LEAD["deck"], f_deck, CW, d), f_deck,
                   leading=int(14 * SCALE * 1.45))
    y += 4 * SCALE

    lead_photo = Image.open(LEAD["photo"]).convert("RGB")
    ph = LEAD["photo_h"] * SCALE
    img.paste(crop_cover(lead_photo, CW, ph, focus=LEAD.get("photo_focus", 0.5)),
              (x, y))
    y += ph + 4 * SCALE
    f_cap = font(SERIF_I, 11)
    d.text((x, y), LEAD["caption"], font=f_cap, fill=GREY)
    y += int(11 * SCALE * 1.7) + 2 * SCALE

    # Lead body, two columns
    f_body = font(SERIF, 13)
    col_w = (CW - 20 * SCALE) // 2
    lh = int(13 * SCALE * 1.5)
    y1 = draw_lines(d, x, y, wrap(LEAD["left"], f_body, col_w, d), f_body,
                    leading=lh)
    y2 = draw_lines(d, x + col_w + 20 * SCALE, y,
                    wrap(LEAD["right"], f_body, col_w, d), f_body, leading=lh)
    y = max(y1, y2) + 4 * SCALE
    print("lead ends at y =", y // SCALE)

    d.rectangle([x, y, x + CW, y + 1 * SCALE], fill=INK)
    y += 6 * SCALE

    # ---- Middle: two stories side by side ----
    mid_y = y
    col_w = (CW - 20 * SCALE) // 2
    f_mid_head = font(SERIF_B, 23)

    def story(cx, s):
        yy = mid_y
        tracked(d, cx, yy, s["kicker"], f_kick, RED, tracking=2)
        yy += int(13 * SCALE * 1.7)
        yy = draw_lines(d, cx, yy, wrap(s["headline"], f_mid_head, col_w, d),
                        f_mid_head, leading=int(23 * SCALE * 1.12))
        yy += 3 * SCALE
        im = Image.open(s["photo"]).convert("RGB")
        ph2 = s["photo_h"] * SCALE
        img.paste(crop_cover(im, col_w, ph2, focus=s.get("photo_focus", 0.5)),
                  (cx, yy))
        yy += ph2 + 4 * SCALE
        d.text((cx, yy), s["caption"], font=f_cap, fill=GREY)
        yy += int(11 * SCALE * 1.7) + 2 * SCALE
        yy = draw_lines(d, cx, yy, wrap(s["body"], f_body, col_w, d), f_body,
                        leading=lh)
        return yy

    y_left = story(x, MIDDLE_LEFT)
    y_right = story(x + col_w + 20 * SCALE, MIDDLE_RIGHT)
    y = max(y_left, y_right)
    print("middle ends at y =", y // SCALE, "(left", y_left // SCALE,
          "right", y_right // SCALE, ")")
    # vertical divider between the two middle stories
    div_x = x + col_w + 10 * SCALE
    d.rectangle([div_x, mid_y, div_x + 1 * SCALE, y - 4 * SCALE], fill=INK)
    y += 4 * SCALE

    d.rectangle([x, y, x + CW, y + 1 * SCALE], fill=INK)
    y += 6 * SCALE

    # ---- The day in brief ----
    f_brief_h = font(SANS_B, 13)
    tracked(d, x, y, "THE DAY IN BRIEF", f_brief_h, INK, tracking=2)
    y += int(13 * SCALE * 1.8)
    n = len(BRIEFS)
    gap = 16 * SCALE
    bw = (CW - (n - 1) * gap) // n
    f_bh = font(SANS_B, 12)
    f_bb = font(SERIF, 13)
    yb = y
    for i, (h, b) in enumerate(BRIEFS):
        bx = x + i * (bw + gap)
        d.text((bx, y), h, font=f_bh, fill=RED)
        yy = draw_lines(d, bx, y + int(12 * SCALE * 1.7),
                        wrap(b, f_bb, bw, d), f_bb, leading=int(13 * SCALE * 1.45))
        yb = max(yb, yy)
    y = yb + 6 * SCALE
    print("briefs end at y =", y // SCALE)

    d.rectangle([x, y, x + CW, y + 1 * SCALE], fill=INK)
    y += 4 * SCALE

    # ---- Footer ----
    f_foot = font(SANS, 8)
    y = draw_lines(d, x, y, wrap(FOOT_SOURCES, f_foot, CW, d), f_foot,
                   fill=GREY, leading=int(8 * SCALE * 1.55))
    y = draw_lines(d, x, y + 2 * SCALE, wrap(FOOT_PHOTOS, f_foot, CW, d),
                   f_foot, fill=GREY, leading=int(8 * SCALE * 1.55))

    out = img.resize((680, 1024), Image.LANCZOS)
    out.save(os.path.join(ROOT, "entry.png"), "PNG")
    print("wrote entry.png", out.size,
          os.path.getsize(os.path.join(ROOT, "entry.png")), "bytes,",
          "content ends at y =", y // SCALE, "(logical)")


if __name__ == "__main__":
    main()
