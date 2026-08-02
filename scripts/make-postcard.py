"""High-contrast B&W postcard — symmetric, clean layout for mono printers + MindAR."""
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

# --- Outer checkerboard frame (2 cells deep) ---
cell = 40
frame = cell * 2  # 80
for y in range(0, H, cell):
    for x in range(0, W, cell):
        on_edge = x < frame or y < frame or x >= W - frame or y >= H - frame
        if on_edge and ((x // cell) + (y // cell)) % 2 == 0:
            draw.rectangle([x, y, x + cell - 1, y + cell - 1], fill=BLACK)

pad = frame + 24  # 104 — inner content margin
draw.rectangle([pad, pad, W - pad - 1, H - pad - 1], outline=BLACK, width=6)

try:
    font_lg = ImageFont.truetype("arialbd.ttf", 70)
    font_md = ImageFont.truetype("arial.ttf", 30)
    font_sm = ImageFont.truetype("arial.ttf", 24)
except OSError:
    try:
        font_lg = ImageFont.truetype("arial.ttf", 70)
        font_md = ImageFont.truetype("arial.ttf", 30)
        font_sm = ImageFont.truetype("arial.ttf", 24)
    except OSError:
        font_lg = font_md = font_sm = ImageFont.load_default()

# --- Title ---
draw.text((CX, 175), "QUACK AR", fill=BLACK, font=font_lg, anchor="mm")
draw.text((CX, 240), "Point camera at this card", fill=BLACK, font=font_md, anchor="mm")

# --- Four identical corner bullseyes (symmetric) ---
def corner_mark(cx, cy):
    for r in (44, 28, 12):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLACK, width=4)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=BLACK)

c = pad + 78
corner_mark(c, c)
corner_mark(W - c, c)
corner_mark(c, H - c)
corner_mark(W - c, H - c)

# --- Centered 7x5 feature grid ---
cols, rows = 7, 5
spacing_x, spacing_y = 96, 72
grid_w = (cols - 1) * spacing_x
grid_h = (rows - 1) * spacing_y
grid_left = (W - grid_w) // 2
grid_top = 310

for row in range(rows):
    for col in range(cols):
        x = grid_left + col * spacing_x
        y = grid_top + row * spacing_y
        if (row + col) % 2 == 0:
            s = 15
            draw.rectangle([x - s, y - s, x + s, y + s], outline=BLACK, width=3)
            draw.line([(x - 9, y), (x + 9, y)], fill=BLACK, width=3)
            draw.line([(x, y - 9), (x, y + 9)], fill=BLACK, width=3)
        else:
            draw.ellipse([x - 13, y - 13, x + 13, y + 13], outline=BLACK, width=3)
            draw.ellipse([x - 4, y - 4, x + 4, y + 4], fill=BLACK)

# Divider — same inset from both sides
rule_y = grid_top + grid_h + 42
draw.line([(pad + 60, rule_y), (W - pad - 60, rule_y)], fill=BLACK, width=3)

# --- Duck: shift so full silhouette (body+beak) is centered on CX ---
# Local duck coords designed around origin; then offset so bbox center == CX
# body ~(-120,-35)-(80,95), head~(35,-90)-(155,20), beak tip ~235
# visual bbox approx x: -120 .. 235  → width 355, center at (-120+235)/2 = 57.5
# so place origin at CX - 58
ox = CX - 58
oy = 780  # raised so clear air above QR caption

draw.ellipse([ox - 120, oy - 35, ox + 80, oy + 95], fill=WHITE, outline=BLACK, width=6)
draw.ellipse([ox + 35, oy - 90, ox + 155, oy + 20], fill=WHITE, outline=BLACK, width=6)
draw.polygon(
    [(ox + 155, oy - 40), (ox + 230, oy - 18), (ox + 155, oy)],
    fill=BLACK,
)
draw.ellipse([ox + 90, oy - 55, ox + 110, oy - 35], fill=BLACK)
draw.arc([ox - 85, oy - 5, ox + 35, oy + 80], 200, 340, fill=BLACK, width=5)

# Duck bottom ~875; keep generous whitespace before caption
qr_size = 260
caption_y = 1020
qr_top = 1060
qr_left = CX - qr_size // 2

draw.text((CX, caption_y), "Scan QR to open AR", fill=BLACK, font=font_sm, anchor="mm")
draw.rectangle(
    [qr_left - 10, qr_top - 10, qr_left + qr_size + 10, qr_top + qr_size + 10],
    outline=BLACK,
    width=4,
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
