#!/usr/bin/env python3
"""Draw the 22 November 2026 world-news front page (1024x1024 PNG).

One image, five verified stories, drawn with Pillow only. Every fact on
the page was checked against reports published on 21 November 2026
(see README.md for the sources). The page is drawn early on 22 November
UTC, so the Saturday 21 November stories are dated as such on the page.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
PAPER = (247, 243, 230)
INK = (16, 16, 16)
RED = (176, 32, 32)
BLUE = (22, 64, 122)
GREY = (92, 88, 78)
RULE = (16, 16, 16)
GOLD = (198, 158, 28)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns lines fitting `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, leading, color=INK):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, text):
    f = font(SANS_B, 18)
    draw.text((x, y), text, font=f, fill=RED)
    return y + 25


def box(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)


def flames(draw, x, y, w, h):
    """Three missile streaks above burning city blocks."""
    for sx, sy, ln in [(x + 20, y + 8, 70), (x + 110, y + 2, 84),
                       (x + 200, y + 12, 64)]:
        draw.line([sx, sy, sx + ln, sy + 26], fill=RED, width=4)
        draw.ellipse([sx + ln - 4, sy + 22, sx + ln + 4, sy + 30],
                     fill=RED)
    # City blocks, one with a flame on its roof.
    for i, bx in enumerate([x + 8, x + w // 3 + 2, x + 2 * w // 3 - 4]):
        bw = w // 3 - 12
        bh = 70 - i * 12
        draw.rectangle([bx, y + h - 26 - bh, bx + bw, y + h - 26],
                       outline=INK, width=3)
        for wy in range(3):
            draw.rectangle([bx + 8, y + h - 26 - bh + 10 + wy * 18,
                            bx + 20, y + h - 26 - bh + 22 + wy * 18],
                           fill=BLUE)
    fx, fy = x + w // 2, y + h - 96
    draw.polygon([(fx, fy - 40), (fx + 16, fy - 6), (fx + 6, fy - 6),
                  (fx + 20, fy + 12), (fx - 20, fy + 12), (fx - 6, fy - 6),
                  (fx - 16, fy - 6)], fill=RED)
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=BLUE)


def ship(draw, x, y, w, h):
    """Cargo ship on waves, smoke rising, two drones above."""
    for dx, dy in [(x + 24, y + 8), (x + w - 24, y + 4)]:
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=INK)
        draw.line([dx, dy + 5, dx - 10, dy + 20], fill=INK, width=3)
    for k in range(2):
        draw.ellipse([x + w // 2 - 22 + k * 16, y + 34 + k * 12,
                      x + w // 2 + 8 + k * 16, y + 58 + k * 12],
                     outline=GREY, width=3)
    # Hull and containers.
    draw.polygon([(x + 4, y + h - 52), (x + w - 4, y + h - 52),
                  (x + w - 22, y + h - 24), (x + 22, y + h - 24)],
                 fill=INK)
    draw.rectangle([x + 28, y + h - 78, x + 62, y + h - 52],
                   fill=RED)
    draw.rectangle([x + 68, y + h - 78, x + 102, y + h - 52],
                   fill=BLUE)
    for k in range(2):
        draw.arc([x + 4 + k * (w // 2), y + h - 18,
                  x + 4 + (k + 1) * (w // 2), y + h + 4],
                 start=180, end=360, fill=BLUE, width=5)


def badge(draw, cx, cy, r):
    """Five-point star badge: the arrest."""
    pts = []
    for k in range(10):
        rr = r if k % 2 == 0 else r * 0.45
        a = math.pi * 2 * k / 10 - math.pi / 2
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    draw.polygon(pts, fill=GOLD, outline=INK)


def globe_clock(draw, cx, cy, r):
    """A globe with a clock face: talks running into overtime."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=4)
    draw.arc([cx - r, cy - r // 2, cx + r, cy + r // 2],
             start=180, end=360, fill=BLUE, width=3)
    draw.line([cx, cy - r, cx, cy + r], fill=BLUE, width=3)
    draw.line([cx, cy, cx + int(0.6 * r), cy - int(0.4 * r)],
              fill=RED, width=5)
    draw.line([cx, cy, cx - int(0.3 * r), cy - int(0.5 * r)],
              fill=RED, width=5)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)


def phone(draw, x, y, w, h):
    """A handset over a row of European stars."""
    draw.rounded_rectangle([x + 10, y + 10, x + w - 10, y + h - 10],
                           radius=14, outline=INK, width=4)
    draw.rectangle([x + 24, y + 28, x + w - 24, y + 42], fill=BLUE)
    for k in range(5):
        sx = x + 28 + k * 16
        draw.ellipse([sx, y + 54, sx + 10, y + 64], fill=GOLD)
    draw.line([x + 24, y + 78, x + w - 24, y + 78], fill=GREY, width=2)
    draw.line([x + 24, y + 92, x + w - 40, y + 92], fill=GREY, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Double outer rule.
    d.rectangle([14, 14, W - 14, H - 14], outline=RULE, width=3)
    d.rectangle([22, 22, W - 22, H - 22], outline=RULE, width=1)

    # Masthead.
    title = "ONE DAY · ONE PAGE"
    tf = font(SERIF_B, 58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 36), title, font=tf, fill=INK)
    d.line([40, 116, W - 40, 116], fill=RULE, width=3)
    sub = "SUNDAY 22 NOVEMBER 2026  ·  THE WORLD'S NEWS IN ONE IMAGE"
    sf = font(SANS_B, 21)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 126), sub, font=sf, fill=INK)
    d.line([40, 162, W - 40, 162], fill=RULE, width=1)

    # --- Lead: Kryvyi Rih triple-tap (full width, y 176-404) ---
    box(d, 36, 176, 952, 228)
    y = kicker(d, 52, 188, "KRYVYI RIH  ·  UKRAINE")
    y = para(d, 52, y, "Three strikes, one playground",
             font(SERIF_B, 38), 600, 44)
    y = para(d, 52, y + 6,
             "A Russian triple-tap hits President Zelenskyy's home "
             "city on Friday night: missiles strike a restaurant car "
             "park, then drones hit the rescuers. A boy of 7 and a "
             "paramedic of 20 are killed; about 60 are wounded.",
             font(SANS, 19), 600, 23)
    flames(d, 690, 208, 282, 168)

    # --- Row 2: Sparta II | El Chapo Isidro (y 412-636) ---
    box(d, 36, 412, 466, 224)
    y = kicker(d, 52, 424, "GULF OF FINLAND  ·  THE BALTIC")
    y = para(d, 52, y, "Drones set a Russian ship alight",
             font(SERIF_B, 27), 300, 33)
    y = para(d, 52, y + 6,
             "Two drones strike the sanctioned cargo ship Sparta II "
             "in neutral waters on Saturday. She burns as Finland "
             "tightens air and sea limits. Kyiv has not claimed it.",
             font(SANS, 18), 300, 23)
    ship(d, 356, 512, 136, 112)

    box(d, 522, 412, 466, 224)
    y = kicker(d, 538, 424, "SINALOA, MEXICO  ·  THE CARTELS")
    y = para(d, 538, y, "El Chapo Isidro is captured",
             font(SERIF_B, 27), 434, 33)
    y = para(d, 538, y + 6,
             "Mexican special forces seize FBI top-10 fugitive "
             "Fausto Isidro Meza Flores in Guasave on Friday night; "
             "4 soldiers and 7 gunmen die. US intelligence helped.",
             font(SANS, 18), 320, 23)
    badge(d, 902, 560, 52)

    # --- Row 3: COP31 | Trump-Europe call (y 650-880) ---
    box(d, 36, 650, 466, 230)
    y = kicker(d, 52, 662, "ANTALYA, TURKIYE  ·  CLIMATE")
    y = para(d, 52, y, "COP31 runs past its deadline",
             font(SERIF_B, 27), 434, 33)
    y = para(d, 52, y + 6,
             "Nearly 200 nations miss Friday's deadline and keep "
             "talking on Saturday. The draft drops fossil fuels; "
             "the EU says no deal beats a weak one.",
             font(SANS, 18), 320, 23)
    globe_clock(d, 400, 800, 52)

    box(d, 522, 650, 466, 230)
    y = kicker(d, 538, 662, "KYIV  ·  THE ALLIES")
    y = para(d, 538, y, "Trump: Europe spends too much",
             font(SERIF_B, 27), 300, 33)
    y = para(d, 538, y + 6,
             "Zelenskyy says Trump told Europe's leaders they "
             "spend a lot on Ukraine and could keep it once the "
             "war ends. \"It didn't sound like a threat.\"",
             font(SANS, 18), 310, 23)
    phone(d, 868, 716, 104, 124)

    # --- Footer ---
    d.line([40, 894, W - 40, 894], fill=RULE, width=1)
    foot = ("Drawn early on Sunday 22 November 2026 (UTC). The five "
            "stories are Saturday 21 November's news as reported "
            "overnight. Sources: CNN, Institute for the Study of "
            "War, Reuters, Associated Press, Bulletin Observer.")
    para(d, 40, 906, foot, font(SANS, 15), 944, 21, color=GREY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
