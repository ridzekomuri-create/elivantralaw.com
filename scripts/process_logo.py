"""One-off script: extract icon / full lockup from the supplied logo photo,
producing transparent PNGs used by the site (header, favicon, footer)."""
from PIL import Image
import numpy as np

SRC = "static/img/source/logo_source.jpg"
BG = np.array([229, 253, 229], dtype=float)

im = Image.open(SRC).convert("RGB")
arr = np.array(im, dtype=float)

def make_rgba(crop_box, pad=14, upscale=3):
    x0, y0, x1, y1 = crop_box
    x0 = max(0, x0 - pad)
    y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad)
    y1 = min(im.height, y1 + pad)
    sub = arr[y0:y1, x0:x1]
    diff = np.abs(sub - BG).sum(axis=2)
    # smooth alpha ramp for clean anti-aliased edges
    alpha = np.clip((diff - 8) / (45 - 8), 0, 1) * 255
    rgba = np.dstack([sub, alpha]).astype(np.uint8)
    out = Image.fromarray(rgba, mode="RGBA")
    if upscale != 1:
        out = out.resize((out.width * upscale, out.height * upscale), Image.LANCZOS)
    return out

icon = make_rgba((32, 34, 270, 319), pad=10, upscale=4)
icon.save("static/img/logo-icon.png")

full = make_rgba((32, 34, 1094, 320), pad=16, upscale=3)
full.save("static/img/logo-full.png")

# square favicon canvas (padded icon centered on transparent square)
icon_sq = make_rgba((32, 34, 270, 319), pad=30, upscale=4)
side = max(icon_sq.width, icon_sq.height)
canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
canvas.paste(icon_sq, ((side - icon_sq.width) // 2, (side - icon_sq.height) // 2), icon_sq)
canvas.save("static/img/favicon-source.png")
for sz in (32, 180, 512):
    canvas.resize((sz, sz), Image.LANCZOS).save(f"static/img/favicon-{sz}.png")

print("done", icon.size, full.size, canvas.size)
