"""Generate a high-contrast black & white postcard for MindAR + mono printers."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "postcard.png"
QR_PATH = ROOT / "assets" / "qr.png"

W, H = 1200, 1600
BLACK, WHITE = "#000000", "#ffffff"

img = Image.new("RGB", (W, H), WHITE)
draw = ImageDraw.Draw(img)

# Outer checkerboard frame — dense high-contrast features for tracking
cell = 40
for y in range(0, H, cell):
    for x in range(0, W, cell):
        if ((x // cell) + (y // cell)) % 2 == 0:
            draw.rectangle([x, y, x + cell - 1, y + cell - 1], fill=BLACK)

# Inner white card
margin = 100
draw.rounded_rectangle(
    [margin, margin, W - margin, H - margin],
    radius=28,
    fill=WHITE,
    outline=BLACK,
    width=10,
)

# Asymmetric corner marks (orientation cues, not just decoration)
# top-left: concentric squares
for i, s in enumerate((90, 60, 30)):
    x0, y0 = margin + 40, margin + 40
    draw.rectangle([x0, y0, x0 + s, y0 + s], outline=BLACK, width=6 if i == 0 else 4)
# top-right: bullseye
cx, cy = W - margin - 85, margin + 85
for r in (70, 45, 22):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLACK, width=6)
draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=BLACK)
# bottom-left: diagonal stripes block
bx0, by0 = margin + 40, H - margin - 200
for i in range(-4, 10):
    x = bx0 + i * 18
    draw.line([(x, by0), (x + 120, by0 + 120)], fill=BLACK, width=8)
draw.rectangle([bx0, by0, bx0 + 140, by0 + 140], outline=BLACK, width=6)

# Center feature field — unique dotted / cross pattern (fills the "empty cream" problem)
for row in range(8):
    for col in range(6):
        x = 280 + col * 110
        y = 420 + row * 70
        if (row + col) % 2 == 0:
            draw.rectangle([x - 18, y - 18, x + 18, y + 18], outline=BLACK, width=3)
            draw.line([(x - 12, y), (x + 12, y)], fill=BLACK, width=3)
            draw.line([(x, y - 12), (x, y + 12)], fill=BLACK, width=3)
        else:
            draw.ellipse([x - 16, y - 16, x + 16, y + 16], outline=BLACK, width=3)
            draw.ellipse([x - 5, y - 5, x + 5, y + 5], fill=BLACK)

try:
    font_lg = ImageFont.truetype("arialbd.ttf", 78)
    font_md = ImageFont.truetype("arial.ttf", 34)
    font_sm = ImageFont.truetype("arial.ttf", 26)
except OSError:
    try:
        font_lg = ImageFont.truetype("arial.ttf", 78)
        font_md = ImageFont.truetype("arial.ttf", 34)
        font_sm = ImageFont.truetype("arial.ttf", 26)
    except OSError:
        font_lg = font_md = font_sm = ImageFont.load_default()

draw.text((W // 2, 220), "QUACK AR", fill=BLACK, font=font_lg, anchor="mm")
draw.text((W // 2, 290), "Point camera at this card", fill=BLACK, font=font_md, anchor="mm")

# High-contrast duck silhouette
duck_y = 980
draw.ellipse([470, duck_y, 730, duck_y + 170], fill=WHITE, outline=BLACK, width=8)
draw.ellipse([650, duck_y - 50, 800, duck_y + 100], fill=WHITE, outline=BLACK, width=8)
draw.polygon([(800, duck_y + 20), (900, duck_y + 45), (800, duck_y + 70)], fill=BLACK)
draw.ellipse([720, duck_y - 15, 748, duck_y + 13], fill=BLACK)
# wing detail
draw.arc([520, duck_y + 40, 680, duck_y + 140], 200, 340, fill=BLACK, width=6)

# QR block
draw.text((W // 2, H - 470), "Scan QR to open AR", fill=BLACK, font=font_sm, anchor="mm")
qr_box = (W // 2 - 165, H - 445, W // 2 + 165, H - 115)
draw.rounded_rectangle(qr_box, radius=12, fill=WHITE, outline=BLACK, width=6)

if QR_PATH.exists():
    qr = Image.open(QR_PATH).convert("RGB").resize((300, 300))
    # Force pure B&W QR (remove anti-alias gray)
    qr = qr.point(lambda p: 0 if p < 128 else 255)
    img.paste(qr, (W // 2 - 150, H - 430))
else:
    draw.text((W // 2, H - 280), "QR HERE", fill=BLACK, font=font_md, anchor="mm")

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} ({OUT.stat().st_size} bytes) B&W")
