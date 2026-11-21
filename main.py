#!/usr/bin/env python3
"""Catalogue photo of an impossible gadget: a self-powered power strip.

The strip's own cable loops back and plugs into one of its own sockets,
so it powers itself forever. One accessory: the electricity bill for
$0.00 leaning beside it. Drawn entirely with PIL - no network, no assets.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 768

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except OSError:
        return ImageFont.load_default()

F_TITLE = font("DejaVuSans-Bold.ttf", 30)
F_MODEL = font("DejaVuSans-Bold.ttf", 20)
F_SMALL = font("DejaVuSans.ttf", 17)
F_BILL_H = font("DejaVuSans-Bold.ttf", 21)
F_BILL = font("DejaVuSans.ttf", 17)
F_BILL_BIG = font("DejaVuSans-Bold.ttf", 30)

# ---------- canvas: clean studio backdrop ----------
img = Image.new("RGB", (W, H), (238, 240, 243))
d = ImageDraw.Draw(img)
for y in range(H):
    # gentle vertical falloff: brighter top, slightly darker floor
    t = y / H
    g = int(247 - 9 * t)
    d.line([(0, y), (W, y)], fill=(g, g + 1, g + 3))
# soft horizon glow behind the product
glow = Image.new("RGB", (W, H), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([180, 90, 844, 640], fill=(255, 255, 255))
glow = glow.filter(ImageFilter.GaussianBlur(90))
img = Image.blend(img, glow, 0.35)
d = ImageDraw.Draw(img)

# ---------- floor shadow (soft, under the whole scene) ----------
shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([150, 560, 880, 660], fill=(60, 65, 75, 90))
shadow = shadow.filter(ImageFilter.GaussianBlur(18))
img.paste(shadow, (0, 0), shadow)
d = ImageDraw.Draw(img)

# ---------- the cable: exits right end, loops down, plugs into socket 1 ----------
# Draw cable BEFORE the strip body so the plug end sits on top later.
CABLE = (52, 56, 62)
cable_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
cd = ImageDraw.Draw(cable_layer)
# loop path: from strip right end, sweep down and left, rise into socket 1
pts = [(742, 478), (830, 505), (872, 562), (838, 624), (700, 642),
       (520, 634), (380, 602), (300, 556), (288, 528)]
cd.line(pts, fill=CABLE + (255,), width=17, joint="curve")
cd.line(pts, fill=(74, 79, 86, 255), width=9, joint="curve")
cable_layer = cable_layer.filter(ImageFilter.GaussianBlur(0.6))
img.paste(cable_layer, (0, 0), cable_layer)
d = ImageDraw.Draw(img)

# ---------- power strip body ----------
X0, Y0, X1, Y1 = 210, 392, 760, 516
# top face (slightly lighter, gives manufactured depth)
d.rounded_rectangle([X0, Y0 - 16, X1, Y1 - 8], radius=18, fill=(252, 253, 254))
d.rounded_rectangle([X0, Y0, X1, Y1], radius=18, fill=(233, 235, 238))
d.rounded_rectangle([X0, Y0, X1, Y1], radius=18, outline=(178, 184, 192), width=2)
# subtle top highlight line
d.line([(X0 + 20, Y0 + 4), (X1 - 20, Y0 + 4)], fill=(255, 255, 255), width=3)

# ---------- sockets: 4 outlets along the strip ----------
def socket(cx, cy, plugged=False):
    # recessed dark plate
    d.rounded_rectangle([cx - 52, cy - 34, cx + 52, cy + 34], radius=12,
                        fill=(64, 68, 74))
    d.rounded_rectangle([cx - 52, cy - 34, cx + 52, cy + 34], radius=12,
                        outline=(40, 44, 50), width=2)
    if plugged:
        # plug body sitting in the socket
        d.rounded_rectangle([cx - 34, cy - 26, cx + 34, cy + 26], radius=9,
                            fill=(38, 42, 47))
        d.rounded_rectangle([cx - 34, cy - 26, cx + 34, cy + 26], radius=9,
                            outline=(22, 25, 29), width=2)
        # plug prongs disappearing into the face
        d.rounded_rectangle([cx - 14, cy - 6, cx - 4, cy + 6], radius=2,
                            fill=(150, 155, 162))
        d.rounded_rectangle([cx + 4, cy - 6, cx + 14, cy + 6], radius=2,
                            fill=(150, 155, 162))
    else:
        # two slots + round ground hole (US duplex style)
        d.rounded_rectangle([cx - 22, cy - 14, cx - 12, cy + 2], radius=3,
                            fill=(28, 31, 36))
        d.rounded_rectangle([cx + 12, cy - 14, cx + 22, cy + 2], radius=3,
                            fill=(28, 31, 36))
        d.ellipse([cx - 6, cy + 12, cx + 6, cy + 24], fill=(28, 31, 36))
        # tiny screw heads at plate corners
        for sx, sy in ((cx - 44, cy - 26), (cx + 44, cy - 26),
                       (cx - 44, cy + 26), (cx + 44, cy + 26)):
            d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(140, 145, 152))

socket(292, 470, plugged=True)   # own plug lives here
socket(418, 470)
socket(544, 470)
socket(670, 470)

# ---------- plug where cable meets socket 1 (drawn over cable end) ----------
d.rounded_rectangle([262, 488, 322, 534], radius=10, fill=(38, 42, 47))
d.rounded_rectangle([262, 488, 322, 534], radius=10, outline=(22, 25, 29), width=2)
d.line([(322, 500), (338, 500)], fill=(38, 42, 47), width=12)
d.line([(322, 522), (338, 522)], fill=(38, 42, 47), width=12)

# ---------- brand + model text on the strip (own band above the sockets) ----------
d.text((268, 398), "SELF-POWERED", font=F_TITLE, fill=(38, 42, 47))
d.text((600, 404), "SP-\u221e", font=F_MODEL, fill=(120, 126, 134))

# ---------- green LED, glowing ----------
LED = (700, 412)
led_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(led_glow)
ld.ellipse([LED[0] - 22, LED[1] - 22, LED[0] + 22, LED[1] + 22],
           fill=(46, 204, 113, 110))
led_glow = led_glow.filter(ImageFilter.GaussianBlur(8))
img.paste(led_glow, (0, 0), led_glow)
d = ImageDraw.Draw(img)
d.ellipse([LED[0] - 9, LED[1] - 9, LED[0] + 9, LED[1] + 9],
          fill=(39, 174, 96), outline=(22, 120, 66), width=2)
d.ellipse([LED[0] - 4, LED[1] - 4, LED[0] + 2, LED[1] + 2], fill=(190, 245, 210))
d.text((716, 400), "ON", font=F_SMALL, fill=(60, 120, 80))

# ---------- switch on the strip's right end ----------
d.rounded_rectangle([726, 442, 748, 488], radius=6, fill=(205, 210, 216),
                    outline=(160, 166, 174), width=2)
d.line([(726, 465), (748, 465)], fill=(160, 166, 174), width=2)

# ---------- accessory: the $0.00 electricity bill, leaning ----------
bill = Image.new("RGBA", (190, 250), (0, 0, 0, 0))
bd = ImageDraw.Draw(bill)
bd.rounded_rectangle([4, 4, 186, 246], radius=4, fill=(255, 255, 255, 255))
bd.rounded_rectangle([4, 4, 186, 246], radius=4, outline=(200, 204, 210, 255), width=2)
bd.text((18, 16), "ELECTRIC BILL", font=F_BILL_H, fill=(40, 44, 50))
bd.line([(18, 48), (172, 48)], fill=(180, 184, 190), width=2)
bd.text((18, 62), "Account 0001", font=F_BILL, fill=(80, 85, 92))
bd.text((18, 88), "Usage:  0 kWh", font=F_BILL, fill=(80, 85, 92))
bd.text((18, 114), "AMOUNT DUE", font=F_BILL, fill=(80, 85, 92))
bd.text((18, 140), "$0.00", font=F_BILL_BIG, fill=(39, 174, 96))
bd.line([(18, 188), (172, 188)], fill=(180, 184, 190), width=2)
bd.text((18, 200), "Thank you!", font=F_BILL, fill=(120, 126, 134))
bill = bill.rotate(-7, expand=True, resample=Image.BICUBIC)
# bill shadow on the floor
bshadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
bsd = ImageDraw.Draw(bshadow)
bsd.polygon([(812, 640), (950, 640), (930, 600), (830, 600)],
            fill=(60, 65, 75, 70))
bshadow = bshadow.filter(ImageFilter.GaussianBlur(6))
img.paste(bshadow, (0, 0), bshadow)
img.paste(bill, (800, 400), bill)
d = ImageDraw.Draw(img)

# ---------- output ----------
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(os.getcwd(), "out")
os.makedirs(out_dir, exist_ok=True)
path = os.path.join(out_dir, "entry.png")
img.save(path, "PNG", optimize=True)
print("saved", path, img.size, os.path.getsize(path), "bytes")
