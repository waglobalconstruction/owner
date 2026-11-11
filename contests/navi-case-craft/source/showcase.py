"""Gold-glow showcase background for a finished case PNG.

Usage: python3 -I showcase.py CASE.png OUT.png
"""
import random
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

case = Image.open(sys.argv[1]).convert("RGBA")
W, H = case.size
px, pt, pb = 170, 170, 230
CW, CH = W + 2 * px, H + pt + pb
yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
cx, cy = CW * 0.5, pt + H * 0.48
r = np.sqrt(((xx - cx) / (CW * 0.62)) ** 2 + ((yy - cy) / (CH * 0.7)) ** 2)
base, edge = np.array([30, 27, 22], np.float32), np.array([6, 6, 8], np.float32)
t = np.clip(r, 0, 1)[..., None]
img = base * (1 - t) + edge * t
ang = np.arctan2(yy - cy, xx - cx)
img += ((0.5 + 0.5 * np.cos(ang * 18)) ** 6 * np.exp(-r * 1.6))[..., None] * np.array([120, 90, 20], np.float32) * 0.55
img += np.exp(-(r / 0.55) ** 2)[..., None] * np.array([90, 64, 10], np.float32)
bg = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

sh = Image.new("L", (CW, CH), 0)
ImageDraw.Draw(sh).ellipse([px + 60, pt + 1330, px + W - 60, pt + 1440], fill=220)
gl = Image.new("L", (CW, CH), 0)
ImageDraw.Draw(gl).ellipse([px - 160, pt + 1290, px + W + 160, pt + 1580], fill=80)
bg = Image.composite(Image.new("RGBA", (CW, CH), (255, 200, 40, 255)), bg, gl.filter(ImageFilter.GaussianBlur(80)))
bg = Image.composite(Image.new("RGBA", (CW, CH), (0, 0, 0, 255)), bg, sh.filter(ImageFilter.GaussianBlur(26)))

rnd = random.Random(5)
sp = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
d = ImageDraw.Draw(sp)
for _ in range(170):
    x, y = rnd.uniform(0, CW), rnd.uniform(0, CH * 0.95)
    rr = rnd.choice([1.2, 1.6, 2, 2.5, 3.5])
    d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(255, 214, 90, int(rnd.uniform(60, 220))))
bg.alpha_composite(sp.filter(ImageFilter.GaussianBlur(4)))
bg.alpha_composite(sp)
bg.alpha_composite(case, (px, pt))

# glints only on the silhouette edge
a = case.getchannel("A").point(lambda v: 255 if v > 128 else 0)
edge = np.asarray(a.filter(ImageFilter.MaxFilter(5)), dtype=np.int16) - np.asarray(a.filter(ImageFilter.MinFilter(5)), dtype=np.int16)
ys, xs = np.nonzero(edge > 0)
fr = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
d = ImageDraw.Draw(fr)
for i in rnd.sample(range(len(xs)), 12):
    x, y, s = xs[i] + px, ys[i] + pt, rnd.uniform(8, 16)
    d.polygon([(x, y - s), (x + s * .2, y - s * .2), (x + s, y), (x + s * .2, y + s * .2), (x, y + s),
               (x - s * .2, y + s * .2), (x - s, y), (x - s * .2, y - s * .2)], fill=(255, 240, 180, 215))
bg.alpha_composite(fr.filter(ImageFilter.GaussianBlur(0.6)))
bg.convert("RGB").save(sys.argv[2], optimize=True)
print("ok", bg.size)
