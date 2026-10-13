"""Rasterize the vector mark (static/img/mark.svg geometry) to PNG favicons.
Kept in sync manually with mark.svg's shape coordinates (100x120 viewbox)."""
from PIL import Image, ImageDraw

NAVY = (11, 29, 46, 255)
GOLD = (176, 141, 79, 255)

E_SHAPES = [
    [(8, 0), (80, 0), (92, 14), (62, 14), (54, 6), (8, 6)],
    [(8, 0), (24, 0), (24, 120), (8, 120)],
    [(8, 50), (54, 50), (64, 66), (32, 66), (24, 58), (8, 58)],
    [(8, 120), (80, 120), (92, 106), (62, 106), (54, 114), (8, 114)],
]

GOLD_RECTS = [
    (16, 8, 50, 16),
    (20, 16, 46, 22),
    (18, 22, 23, 100),
    (27, 22, 32, 100),
    (36, 22, 41, 100),
    (45, 22, 50, 100),
]

LINE_POINTS = [(16, 98), (40, 82), (58, 60), (88, 28)]
LINE_NODES = [(16, 98, 5.5), (40, 82, 5.5), (58, 60, 5.5), (88, 28, 7)]


def render(size: int) -> Image.Image:
    pad = size * 0.12
    scale = (size - 2 * pad) / 120
    ox = (size - 100 * scale) / 2
    oy = pad

    def T(pt):
        x, y = pt
        return (ox + x * scale, oy + y * scale)

    ss = 4  # supersample for smooth edges
    img = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    def T2(pt):
        x, y = T(pt)
        return (x * ss, y * ss)

    for shape in E_SHAPES:
        draw.polygon([T2(p) for p in shape], fill=NAVY)

    for (x0, y0, x1, y1) in GOLD_RECTS:
        draw.polygon([T2((x0, y0)), T2((x1, y0)), T2((x1, y1)), T2((x0, y1))], fill=GOLD)

    line_w = max(2, int(4.5 * scale * ss))
    draw.line([T2(p) for p in LINE_POINTS], fill=GOLD, width=line_w, joint="curve")
    for x, y, r in LINE_NODES:
        cx, cy = T2((x, y))
        rr = r * scale * ss
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=GOLD)

    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    for sz in (32, 180, 512):
        render(sz).save(f"static/img/favicon-{sz}.png")
    print("favicons rendered")
