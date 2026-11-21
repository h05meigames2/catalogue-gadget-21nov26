#!/usr/bin/env python3
"""Catalogue photo of an impossible gadget: the SELF-POWERED power strip.

A sleek white power strip whose own cable loops back and plugs into its
own socket. One accessory: a paper electricity bill reading $0.00.

Drawn entirely with Pillow (stdlib + PIL only, no network).
Writes one image to $MAKEFUN_OUTPUT_DIR/entry.png (fallback ./out/entry.png).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1024, 768

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def rounded_rect(d, box, radius, **kw):
    d.rounded_rectangle(box, radius=radius, **kw)


def bezier(p0, p1, p2, p3, n=90):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3 * p0[0] + 3 * mt * mt * t * p1[0] + 3 * mt * t * t * p2[0] + t**3 * p3[0]
        y = mt**3 * p0[1] + 3 * mt * mt * t * p1[1] + 3 * mt * t * t * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def main():
    # ---- backdrop: clean studio gradient ---------------------------------
    img = Image.new("RGB", (W, H))
    px = img.load()
    top = (250, 251, 253)
    bot = (226, 229, 233)
    for y in range(H):
        t = y / (H - 1)
        # gentle ease so the top stays bright and the floor is a touch darker
        t = t * t * 0.6 + t * 0.4
        px_line = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        for x in range(W):
            px[x, y] = px_line
    d = ImageDraw.Draw(img, "RGBA")

    # soft radial pool of light behind the product
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((180, 60, 860, 700), fill=(255, 255, 255, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(90))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- soft contact shadows (blurred layer) ----------------------------
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.ellipse((150, 545, 800, 600), fill=(30, 34, 40, 110))   # strip shadow
    sd.ellipse((800, 560, 990, 610), fill=(30, 34, 40, 90))    # bill shadow
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- the cable: exits right end, loops up, plugs into its own socket -
    cable_pts = bezier((792, 505), (905, 470), (945, 250), (830, 175),
                       60) + bezier((830, 175), (720, 110), (645, 170), (600, 334), 60)
    d.line(cable_pts, fill=(52, 56, 62), width=26, joint="curve")
    # cable highlight so it reads as round rubber, not a flat line
    hi_pts = [(x - 4, y - 6) for (x, y) in cable_pts]
    d.line(hi_pts, fill=(110, 116, 124), width=6, joint="curve")

    # ---- power strip body -------------------------------------------------
    bx0, by0, bx1, by1 = 170, 420, 800, 545
    rounded_rect(d, (bx0, by0, bx1, by1), 26, fill=(250, 250, 252),
                 outline=(196, 200, 206), width=2)
    # top highlight + bottom shade for a moulded-plastic look
    rounded_rect(d, (bx0 + 4, by0 + 4, bx1 - 4, by0 + 26), 20, fill=(255, 255, 255))
    d.rounded_rectangle((bx0 + 4, by1 - 22, bx1 - 4, by1 - 4), radius=18,
                        fill=(214, 217, 222))
    # end caps
    d.rounded_rectangle((bx0 + 2, by0 + 2, bx0 + 26, by1 - 2), radius=12,
                        fill=(232, 234, 238))
    d.rounded_rectangle((bx1 - 28, by0 + 2, bx1 - 2, by1 - 2), radius=12,
                        fill=(232, 234, 238))

    # rocker switch (left end) + green LED
    rounded_rect(d, (196, 448, 232, 520), 8, fill=(206, 48, 48),
                 outline=(150, 30, 30), width=1)
    d.line((214, 460, 214, 508), fill=(255, 255, 255), width=3)
    # LED glow
    led = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(led)
    ld.ellipse((246 - 22, 452 - 22, 246 + 22, 452 + 22), fill=(60, 220, 110, 120))
    led = led.filter(ImageFilter.GaussianBlur(10))
    img.paste(Image.alpha_composite(img.convert("RGBA"), led).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse((238, 444, 254, 460), fill=(46, 204, 96), outline=(20, 120, 55), width=2)
    d.ellipse((242, 447, 248, 453), fill=(200, 255, 215))

    # ---- five sockets ------------------------------------------------------
    socket_xs = [300, 400, 500, 600, 700]
    for i, cx in enumerate(socket_xs):
        cy = 483
        # recessed socket well
        d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), fill=(228, 230, 234),
                  outline=(180, 184, 190), width=2)
        d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=(38, 40, 44))
        # two blade slots + round ground hole
        d.rounded_rectangle((cx - 13, cy - 9, cx - 5, cy + 9), radius=3, fill=(12, 12, 14))
        d.rounded_rectangle((cx + 5, cy - 9, cx + 13, cy + 9), radius=3, fill=(12, 12, 14))
        d.ellipse((cx - 4, cy + 13, cx + 4, cy + 21), fill=(12, 12, 14))

    # ---- the plug, inserted into socket #4 (x=600) ------------------------
    # plug body: white, angled slightly, prongs disappearing into the socket
    plug = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plug)
    pd.rounded_rectangle((572, 330, 628, 452), radius=14, fill=(245, 245, 247, 255),
                         outline=(190, 193, 198, 255), width=2)
    pd.rounded_rectangle((578, 344, 622, 372), radius=8, fill=(222, 224, 228, 255))
    pd.line((584, 452, 584, 468), fill=(120, 124, 130, 255), width=7)
    pd.line((616, 452, 616, 468), fill=(120, 124, 130, 255), width=7)
    img.paste(Image.alpha_composite(img.convert("RGBA"), plug).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- brand text on the strip -------------------------------------------
    d.text((300, 428), "SELF-POWERED", font=font(17, bold=True), fill=(90, 94, 100))
    d.text((700, 428), "SP-\u221e", font=font(17, bold=True), fill=(90, 94, 100))
    d.text((300, 520), "MODEL SP-\u221e  \u00b7  250V  \u00b7  NO GRID REQUIRED",
           font=font(11), fill=(140, 144, 150))

    # ---- accessory: the $0.00 electricity bill, leaning --------------------
    bill = Image.new("RGBA", (300, 260), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bill)
    bd.rectangle((8, 8, 292, 252), fill=(255, 255, 255, 255),
                 outline=(205, 208, 212, 255), width=2)
    bd.rectangle((8, 8, 292, 52), fill=(238, 240, 243, 255))
    bd.text((22, 16), "ELECTRICITY BILL", font=font(19, bold=True), fill=(40, 42, 46))
    bd.text((22, 68), "Account: SP-\u221e-0001", font=font(15), fill=(80, 84, 90))
    bd.text((22, 94), "Period:  NOV 2026", font=font(15), fill=(80, 84, 90))
    bd.text((22, 120), "Usage:  0 kWh", font=font(15), fill=(80, 84, 90))
    bd.line((22, 150, 278, 150), fill=(200, 203, 208), width=2)
    bd.text((22, 162), "AMOUNT DUE", font=font(18, bold=True), fill=(40, 42, 46))
    bd.text((22, 190), "$0.00", font=font(42, bold=True), fill=(30, 160, 80))
    bd.text((180, 204), "PAID IN FULL", font=font(14, bold=True), fill=(30, 160, 80))
    bill = bill.rotate(-7, expand=True, resample=Image.BICUBIC)
    img.paste(bill, (688, 300), bill)

    # ---- output -------------------------------------------------------------
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(".", "out")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    print(f"wrote {path} {img.size} {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
