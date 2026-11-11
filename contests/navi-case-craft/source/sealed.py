"""'NAVI SEALED' — a chained, padlocked case that cannot hold the legend inside.

Usage: python3 -I sealed.py TEMPLATE.png BASE_DIR FONT_DIR OUT_DIR   (OUT_DIR holds chains/emit/stencil/hud.png)
  BASE_DIR: output of `recolor.py TEMPLATE BASE_DIR "" neon` (base.png, paintable.npy)
Writes OUT_DIR/sealed_case.png (template size, RGBA with glow halo) and
OUT_DIR/sealed_showcase.png (dark scene with rays, smoke and reflection).
"""
import math
import random
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

TPL, BASE, FONTS, OUT = sys.argv[1:5]
rng = random.Random(2009)

tpl = np.asarray(Image.open(TPL).convert("RGBA")).astype(np.float32) / 255
H, W = tpl.shape[:2]
alpha = tpl[..., 3]
L = tpl[..., :3] @ np.array([0.2126, 0.7152, 0.0722], np.float32)
base = np.asarray(Image.open(f"{BASE}/base.png").convert("RGBA")).astype(np.float32)[..., :3] / 255
paintable = np.load(f"{BASE}/paintable.npy").astype(np.float32)


def blur(m, r):
    im = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255


def to_arr(img):
    return np.asarray(img).astype(np.float32) / 255


# ---------------------------------------------------------------- cracks
crack_img = Image.new("L", (W, H), 0)
core_img = Image.new("L", (W, H), 0)
dc, dk = ImageDraw.Draw(crack_img), ImageDraw.Draw(core_img)
crack_ends = []


def crack(x, y, ang, width, length, depth=0):
    while length > 0:
        step = rng.uniform(14, 34)
        ang += rng.gauss(0, 0.55) if rng.random() < 0.16 else rng.gauss(0, 0.1)
        nx, ny = x + math.cos(ang) * step, y + math.sin(ang) * step
        w = max(1, int(round(width)))
        dc.line([(x, y), (nx, ny)], fill=255, width=w + 2, joint="curve")
        dk.line([(x, y), (nx, ny)], fill=255, width=max(1, int(w * 0.45)), joint="curve")
        width = max(1.0, width * 0.972)
        length -= step
        if depth < 3 and rng.random() < 0.07:
            crack(nx, ny, ang + rng.choice([-1, 1]) * rng.uniform(0.35, 0.9), width * 0.6,
                  length * rng.uniform(0.3, 0.7), depth + 1)
        x, y = nx, ny
    crack_ends.append((x, y))


def burst(cx, cy, n, wmin, wmax, lmin, lmax, a0=0.0, spread=2 * math.pi):
    for i in range(n):
        ang = a0 + spread * (i + rng.uniform(-0.3, 0.3)) / n
        crack(cx + math.cos(ang) * 30, cy + math.sin(ang) * 30, ang, rng.uniform(wmin, wmax), rng.uniform(lmin, lmax))


EPI = (1505, 900)
# cracks start around the padlock and run outward
for i in range(14):
    a = 2 * math.pi * i / 14 + rng.uniform(-0.15, 0.15)
    sx, sy = EPI[0] + math.cos(a) * 150, EPI[1] + math.sin(a) * 140
    crack(sx, sy, a + rng.gauss(0, 0.15), rng.uniform(12, 17), rng.uniform(260, 520))
# long fractures racing left across the latch, the corner pillar and the side
for y0, l in [(700, 1250), (880, 1150), (1010, 1050)]:
    crack(1190, y0, math.pi + rng.gauss(0, 0.12), rng.uniform(11, 14), l)
crack(1820, 760, 0.0 + rng.gauss(0, 0.1), 11, 520)       # and right, past the other latch
crack(1820, 980, 0.1, 9, 420)
# up through the lid gap into the lid
for x0 in (1300, 1500, 1700):
    crack(x0, 560, -math.pi / 2 + rng.gauss(0, 0.35), rng.uniform(9, 12), rng.uniform(380, 520))
crack(700, 470, -math.pi / 2 + 0.55, 9, 360)
crack(250, 700, math.pi / 2 + 0.25, 8, 380)

logo_box = np.zeros((H, W), np.float32)
logo_box[130:290, 1120:1880] = 1
allow = paintable * alpha * (1 - logo_box)
cr = to_arr(crack_img) * allow
co = to_arr(core_img) * allow

# ---------------------------------------------------------------- burned-in NAVI
font = ImageFont.truetype(f"{FONTS}/BlackOpsOne.ttf", 230)
txt = Image.new("L", (W, H), 0)
dt = ImageDraw.Draw(txt)
bb = dt.textbbox((0, 0), "NAVI", font=font)
tx, ty = EPI[0] - (bb[2] - bb[0]) / 2 - bb[0], EPI[1] - (bb[3] - bb[1]) / 2 - bb[1]
# (NAVI lives on the padlock in this version)
tm = to_arr(txt) * alpha
tm_core = to_arr(txt.filter(ImageFilter.MinFilter(9)))

# ---------------------------------------------------------------- light leaking from the lid gap
Lb = blur(L, 3)
leak = np.zeros_like(L)
for x in range(60, 2300):
    if alpha[340:470, x].max() < 0.5 or 905 <= x <= 1122 or 1945 <= x <= 2172 or 300 <= x <= 470:
        continue
    col = Lb[340:470, x].copy()
    col[alpha[340:470, x] < 0.5] = 9
    y = int(np.argmin(col)) + 340
    if col.min() > 0.12:
        continue
    leak[y - 5:y + 6, x] = 1.0
leak = blur(leak, 2)
for (x0, y0, x1, y1) in [(1185, 1135, 1305, 1215), (1700, 1135, 1815, 1215)]:
    sub = Lb[y0:y1, x0:x1]
    leak[y0:y1, x0:x1] = np.maximum(leak[y0:y1, x0:x1], (sub < 0.22).astype(np.float32))

# ---------------------------------------------------------------- compose the case
out = base.copy() * 1.15
Ln = np.load(f"{BASE}/Ln.npy")
st = np.asarray(Image.open(f"{OUT}/stencil.png").convert("RGBA")).astype(np.float32) / 255
st_a = st[..., 3] * paintable * np.clip(1.15 - np.clip(Ln - 0.86, 0, 1) * 4.0, 0, 1)
out = out * (1 - st_a[..., None]) + st[..., :3] * np.clip(0.3 + 0.95 * Ln, 0.25, 1.12)[..., None] * st_a[..., None]
src = np.clip(cr + tm + leak, 0, 1)
# charred, sunken edges around every fissure
char = blur(cr, 3)
out *= (1 - np.clip(char * 0.9, 0, 0.9))[..., None]
shadow = np.roll(np.roll(blur(cr + tm, 2), 3, axis=0), 2, axis=1)
out *= (1 - shadow * 0.5)[..., None]
charred = blur(to_arr(txt.filter(ImageFilter.MaxFilter(15))), 6)
out *= (1 - charred * 0.85)[..., None]
# metal heated around the rupture
heat = blur(src, 45) * 2.0 + blur(src, 130) * 2.0
HOT = np.array([1.0, 0.36, 0.02], np.float32)
out = 1 - (1 - out) * (1 - np.clip(heat[..., None] * HOT * 0.55, 0, 1))

WHITE = np.array([1.0, 0.98, 0.88], np.float32)
YEL = np.array([1.0, 0.82, 0.08], np.float32)
ORG = np.array([1.0, 0.48, 0.02], np.float32)


def glow(m, k=1.0):
    return (blur(m, 2)[..., None] * YEL * 1.6 + blur(m, 9)[..., None] * YEL * 1.1 +
            blur(m, 28)[..., None] * ORG * 1.0 + blur(m, 80)[..., None] * ORG * 0.8) * k


em = to_arr(Image.open(f"{OUT}/emit.png").convert("RGBA"))[..., 3]
light = glow(cr) + glow(leak, 1.5) + glow(em, 2.2)
# molten interior of the cracks and the letters
molten = np.clip(cr * 0.9, 0, 1)[..., None] * (YEL * 0.8 + 0.2) + tm[..., None] * ORG * 1.0
hotcore = np.clip(co, 0, 1)[..., None] * WHITE
out = np.clip(out * (1 - tm[..., None]) + molten * 1.0, 0, 1)
out = np.where(np.clip(co, 0, 1)[..., None] > 0.4, hotcore, out)
chains = to_arr(Image.open(f"{OUT}/chains.png").convert("RGBA"))
ch_a = chains[..., 3]
out = out * (1 - ch_a[..., None]) + chains[..., :3] * ch_a[..., None]
out = np.where(em[..., None] > 0.5, WHITE, out)
# letters: orange rim fading to a white-hot centre
inner = blur(tm_core, 3)[..., None]
out = out * (1 - inner) + (YEL * 0.6 + WHITE * 0.4) * inner
out = 1 - (1 - out) * (1 - np.clip(light * (1 - 0.8 * ch_a)[..., None], 0, 1))
# shiny edges pick up the fire
spec = np.clip(L - 0.55, 0, 1)[..., None] * 2.0
out = np.clip(out + spec * np.clip(light, 0, 1) * (1 - ch_a)[..., None] * np.array([1.0, 0.7, 0.2], np.float32), 0, 1)

# ---------------------------------------------------------------- lightning, embers, shards (can leave the case)
fx = Image.new("RGBA", (W, H), (0, 0, 0, 0))
df = ImageDraw.Draw(fx)
fx_glow_src = Image.new("L", (W, H), 0)
dg = ImageDraw.Draw(fx_glow_src)


def bolt(p0, p1, disp, depth):
    if depth == 0:
        return [p0, p1]
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    n = math.hypot(dx, dy) or 1
    off = rng.gauss(0, disp)
    m = (mx - dy / n * off, my + dx / n * off)
    return bolt(p0, m, disp / 2, depth - 1)[:-1] + bolt(m, p1, disp / 2, depth - 1)


bolt_specs = [((1180, 600), (1010, 470)), ((1830, 610), (2000, 470)), ((1840, 1050), (2060, 1120)),
              ((620, 1000), (520, 1140)), ((260, 700), (120, 590)), ((1300, 330), (1180, 180))]
for p0, p1 in bolt_specs:
    path = bolt(p0, p1, math.dist(p0, p1) * 0.22, 6)
    df.line(path, fill=(255, 250, 220, 255), width=3, joint="curve")
    dg.line(path, fill=255, width=7, joint="curve")
    k = rng.randint(2, max(3, len(path) - 2))
    sub = bolt(path[k], (path[k][0] + rng.uniform(-90, 90), path[k][1] + rng.uniform(-90, 90)), 25, 4)
    df.line(sub, fill=(255, 240, 190, 220), width=2)
    dg.line(sub, fill=200, width=5)

# embers: born on the cracks and the gap, flying out and up
cy_idx, cx_idx = np.nonzero(cr > 0.5)
ly_idx, lx_idx = np.nonzero(leak > 0.5)
for i in range(900):
    if i < 650 and len(cx_idx):
        j = rng.randrange(len(cx_idx)); x, y = float(cx_idx[j]), float(cy_idx[j])
    else:
        j = rng.randrange(len(lx_idx)); x, y = float(lx_idx[j]), float(ly_idx[j])
    vx, vy = x - EPI[0], y - EPI[1]
    n = math.hypot(vx, vy) or 1
    ang = math.atan2(vy / n - 1.1, vx / n) + rng.gauss(0, 0.35)
    dist = rng.expovariate(1 / 90)
    x, y = x + math.cos(ang) * dist, y + math.sin(ang) * dist
    ln = rng.uniform(4, 26)
    col = rng.choice([(255, 250, 220), (255, 215, 60), (255, 170, 30), (255, 120, 10)])
    a = int(rng.uniform(150, 255))
    wdt = rng.choice([1, 1, 2, 2, 3])
    df.line([(x, y), (x - math.cos(ang) * ln, y - math.sin(ang) * ln)], fill=col + (a,), width=wdt)
    dg.line([(x, y), (x - math.cos(ang) * ln, y - math.sin(ang) * ln)], fill=int(a * 0.8), width=wdt + 2)

# glowing shards of metal blown off the rupture
for i in range(0):  # shards disabled: read as specks at thumbnail size
    ang = rng.uniform(0, 2 * math.pi)
    dist = rng.uniform(330, 620)
    x, y = EPI[0] + math.cos(ang) * dist, EPI[1] + math.sin(ang) * dist * 0.8 - 40
    s = rng.uniform(14, 30)
    rot = rng.uniform(0, math.pi)
    poly = [(x + math.cos(rot + k * 2.1 + rng.uniform(-.3, .3)) * s * rng.uniform(.6, 1.2),
             y + math.sin(rot + k * 2.1 + rng.uniform(-.3, .3)) * s * rng.uniform(.6, 1.2)) for k in range(3)]
    tail = [(px_ - math.cos(ang) * 26, py_ - math.sin(ang) * 26) for px_, py_ in poly]
    df.polygon([poly[0], poly[1], tail[1], tail[0]], fill=(255, 140, 20, 70))
    df.polygon(poly, fill=(40, 30, 24, 255), outline=(255, 200, 70, 255), width=3)
    dg.polygon(poly, outline=255, width=4)

fxa = to_arr(fx)
fx_rgb, fx_a = fxa[..., :3], fxa[..., 3]
fxg = to_arr(fx_glow_src)
fx_light = blur(fxg, 3)[..., None] * YEL * 1.4 + blur(fxg, 14)[..., None] * ORG * 1.0

out = 1 - (1 - out) * (1 - np.clip(fx_light, 0, 1))
out = out * (1 - fx_a[..., None]) + fx_rgb * fx_a[..., None]

# halo outside the silhouette
halo_l = np.clip(light + fx_light, 0, 1)
halo_a = np.clip(halo_l.max(axis=2) * 1.3, 0, 1)
a_out = np.clip(np.maximum.reduce([alpha, halo_a * 0.85, fx_a]), 0, 1)
outside = (alpha < 0.5)[..., None]
out = np.where(outside, np.clip(halo_l * (1 - fx_a[..., None]) + fx_rgb * fx_a[..., None], 0, 1), out)
case_rgba = np.dstack([np.clip(out, 0, 1), a_out])
Image.fromarray((case_rgba * 255).astype(np.uint8), "RGBA").save(f"{OUT}/sealed_case.png")

# ---------------------------------------------------------------- showcase scene
px, pt, pb = 200, 220, 330
CW, CH = W + 2 * px, H + pt + pb
yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
ex, ey = EPI[0] + px, EPI[1] + pt
r = np.sqrt(((xx - CW / 2) / (CW * 0.6)) ** 2 + ((yy - CH * 0.5) / (CH * 0.62)) ** 2)
bg = np.array([10, 8, 7], np.float32) * np.clip(1.2 - r, 0, 1)[..., None] + 3
# god rays bursting from the rupture
ang = np.arctan2(yy - ey, xx - ex)
dist = np.hypot(xx - ex, yy - ey)
rays = np.zeros_like(ang)
for k, ph, amp in [(7, 0.3, 1.0), (13, 1.7, 0.7), (23, 0.9, 0.5), (41, 2.2, 0.35)]:
    rays += amp * np.cos(ang * k + ph)
rays = np.clip(rays / 2.55, 0, 1) ** 2.4 * np.exp(-dist / 1100)
bg += rays[..., None] * np.array([255, 150, 30], np.float32) * 1.3
bg += np.exp(-(dist / 700) ** 2)[..., None] * np.array([120, 60, 8], np.float32)


# smoke: fractal noise drifting around the base
def fractal(h, w, seed):
    g = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    for o, wgt in [(8, 1.0), (16, 0.6), (32, 0.35), (64, 0.2)]:
        small = g.random((max(2, h // (h // o)), max(2, w // (h // o)))).astype(np.float32)
        acc += wgt * np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(np.float32) / 255
    return acc / 2.15


smk = fractal(CH, CW, 7)
band = np.clip(1 - np.abs(yy - (pt + H * 0.92)) / 420, 0, 1)
smoke_a = np.clip((smk - 0.45) * 2.4, 0, 1) * band * 0.85
smoke_col = np.array([34, 30, 28], np.float32) + np.exp(-((xx - CW / 2) / (CW * 0.4)) ** 2)[..., None] * np.array([90, 45, 10], np.float32)
bg = bg * (1 - smoke_a[..., None]) + smoke_col * smoke_a[..., None]
scene = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8), "RGB").convert("RGBA")

case_img = Image.fromarray((case_rgba * 255).astype(np.uint8), "RGBA")
floor_y = pt + 1395
refl = case_img.transpose(Image.FLIP_TOP_BOTTOM).filter(ImageFilter.GaussianBlur(4))
ra = np.asarray(refl).astype(np.float32)
fade = np.clip(1 - np.arange(ra.shape[0]) / 420.0, 0, 1) ** 1.4 * 0.5
ra[..., 3] *= fade[:, None]
scene.alpha_composite(Image.fromarray(ra.astype(np.uint8), "RGBA"), (px, floor_y - (H - 1395)))
scene.alpha_composite(case_img, (px, pt))
# foreground smoke wisps, lit from the fire
fg = fractal(CH, CW, 11)
fg_a = np.clip((fg - 0.58) * 3.0, 0, 1) * np.clip(1 - np.abs(yy - (pt + H * 1.0)) / 260, 0, 1) * 0.55
fg_rgba = np.dstack([np.broadcast_to(np.array([60, 44, 30], np.float32), (CH, CW, 3)), fg_a * 255]).astype(np.uint8)
scene.alpha_composite(Image.fromarray(fg_rgba, "RGBA").filter(ImageFilter.GaussianBlur(6)))
hud = Image.open(f"{OUT}/hud.png").convert("RGBA")
hud_glow = hud.filter(ImageFilter.GaussianBlur(8))
scene.alpha_composite(hud_glow)
scene.alpha_composite(hud)
scene.convert("RGB").save(f"{OUT}/sealed_showcase.png", optimize=True)
print("ok", scene.size)
