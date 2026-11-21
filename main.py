#!/usr/bin/env python3
"""Catalogue photo of an impossible gadget: a self-powered power strip.

The strip's own cable loops back and plugs into its own socket, so it
powers itself forever. One accessory: the electricity bill for $0.00.
Drawn with PIL only, no network. Output: $MAKEFUN_OUTPUT_DIR/entry.png
(or ./out/entry.png), 1024x768 PNG.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = 2  # supersample factor
W, H = 1024 * S, 768 * S

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size):
    return ImageFont.truetype(FONT, size * S)


def font_reg(size):
    return ImageFont.truetype(FONT_REG, size * S)


def main():
    img = Image.new("RGB", (W, H), (244, 246, 248))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- studio backdrop: soft vertical gradient + seamless floor ----
    for y in range(H):
        t = y / H
        r = int(246 - 14 * t)
        g = int(248 - 14 * t)
        b = int(250 - 12 * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    # faint horizon glow behind product
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W * 0.22, H * 0.08, W * 0.78, H * 0.85], fill=(255, 255, 255, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(60 * S))
    img.paste(Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- soft floor shadow under the strip ----
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.ellipse([150 * S, 520 * S, 830 * S, 590 * S], fill=(40, 50, 60, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(18 * S))
    img.paste(Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- cable: thick dark loop leaving right end, arcing down and back
    # up to plug into the leftmost socket ----
    cable_pts = []
    # bezier-ish path: start at right end of strip, sweep down-right,
    # loop low, come back up-left into socket 1
    import math
    def bez(p0, p1, p2, p3, n=60):
        pts = []
        for i in range(n + 1):
            t = i / n
            x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
            pts.append((x * S, y * S))
        return pts

    cable_pts = bez((745, 445), (880, 470), (900, 640), (700, 660))
    cable_pts += bez((700, 660), (480, 685), (330, 620), (300, 470))
    # cable body (dark grey with lighter top edge highlight)
    d.line(cable_pts, fill=(52, 58, 66), width=15 * S, joint="curve")
    d.line(cable_pts, fill=(96, 104, 114), width=5 * S, joint="curve")

    # ---- power strip body: sleek white slab, slight perspective top ----
    # top face
    d.polygon([(180 * S, 400 * S), (760 * S, 400 * S), (745 * S, 378 * S),
               (195 * S, 378 * S)], fill=(226, 230, 234))
    # front face
    d.rounded_rectangle([180 * S, 395 * S, 760 * S, 505 * S], radius=18 * S,
                        fill=(250, 251, 252), outline=(196, 202, 208), width=2 * S)
    # top highlight line
    d.line([(195 * S, 402 * S), (745 * S, 402 * S)], fill=(255, 255, 255), width=3 * S)
    # bottom shade line
    d.line([(195 * S, 498 * S), (745 * S, 498 * S)], fill=(214, 219, 224), width=3 * S)

    # ---- six sockets on the top face ----
    for i in range(6):
        x0 = (205 + i * 82) * S
        y0 = 408 * S
        d.rounded_rectangle([x0, y0, x0 + 58 * S, y0 + 58 * S], radius=10 * S,
                            fill=(238, 240, 242), outline=(200, 206, 212), width=2 * S)
        # three pin holes
        for hx, hy in ((15, 16), (43, 16), (29, 40)):
            d.ellipse([x0 + hx * S - 4 * S, y0 + hy * S - 5 * S,
                       x0 + hx * S + 4 * S, y0 + hy * S + 5 * S],
                      fill=(38, 42, 48))
    # leftmost socket is occupied by the plug: cover its holes with plug prongs
    # ---- plug head entering socket 1 ----
    d.rounded_rectangle([232 * S, 452 * S, 300 * S, 486 * S], radius=8 * S,
                        fill=(52, 58, 66), outline=(30, 34, 40), width=2 * S)
    d.rounded_rectangle([246 * S, 424 * S, 286 * S, 456 * S], radius=6 * S,
                        fill=(70, 76, 86))
    # prongs into the socket
    d.rectangle([252 * S, 408 * S, 260 * S, 428 * S], fill=(180, 184, 190))
    d.rectangle([272 * S, 408 * S, 280 * S, 428 * S], fill=(180, 184, 190))

    # ---- rocker switch + glowing LED on front face (right of last socket) ----
    d.rounded_rectangle([700 * S, 452 * S, 748 * S, 488 * S], radius=8 * S,
                        fill=(226, 229, 233), outline=(190, 196, 202), width=2 * S)
    d.line([(724 * S, 456 * S), (724 * S, 484 * S)], fill=(120, 126, 134), width=3 * S)
    # LED glow
    led = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(led)
    ld.ellipse([676 * S, 460 * S, 696 * S, 480 * S], fill=(60, 220, 120, 110))
    led = led.filter(ImageFilter.GaussianBlur(6 * S))
    img.paste(Image.alpha_composite(img.convert("RGBA"), led).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    d.ellipse([680 * S, 464 * S, 692 * S, 476 * S], fill=(46, 200, 110),
              outline=(20, 140, 70), width=2 * S)

    # ---- brand label on front face ----
    d.text((315 * S, 466 * S), "SELF-POWERED™", font=font(14), fill=(90, 96, 104))
    d.text((315 * S, 485 * S), "Model SP-∞  •  0 W from the wall, forever",
           font=font_reg(10), fill=(140, 146, 152))

    # ---- screws at both ends of the strip ----
    for sx in (196, 744):
        d.ellipse([sx * S, 486 * S, (sx + 10) * S, 496 * S], fill=(200, 205, 211),
                  outline=(160, 166, 172), width=1 * S)
        d.line([(sx + 2) * S, 491 * S, (sx + 8) * S, 491 * S], fill=(140, 146, 152), width=1 * S)

    # ---- ONE accessory: paper electricity bill leaning at the right ----
    bill = Image.new("RGBA", (340 * S, 460 * S), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bill)
    bd.rectangle([10 * S, 10 * S, 330 * S, 450 * S], fill=(255, 255, 255, 255),
                 outline=(205, 210, 215), width=2 * S)
    bd.rectangle([10 * S, 10 * S, 330 * S, 66 * S], fill=(42, 52, 64, 255))
    bd.text((28 * S, 26 * S), "ELECTRICITY BILL", font=font(20), fill=(255, 255, 255))
    bd.text((28 * S, 92 * S), "Account: SELF-POWERED", font=font_reg(15), fill=(70, 76, 84))
    bd.text((28 * S, 122 * S), "Period: Nov 2026", font=font_reg(15), fill=(70, 76, 84))
    bd.text((28 * S, 152 * S), "Usage: 0 kWh", font=font_reg(15), fill=(70, 76, 84))
    bd.line([(28 * S, 196 * S), (312 * S, 196 * S)], fill=(210, 214, 218), width=2 * S)
    bd.text((28 * S, 216 * S), "AMOUNT DUE", font=font(16), fill=(70, 76, 84))
    bd.text((28 * S, 250 * S), "$0.00", font=font(58), fill=(24, 160, 90))
    bd.text((28 * S, 340 * S), "Thank you for using", font=font_reg(14), fill=(120, 126, 134))
    bd.text((28 * S, 364 * S), "absolutely nothing.", font=font_reg(14), fill=(120, 126, 134))
    bill = bill.resize((250 * S, 338 * S), Image.LANCZOS)
    bill = bill.rotate(-7, expand=True, resample=Image.BICUBIC)
    # shadow behind bill
    bsh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bsd = ImageDraw.Draw(bsh)
    bsd.rectangle([800 * S, 480 * S, 985 * S, 600 * S], fill=(40, 50, 60, 55))
    bsh = bsh.filter(ImageFilter.GaussianBlur(10 * S))
    img.paste(Image.alpha_composite(img.convert("RGBA"), bsh).convert("RGB"), (0, 0))
    img.paste(bill, (740 * S, 195 * S), bill)

    # ---- downscale to final size ----
    img = img.resize((1024, 768), Image.LANCZOS)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(os.getcwd(), "out")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, "PNG", optimize=True)
    print("wrote", out_path, img.size, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    main()
