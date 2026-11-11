"""Recolour the contest's blank case template into the 'Blueprint Case' livery.

Usage: python3 -I recolor.py TEMPLATE.png OUT_DIR [overlays_dir]
Writes OUT_DIR/base.png (recoloured case, RGBA) and masks used by the overlay pass.
If overlays_dir is given (paint.png, spray.png, stickers.png at template size),
composites them with the case's own shading into OUT_DIR/final.png.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

TPL, OUT = sys.argv[1], sys.argv[2]
OVL = sys.argv[3] if len(sys.argv) > 3 else None
PALETTE = sys.argv[4] if len(sys.argv) > 4 else 'blueprint'

im = Image.open(TPL).convert("RGBA")
Wd, Ht = im.size
arr = np.asarray(im).astype(np.float32) / 255.0
rgb, alpha = arr[..., :3], arr[..., 3]
L = rgb @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
inside = alpha > 0.5
p1, p99 = np.percentile(L[inside], [1, 99.5])
Ln = np.clip((L - p1) / (p99 - p1), 0, 1)


def poly_mask(polys, feather=1.5):
    m = Image.new("L", (Wd, Ht), 0)
    d = ImageDraw.Draw(m)
    for p in polys:
        d.polygon(p, fill=255)
    if feather:
        m = m.filter(ImageFilter.GaussianBlur(feather))
    return np.asarray(m).astype(np.float32) / 255.0


# --- hardware that stays bare metal -------------------------------------------------
METAL = [
    [(906, 395), (1120, 395), (1120, 975), (1100, 985), (925, 985), (906, 975)],  # left latch column
    [(1947, 395), (2172, 395), (2172, 968), (2150, 978), (1965, 978), (1947, 968)],  # right latch column
    [(310, 276), (464, 276), (472, 622), (316, 622)],                         # side handle
    [(605, 425), (863, 425), (863, 528), (803, 593), (655, 593), (605, 517)], # pillar top cap
    [(76, 378), (140, 378), (140, 495), (78, 540)],                           # left top cap
    [(2180, 410), (2282, 423), (2292, 565), (2282, 592), (2255, 588), (2180, 517)],  # right top cap
    [(604, 1140), (652, 1088), (762, 1088), (872, 1168), (872, 1305),
     (893, 1308), (893, 1400), (600, 1400)],                                  # pillar bottom cap + foot
    [(74, 1050), (136, 1050), (136, 1282), (192, 1282), (192, 1352), (88, 1352), (74, 1300)],
    [(898, 1072), (1102, 1072), (1102, 1362), (898, 1362)],                   # front-left bottom block
    [(1948, 1062), (2142, 1062), (2142, 1356), (1948, 1356)],                 # front-right bottom block
    [(2168, 1058), (2298, 1058), (2298, 1382), (2138, 1382), (2138, 1300), (2168, 1262)],
]
STRAPS = [
    [(822, 76), (1004, 76), (1062, 214), (1106, 300), (1112, 394), (934, 394), (921, 310), (866, 214)],
    [(1867, 76), (2049, 76), (2107, 210), (2151, 300), (2157, 394), (1991, 394), (1977, 305), (1916, 210)],
]
# blueprint "sheets" (recessed panels that get the grid)
SHEETS = [
    [(1200, 536), (1805, 536), (1832, 562), (1832, 1118), (1700, 1118), (1660, 1150),
     (1370, 1150), (1330, 1118), (1176, 1118), (1176, 562)],                 # front recessed panel
    [(258, 598), (495, 598), (495, 1100), (258, 1100)],                       # side door panel (below handle)
]

metal = poly_mask(METAL)
strap = poly_mask(STRAPS)
sheet = poly_mask(SHEETS, feather=1)

# sponsor logo: keep original white/cyan pixels
lb = np.zeros_like(L, dtype=bool)
lb[145:275, 1135:1865] = True
r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
cyan = lb & ((b - r) > 0.18)
white = lb & (np.min(rgb, axis=2) > 0.95)
# morphological opening removes the lid's bright speckles but keeps letter strokes
white_img = Image.fromarray((white * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(7)).filter(ImageFilter.MaxFilter(9))
logo = cyan | (np.asarray(white_img) > 0)
logo_img = Image.fromarray((logo * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1.2))
logo_m = np.asarray(logo_img).astype(np.float32) / 255.0


def gradient_map(x, stops):
    xs = np.array([s[0] for s in stops], dtype=np.float32)
    cs = np.array([s[1] for s in stops], dtype=np.float32) / 255.0
    out = np.empty(x.shape + (3,), dtype=np.float32)
    for c in range(3):
        out[..., c] = np.interp(x, xs, cs[:, c])
    return out


BLUE = [(0.0, (2, 8, 24)), (0.22, (6, 30, 78)), (0.5, (16, 70, 160)),
        (0.72, (32, 104, 210)), (0.88, (80, 150, 240)), (0.97, (140, 190, 250)), (1.0, (175, 210, 252))]
SHEET = [(0.0, (2, 10, 30)), (0.25, (8, 40, 100)), (0.55, (18, 78, 172)),
         (0.8, (38, 116, 222)), (0.95, (120, 178, 248)), (1.0, (220, 236, 255))]
BLACK = [(0.0, (3, 3, 4)), (0.3, (12, 12, 14)), (0.6, (30, 30, 34)), (0.8, (62, 62, 66)),
         (0.93, (128, 124, 114)), (1.0, (196, 188, 168))]
PLAQUE = [(0.0, (4, 3, 1)), (0.35, (16, 13, 6)), (0.65, (34, 29, 14)), (0.88, (72, 62, 32)), (1.0, (150, 132, 80))]
YELLOW = [(0.0, (28, 20, 0)), (0.35, (150, 112, 0)), (0.62, (232, 186, 0)), (0.82, (255, 220, 24)), (1.0, (255, 246, 190))]
GOLD = [(0.0, (18, 11, 2)), (0.3, (92, 60, 12)), (0.55, (176, 126, 34)), (0.75, (228, 184, 82)),
        (0.9, (255, 228, 150)), (1.0, (255, 250, 228))]
NEON_BODY = [(0.0, (1, 1, 2)), (0.35, (5, 5, 7)), (0.65, (14, 14, 18)), (0.85, (34, 34, 40)),
             (0.95, (74, 74, 84)), (1.0, (140, 140, 155))]
GUNMETAL = [(0.0, (2, 2, 3)), (0.4, (18, 19, 22)), (0.7, (48, 50, 55)), (0.9, (100, 102, 110)), (1.0, (180, 182, 192))]
if PALETTE == 'legends':
    BLUE, SHEET = BLACK, PLAQUE
if PALETTE == 'neon':
    BLUE, SHEET = NEON_BODY, NEON_BODY
blue = gradient_map(Ln, BLUE)
sheet_blue = gradient_map(Ln, SHEET)

# hazard stripes for straps, shaded by the metal underneath
yy, xx = np.mgrid[0:Ht, 0:Wd]
stripe = (((xx + yy) // 46) % 2 == 0)
yel = np.array([1.0, 0.86, 0.0], dtype=np.float32)
blk = np.array([0.07, 0.07, 0.08], dtype=np.float32)
haz_col = np.where(stripe[..., None], yel, blk)
shade = np.clip(0.18 + 1.05 * Ln, 0.12, 1.15)[..., None]
haz = np.clip(haz_col * shade + np.clip(Ln - 0.9, 0, 1)[..., None] * 2.5, 0, 1)

metal_rgb = np.clip(rgb * 0.9, 0, 1)
if PALETTE == 'legends':
    haz = gradient_map(np.clip(Ln * 1.05, 0, 1), YELLOW)    # solid NAVI-yellow straps
    metal_rgb = gradient_map(Ln, GOLD)                     # gold hardware
if PALETTE == 'neon':
    haz = gradient_map(Ln, NEON_BODY)                      # straps stay black; neon traces their edges
    metal_rgb = gradient_map(Ln, GUNMETAL)                 # dark gunmetal hardware

out = blue
out = out * (1 - sheet[..., None]) + sheet_blue * sheet[..., None]
out = out * (1 - strap[..., None]) + haz * strap[..., None]
out = out * (1 - metal[..., None]) + metal_rgb * metal[..., None]
out = out * (1 - logo_m[..., None]) + rgb * logo_m[..., None]

np.save(f"{OUT}/Ln.npy", Ln)
paintable = np.clip(1 - metal - strap - logo_m, 0, 1)
np.save(f"{OUT}/paintable.npy", paintable)


def save(rgbf, name):
    a8 = (np.clip(rgbf, 0, 1) * 255).astype(np.uint8)
    Image.fromarray(np.dstack([a8, (alpha * 255).astype(np.uint8)]), "RGBA").save(f"{OUT}/{name}")


save(out, "base.png")

if OVL:
    def load(name):
        a = np.asarray(Image.open(f"{OVL}/{name}").convert("RGBA")).astype(np.float32) / 255.0
        return a[..., :3], a[..., 3]

    # printed photos: keep them vivid but let the panel's shading and texture through a little
    import os
    if os.path.exists(f"{OVL}/photo.png"):
        c, a = load("photo.png")
        a = a * paintable
        ph_shade = np.clip(0.62 + 0.42 * Ln, 0.55, 1.06)[..., None]
        out = out * (1 - a[..., None]) + np.clip(c * ph_shade, 0, 1) * a[..., None]
    # painted layers follow the surface shading (darker in crevices, scratches show through)
    paint_shade = np.clip(0.30 + 0.95 * Ln, 0.25, 1.12)[..., None]
    for name, mask_to_paintable in (("paint.png", True), ("spray.png", True)):
        c, a = load(name)
        if mask_to_paintable:
            a = a * paintable
        # paint wear: let bright scratches/edges of the metal break through the paint a little
        a = a * np.clip(1.15 - np.clip(Ln - 0.86, 0, 1) * 4.0, 0, 1)
        out = out * (1 - a[..., None]) + np.clip(c * paint_shade, 0, 1) * a[..., None]
    c, a = load("stickers.png")
    st_shade = np.clip(0.62 + 0.45 * Ln, 0.5, 1.08)[..., None]
    out = out * (1 - a[..., None]) + np.clip(c * st_shade, 0, 1) * a[..., None]
    out = out * (1 - logo_m[..., None]) + rgb * logo_m[..., None]
    save(out, "final.png")
print("ok", (p1, p99))
