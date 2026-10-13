"""Process the user-supplied clean icon (static/img/source/mark-new.png) into
transparent PNGs for header use: a navy variant (light theme) and a cream
variant (dark theme, so the "E" stays legible against a dark header bg)."""
from PIL import Image, ImageFilter
import numpy as np

SRC = "static/img/source/mark-new.png"
BG = np.array([229, 253, 229], dtype=float)
NAVY = np.array([11, 29, 46], dtype=float)
CREAM = np.array([234, 247, 236], dtype=float)

im = Image.open(SRC).convert("RGB")
arr = np.array(im, dtype=float)

# near-binary alpha: narrow transition band so there is no wide, noisy
# semi-transparent halo once composited on a dark background.
diff_bg = np.abs(arr - BG).sum(axis=2)
alpha01 = np.clip((diff_bg - 18) / (30 - 18), 0, 1)

# smooth the mask slightly (kills jagged/speckled edges from the small source)
alpha_img = Image.fromarray((alpha01 * 255).astype(np.uint8))
alpha_img = alpha_img.filter(ImageFilter.GaussianBlur(radius=0.6))
alpha01 = np.array(alpha_img, dtype=float) / 255.0
alpha = alpha01 * 255

# classify navy vs gold on the ORIGINAL (non-decontaminated) colors —
# stable even near edges, unlike un-premultiplied colors.
diff_navy = np.abs(arr - NAVY).sum(axis=2)
navy_frac = np.clip(1 - (diff_navy - 60) / (200 - 60), 0, 1)  # 1=navy, 0=not navy
navy_frac = navy_frac * (alpha01 > 0.05)

def save(rgb_arr, path, upscale=5):
    rgba = np.dstack([rgb_arr, alpha]).astype(np.uint8)
    out = Image.fromarray(rgba, mode="RGBA")
    out = out.resize((out.width * upscale, out.height * upscale), Image.LANCZOS)
    out.save(path)

# light-theme variant: original colors, cleaned-up alpha only
save(arr, "static/img/mark-light.png")

# dark-theme variant: fade navy areas toward cream, leave gold untouched
blend = navy_frac[..., None]
dark_arr = arr * (1 - blend) + CREAM * blend
save(dark_arr, "static/img/mark-dark.png")

print("done")
