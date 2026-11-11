"""'NAVI NEON' case: black case, yellow neon tubes along its structure, light leaking from inside.

Step 1 (svg):     python3 neon.py svg   OUT_DIR FONT_DIR            -> neon_y.html, neon_w.html
Step 2 (render):  node render_layers.js OUT_DIR neon_y,neon_w
Step 3 (compose): python3 -I neon.py compose OUT_DIR TEMPLATE BASE.png -> OUT_DIR/neon_final.png
BASE.png is the template recoloured with `recolor.py ... neon` (no overlays).
"""
import sys

MODE, OUT = sys.argv[1], sys.argv[2]
TW, TH = 2393, 1481

FRONT_IN = [(1206, 548), (1799, 548), (1820, 568), (1820, 1106), (1696, 1106), (1656, 1138),
            (1374, 1138), (1334, 1106), (1188, 1106), (1188, 568)]
SIDE_IN = [(271, 611), (483, 611), (483, 1088), (271, 1088)]
STRAP_EDGES = [
    [(832, 80), (875, 214), (930, 310), (943, 392)],
    [(995, 80), (1052, 214), (1096, 300), (1102, 392)],
    [(1877, 80), (1925, 210), (1986, 305), (2000, 392)],
    [(2040, 80), (2097, 210), (2141, 300), (2147, 392)],
]


def pts(p):
    return " ".join(f"{x},{y}" for x, y in p)


def star(cx, cy, r):
    import math
    p = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        p.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(p)}" fill="none" stroke="#fff" stroke-width="7" stroke-linejoin="round"/>'


def page(fonts, body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: 'TiltNeon'; src: url('file://{fonts}/TiltNeon.ttf'); }}
@font-face {{ font-family: 'Orbitron'; src: url('file://{fonts}/Orbitron.ttf'); }}
html,body{{margin:0;padding:0;background:transparent;}} svg{{display:block;}}
</style></head><body>
<div style="position:absolute;left:-9999px;font-family:TiltNeon">a</div>
<div style="position:absolute;left:-9999px;font-family:Orbitron">a</div>
<svg id="art" xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}">{body}</svg>
</body></html>"""


def svg_pages(fonts):
    tube = 'fill="none" stroke="#fff" stroke-linecap="round" stroke-linejoin="round"'
    y = ""
    y += f'<polygon points="{pts(FRONT_IN)}" {tube} stroke-width="7"/>\n'
    y += f'<polygon points="{pts(SIDE_IN)}" {tube} stroke-width="7"/>\n'
    for e in STRAP_EDGES:
        y += f'<polyline points="{pts(e)}" {tube} stroke-width="6"/>\n'
    y += f'<line x1="1196" y1="1262" x2="1816" y2="1262" {tube} stroke-width="6"/>\n'
    # neon sign in the front panel
    y += ('<text x="1504" y="928" text-anchor="middle" font-family="TiltNeon" font-size="262" '
          'fill="#fff" letter-spacing="10">NAVI</text>\n')
    y += f'<line x1="175" y1="113" x2="605" y2="113" {tube} stroke-width="6"/>\n'
    w = ""
    w += ('<text x="1504" y="1030" text-anchor="middle" font-family="TiltNeon" font-size="46" '
          'fill="#fff" letter-spacing="12">BORN TO WIN</text>\n')
    w += star(1222, 1014, 19) + star(1786, 1014, 19)
    # crosshair on the side door (squeezed for the side's perspective)
    w += (f'<g transform="translate(377,846) scale(0.84,1)" {tube} stroke-width="8">'
          f'<circle r="66"/><line x1="0" y1="-112" x2="0" y2="-34"/><line x1="0" y1="34" x2="0" y2="112"/>'
          f'<line x1="-112" y1="0" x2="-34" y2="0"/><line x1="34" y1="0" x2="112" y2="0"/>'
          f'<circle r="7" fill="#fff"/></g>\n')
    w += ('<text x="377" y="1052" text-anchor="middle" font-family="Orbitron" font-weight="800" font-size="30" '
          'fill="#fff" letter-spacing="4" transform="translate(377,0) scale(0.84,1) translate(-377,0)">EST. 2009</text>\n')
    open(f"{OUT}/neon_y.html", "w").write(page(fonts, y))
    open(f"{OUT}/neon_w.html", "w").write(page(fonts, w))


def compose(tpl_path, base_path):
    import numpy as np
    from PIL import Image, ImageFilter

    def blur(m, r):
        im = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8))
        return np.asarray(im.filter(ImageFilter.GaussianBlur(r))).astype(np.float32) / 255

    tpl = np.asarray(Image.open(tpl_path).convert("RGBA")).astype(np.float32) / 255
    L = tpl[..., :3] @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    alpha = tpl[..., 3]
    Lb = blur(L, 3)
    base = np.asarray(Image.open(base_path).convert("RGBA")).astype(np.float32) / 255
    out = base[..., :3].copy()

    # light leaking from inside: the dark lid gap and the front vents
    leak = np.zeros_like(L)
    xs, tops, bots = [], [], []
    for x in range(60, 2300):
        if alpha[340:470, x].max() < 0.5 or 905 <= x <= 1122 or 1945 <= x <= 2172 or 300 <= x <= 470:
            continue
        col = Lb[340:470, x].copy()
        col[alpha[340:470, x] < 0.5] = 9
        y = int(np.argmin(col)) + 340
        if col.min() > 0.12:
            continue
        t = y
        while t > y - 18 and Lb[t - 1, x] < 0.18: t -= 1
        b = y
        while b < y + 18 and Lb[b + 1, x] < 0.18: b += 1
        xs.append(x); tops.append(t); bots.append(b)
    xs, tops, bots = np.array(xs), np.array(tops, float), np.array(bots, float)
    # smooth the gap edges along x within each continuous run
    runs = np.split(np.arange(len(xs)), np.nonzero(np.diff(xs) > 3)[0] + 1)
    k = np.ones(25) / 25
    for r in runs:
        if len(r) < 8:
            continue
        tt = np.convolve(np.pad(tops[r], 12, mode='edge'), k, mode='valid')
        bb = np.convolve(np.pad(bots[r], 12, mode='edge'), k, mode='valid')
        for x, t, b in zip(xs[r], tt, bb):
            c = (t + b) / 2; h = max(3.0, (b - t) * 0.55)
            leak[int(round(c - h / 2)):int(round(c + h / 2)) + 1, x] = 1.0
    for (x0, y0, x1, y1) in [(1185, 1135, 1305, 1215), (1700, 1135, 1815, 1215)]:
        sub = Lb[y0:y1, x0:x1]
        leak[y0:y1, x0:x1] = np.maximum(leak[y0:y1, x0:x1], (sub < 0.22).astype(np.float32))
    leak = blur(leak, 1.6)

    def load(name):
        a = np.asarray(Image.open(f"{OUT}/{name}.png").convert("RGBA")).astype(np.float32) / 255
        return a[..., 3]

    ny, nw = load("neon_y"), load("neon_w")
    YEL = np.array([1.0, 0.86, 0.05], np.float32)
    AMB = np.array([1.0, 0.62, 0.0], np.float32)
    WHT = np.array([1.0, 0.97, 0.86], np.float32)
    CORE = np.array([1.0, 0.99, 0.9], np.float32)

    def light(m, tube, bloom, k=1.0):
        g1, g2, g3, g4 = blur(m, 4), blur(m, 16), blur(m, 55), blur(m, 140)
        lt = (m[..., None] * CORE * 1.0 + g1[..., None] * tube * 1.5 * k +
              g2[..., None] * tube * 0.9 * k + g3[..., None] * bloom * 1.0 * k + g4[..., None] * bloom * 1.2 * k)
        return lt, g3 + g4

    ly, hy = light(ny, YEL, AMB)
    lw, hw = light(nw, WHT, YEL, 0.8)
    ll, hl = light(leak, YEL, AMB, 1.6)
    total = np.clip(ly + lw + ll, 0, 4)
    # surfaces pick up the light (screen blend), strongest near the sources
    out = 1 - (1 - out) * (1 - np.clip(total, 0, 1))
    # shiny edges near the light pick up its colour
    spec = np.clip(L - 0.55, 0, 1)[..., None] * 2.2
    out = np.clip(out + spec * np.clip(total, 0, 1) * np.array([1.0, 0.8, 0.2], np.float32) * 0.9, 0, 1)
    halo = np.clip((hy + hw * 0.6 + hl * 1.4) * 1.6, 0, 1)
    a_out = np.maximum(alpha, halo * 0.8)
    # outside the case the halo carries its own colour
    outside = (alpha < 0.5)[..., None]
    halo_col = np.clip(total + 0.0001, 0, 1)
    out = np.where(outside, halo_col, out)
    rgba = np.dstack([np.clip(out, 0, 1), a_out])
    Image.fromarray((rgba * 255).astype(np.uint8), "RGBA").save(f"{OUT}/neon_final.png")
    print("ok")


if MODE == "svg":
    svg_pages(sys.argv[3])
    print("ok")
else:
    compose(sys.argv[3], sys.argv[4])
