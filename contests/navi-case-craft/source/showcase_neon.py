"""Dark showcase with a glossy floor reflection for the neon case.

Usage: python3 -I showcase_neon.py CASE.png OUT.png
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

case = Image.open(sys.argv[1]).convert("RGBA")
W, H = case.size
px, pt, pb = 170, 150, 330
CW, CH = W + 2 * px, H + pt + pb
yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
cx, cy = CW * 0.5, pt + H * 0.5
r = np.sqrt(((xx - cx) / (CW * 0.6)) ** 2 + ((yy - cy) / (CH * 0.62)) ** 2)
img = np.array([16, 14, 10], np.float32) * np.clip(1 - r, 0, 1)[..., None] + 4
img += np.exp(-(r / 0.42) ** 2)[..., None] * np.array([46, 34, 4], np.float32)
bg = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

# glossy floor reflection
floor_y = pt + 1395
refl = case.transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(3))
ra = np.asarray(refl).astype(np.float32)
fade = np.clip(1 - np.arange(ra.shape[0]) / 420.0, 0, 1) ** 1.4 * 0.6
ra[..., 3] *= fade[:, None]
refl = Image.fromarray(ra.astype(np.uint8), "RGBA")
bg.alpha_composite(refl, (px, floor_y - (H - 1395)))
bg.alpha_composite(case, (px, pt))
bg.convert("RGB").save(sys.argv[2], optimize=True)
print("ok", bg.size)
