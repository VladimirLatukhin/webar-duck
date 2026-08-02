"""B&W postcard for MindAR: asymmetric unique art, 4 different corners, QR same side.
No repetitive grid / checkerboard. Duck-only center scene.
"""
from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "postcard.png"
QR_PATH = ROOT / "assets" / "qr.png"

W, H = 1200, 1600
BLACK, WHITE = "#000000", "#ffffff"
CX = W // 2

img = Image.new("RGB", (W, H), WHITE)
draw = ImageDraw.Draw(img)

# Simple outer frame (not checkerboard)
margin = 48
draw.rectangle([margin, margin, W - margin - 1, H - margin - 1], outline=BLACK, width=8)
draw.rectangle([margin + 16, margin + 16, W - margin - 17, H - margin - 17], outline=BLACK, width=3)

try:
    font_lg = ImageFont.truetype("arialbd.ttf", 68)
    font_md = ImageFont.truetype("arial.ttf", 30)
    font_sm = ImageFont.truetype("arial.ttf", 24)
except OSError:
    try:
        font_lg = ImageFont.truetype("arial.ttf", 68)
        font_md = ImageFont.truetype("arial.ttf", 30)
        font_sm = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        font_lg = font_md = font_sm = ImageFont.load_default()

# Title
draw.text((CX, 130), "QUACK AR", fill=BLACK, font=font_lg, anchor="mm")
draw.text((CX, 190), "Point camera at this card", fill=BLACK, font=font_md, anchor="mm")

# --- Four DIFFERENT corner markers ---
def mark_tl(x, y):
    for s in (70, 48, 28):
        draw.arc([x - s, y - s, x + s, y + s], 180, 270, fill=BLACK, width=6)
    draw.line([(x - 70, y), (x - 20, y)], fill=BLACK, width=6)
    draw.line([(x, y - 70), (x, y - 20)], fill=BLACK, width=6)


def mark_tr(x, y):
    r_out, r_in = 55, 24
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        r = r_out if i % 2 == 0 else r_in
        pts.append((x + r * math.cos(ang), y + r * math.sin(ang)))
    draw.polygon(pts, outline=BLACK, fill=WHITE)
    draw.line(pts + [pts[0]], fill=BLACK, width=4)


def mark_bl(x, y):
    draw.polygon([(x - 55, y + 50), (x + 55, y + 50), (x, y - 55)], outline=BLACK, fill=WHITE)
    draw.line([(x - 55, y + 50), (x + 55, y + 50), (x, y - 55), (x - 55, y + 50)], fill=BLACK, width=5)
    draw.rectangle([x - 50, y + 58, x + 50, y + 72], fill=BLACK)


def mark_br(x, y):
    for r in (58, 40, 24):
        draw.arc([x - r, y - r, x + r, y + r], 40, 320, fill=BLACK, width=5)
    draw.rectangle([x - 14, y - 14, x + 14, y + 14], outline=BLACK, width=4)
    draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=BLACK)


# Tuned further inward so arcs/triangle clear the double frame
mark_tl(165, 165)
mark_tr(W - 130, 130)
mark_bl(175, H - 175)
mark_br(W - 130, H - 145)

# --- Large centered duck only ---
ox, oy = CX - 30, 680
s = 1.85

def sx(v):
    return ox + v * s

def sy(v):
    return oy + v * s

draw.ellipse([sx(-120), sy(-35), sx(80), sy(95)], fill=WHITE, outline=BLACK, width=8)
draw.ellipse([sx(35), sy(-90), sx(155), sy(20)], fill=WHITE, outline=BLACK, width=8)
draw.polygon(
    [(sx(155), sy(-40)), (sx(235), sy(-18)), (sx(155), sy(0))],
    fill=BLACK,
)
draw.ellipse([sx(95), sy(-55), sx(115), sy(-35)], fill=BLACK)
draw.arc([sx(-85), sy(-5), sx(40), sy(85)], 200, 340, fill=BLACK, width=7)

# --- QR block ---
qr_size = 240
caption_y = 1180
qr_top = 1220
qr_left = CX - qr_size // 2

draw.text((CX, caption_y), "Scan QR to open AR", fill=BLACK, font=font_sm, anchor="mm")
draw.rectangle(
    [qr_left - 10, qr_top - 10, qr_left + qr_size + 10, qr_top + qr_size + 10],
    outline=BLACK, width=4,
)

if QR_PATH.exists():
    qr = Image.open(QR_PATH).convert("L").resize((qr_size, qr_size))
    qr = qr.point(lambda p: 0 if p < 128 else 255).convert("RGB")
    img.paste(qr, (qr_left, qr_top))
else:
    draw.text((CX, qr_top + qr_size // 2), "QR HERE", fill=BLACK, font=font_md, anchor="mm")

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
