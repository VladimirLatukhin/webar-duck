"""First postcard layout in high-contrast B&W (mono-printer friendly)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "postcard.png"
QR_PATH = ROOT / "assets" / "qr.png"

W, H = 1200, 1600
BLACK, WHITE = "#000000", "#ffffff"
CX = W // 2

img = Image.new("RGB", (W, H), WHITE)
draw = ImageDraw.Draw(img)

# Original vibe: horizontal color bands → now B&W stripes (80px)
band = 80
for i, y0 in enumerate(range(0, H, band)):
    if i % 2 == 0:
        draw.rectangle([0, y0, W, min(y0 + band - 1, H - 1)], fill=BLACK)

# Inner card — leave a thicker striped frame on all sides (like v1)
margin = 80
draw.rounded_rectangle(
    [margin, margin, W - margin, H - margin],
    radius=48,
    fill=WHITE,
    outline=BLACK,
    width=8,
)

# Four DIFFERENT filled ellipses — unique gray levels + sizes/shapes (no diagonal twins).
# Grayscale intensity matters for MindAR; pure mono pairs confuse matching.
ovals = [
    # TL — dark gray wide oval
    (240, 310, 100, 75, 40),
    # TR — medium gray tall oval
    (960, 320, 65, 95, 110),
    # BL — light gray round-ish
    (250, 1170, 88, 88, 180),
    # BR — near-black flat oval
    (940, 1140, 110, 60, 20),
    # Extra asymmetric accent near duck (not a twin of any corner)
    (500, 620, 55, 40, 90),
]
for cx, cy, rx, ry, gray in ovals:
    box = [cx - rx, cy - ry, cx + rx, cy + ry]
    g = max(0, min(255, int(gray)))
    draw.ellipse(box, fill=(g, g, g), outline=BLACK, width=4)

try:
    font_lg = ImageFont.truetype("arialbd.ttf", 72)
    font_md = ImageFont.truetype("arial.ttf", 36)
    font_sm = ImageFont.truetype("arial.ttf", 28)
except OSError:
    try:
        font_lg = ImageFont.truetype("arial.ttf", 72)
        font_md = ImageFont.truetype("arial.ttf", 36)
        font_sm = ImageFont.truetype("arial.ttf", 28)
    except OSError:
        font_lg = font_md = font_sm = ImageFont.load_default()

draw.text((CX, 260), "QUACK AR", fill=BLACK, font=font_lg, anchor="mm")
draw.text((CX, 340), "Point your camera here", fill=BLACK, font=font_md, anchor="mm")

# Duck (v1 composition)
duck_y = 700
draw.ellipse([460, duck_y, 760, duck_y + 190], fill=WHITE, outline=BLACK, width=7)
draw.ellipse([650, duck_y - 55, 820, duck_y + 105], fill=WHITE, outline=BLACK, width=7)
draw.polygon([(820, duck_y + 15), (930, duck_y + 45), (820, duck_y + 75)], fill=BLACK)
draw.ellipse([730, duck_y - 20, 760, duck_y + 10], fill=BLACK)
draw.arc([500, duck_y + 30, 700, duck_y + 160], 200, 340, fill=BLACK, width=5)

draw.text((CX, H - 450), "Scan QR to open AR", fill=BLACK, font=font_sm, anchor="mm")
draw.rounded_rectangle(
    [CX - 160, H - 420, CX + 160, H - 100],
    radius=16,
    fill=WHITE,
    outline=BLACK,
    width=5,
)

if QR_PATH.exists():
    qr = Image.open(QR_PATH).convert("L").resize((300, 300))
    qr = qr.point(lambda p: 0 if p < 128 else 255).convert("RGB")
    img.paste(qr, (CX - 150, H - 410))
else:
    draw.text((CX, H - 260), "QR HERE", fill=BLACK, font=font_md, anchor="mm")

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
