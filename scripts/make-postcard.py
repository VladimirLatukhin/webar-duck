"""Generate a high-contrast postcard image for MindAR tracking + QR placeholder."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "postcard.png"
QR_PATH = ROOT / "assets" / "qr.png"  # optional; generated later

W, H = 1200, 1600
img = Image.new("RGB", (W, H), "#1a3a5c")
draw = ImageDraw.Draw(img)

# Colorful bands / pattern for feature points
palette = ["#f4a261", "#e76f51", "#2a9d8f", "#e9c46a", "#264653", "#ffb703", "#8ecae6"]
for i, y0 in enumerate(range(0, H, 80)):
    draw.rectangle([0, y0, W, y0 + 80], fill=palette[i % len(palette)])

# Soft vignette card
margin = 60
draw.rounded_rectangle(
    [margin, margin, W - margin, H - margin],
    radius=48,
    fill="#fff8f0",
    outline="#d4a017",
    width=8,
)

# Decorative circles
for cx, cy, r, c in [
    (220, 280, 90, "#2a9d8f"),
    (980, 320, 70, "#e76f51"),
    (180, 1200, 110, "#e9c46a"),
    (1000, 1100, 85, "#8ecae6"),
    (600, 700, 40, "#f4a261"),
]:
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

# Title block
try:
    font_lg = ImageFont.truetype("arial.ttf", 72)
    font_md = ImageFont.truetype("arial.ttf", 36)
    font_sm = ImageFont.truetype("arial.ttf", 28)
except OSError:
    font_lg = ImageFont.load_default()
    font_md = font_lg
    font_sm = font_lg

draw.text((W // 2, 260), "QUACK AR", fill="#264653", font=font_lg, anchor="mm")
draw.text((W // 2, 340), "Point your camera here", fill="#6b5b4f", font=font_md, anchor="mm")

# Duck silhouette hint (simple)
duck_y = 720
draw.ellipse([480, duck_y, 720, duck_y + 160], fill="#ffb703", outline="#264653", width=4)
draw.ellipse([650, duck_y - 40, 780, duck_y + 90], fill="#ffb703", outline="#264653", width=4)
draw.polygon([(780, duck_y + 20), (860, duck_y + 40), (780, duck_y + 55)], fill="#e76f51")
draw.ellipse([720, duck_y - 10, 740, duck_y + 10], fill="#264653")

# QR slot (bottom) — white square; qr.png composited if present
qr_box = (W // 2 - 160, H - 420, W // 2 + 160, H - 100)
draw.rounded_rectangle(qr_box, radius=16, fill="white", outline="#264653", width=4)
draw.text((W // 2, H - 450), "Scan QR to open AR", fill="#264653", font=font_sm, anchor="mm")

if QR_PATH.exists():
    qr = Image.open(QR_PATH).convert("RGB").resize((300, 300))
    img.paste(qr, (W // 2 - 150, H - 410))
else:
    draw.text((W // 2, H - 260), "QR HERE", fill="#999", font=font_md, anchor="mm")

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
