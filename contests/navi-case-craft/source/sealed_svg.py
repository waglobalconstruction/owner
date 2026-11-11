"""SVG layers for 'NAVI SEALED': chains + padlock, light emitters, stencils, and the HUD.

Usage: python3 sealed_svg.py OUT_DIR FONT_DIR -> chains.html, emit.html, stencil.html, hud.html
"""
import math
import sys

OUT, FONTS = sys.argv[1], sys.argv[2]
TW, TH = 2393, 1481
SW, SH, PX, PT = 2793, 2031, 200, 220          # showcase canvas and case offset
CROSS = (1505, 795)                           # where the chains meet (padlock shackle)
LOCK = (1505, 985)                            # padlock body centre (crack epicentre)
CHAINS = [((1170, 290), (1900, 1392)), ((1840, 290), (1110, 1392)), ((60, 845), CROSS)]


def head(w, h, defs=""):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family: 'Ops'; src: url('file://{FONTS}/BlackOpsOne.ttf'); }}
@font-face {{ font-family: 'Russo'; src: url('file://{FONTS}/RussoOne.ttf'); }}
@font-face {{ font-family: 'Orbitron'; src: url('file://{FONTS}/Orbitron.ttf'); }}
html,body{{margin:0;padding:0;background:transparent;}} svg{{display:block;}}
</style></head><body>
<div style="position:absolute;left:-9999px;font-family:Ops">a</div>
<div style="position:absolute;left:-9999px;font-family:Russo">а</div>
<div style="position:absolute;left:-9999px;font-family:Orbitron">a</div>
<svg id="art" xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{defs}</defs>"""


TAIL = "</svg></body></html>"

STEEL_DEFS = """
<linearGradient id="ring" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#a7adb6"/><stop offset="0.3" stop-color="#5d636c"/>
  <stop offset="0.65" stop-color="#1f2226"/><stop offset="1" stop-color="#0a0b0c"/>
</linearGradient>
<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#b9bfc8"/><stop offset="0.35" stop-color="#5a6069"/>
  <stop offset="0.75" stop-color="#1a1c20"/><stop offset="1" stop-color="#0b0c0d"/>
</linearGradient>
<linearGradient id="lockBody" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#3a3d43"/><stop offset="0.5" stop-color="#16181b"/><stop offset="1" stop-color="#07080a"/>
</linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#fff2b8"/><stop offset="0.4" stop-color="#ffcf3a"/>
  <stop offset="0.7" stop-color="#b9820e"/><stop offset="1" stop-color="#ffdf70"/>
</linearGradient>
<linearGradient id="shackle" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#2a2d32"/><stop offset="0.35" stop-color="#c9ced6"/>
  <stop offset="0.6" stop-color="#5b6169"/><stop offset="1" stop-color="#15171a"/>
</linearGradient>
<pattern id="haz" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <rect width="20" height="40" fill="#FFE100"/><rect x="20" width="20" height="40" fill="#0d0d0f"/>
</pattern>
<filter id="dshadow" x="-20%" y="-20%" width="140%" height="140%">
  <feDropShadow dx="7" dy="11" stdDeviation="6" flood-color="#000" flood-opacity="0.85"/>
</filter>
"""


def chain_svg(p0, p1, pitch=60):
    (x0, y0), (x1, y1) = p0, p1
    d = math.dist(p0, p1)
    ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    n = int(d // pitch)
    rings, bars = [], []
    for k in range(n + 1):
        t = k * pitch / d
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        heat = max(0.0, 1 - math.dist((x, y), CROSS) / 330)
        hot = (f'<ellipse rx="43" ry="26" fill="none" stroke="#ff7a12" stroke-width="13" opacity="{heat * 0.85:.2f}"/>'
               if k % 2 == 0 else
               f'<rect x="-43" y="-8" width="86" height="16" rx="8" fill="#ff8a1a" opacity="{heat * 0.85:.2f}"/>')
        if k % 2 == 0:
            rings.append(f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})">'
                         f'<ellipse rx="43" ry="26" fill="none" stroke="url(#ring)" stroke-width="13"/>'
                         f'<ellipse rx="40" ry="22" cy="-3" fill="none" stroke="#fff" stroke-opacity="0.32" stroke-width="3"/>'
                         f'{hot}</g>')
        else:
            bars.append(f'<g transform="translate({x:.1f},{y:.1f}) rotate({ang:.1f})">'
                        f'<rect x="-43" y="-8" width="86" height="16" rx="8" fill="url(#bar)"/>'
                        f'<rect x="-36" y="-6" width="72" height="3" rx="1.5" fill="#fff" fill-opacity="0.45"/>'
                        f'{hot}</g>')
    return "".join(rings) + "".join(bars)


def padlock():
    cx, cy = LOCK
    return f"""
<g filter="url(#dshadow)">
  <path d="M{cx-66},{cy-100} L{cx-66},{cy-190} A66,66 0 0 1 {cx+66},{cy-190} L{cx+66},{cy-100}"
        fill="none" stroke="#0a0b0d" stroke-width="40" stroke-linecap="round"/>
  <path d="M{cx-66},{cy-100} L{cx-66},{cy-190} A66,66 0 0 1 {cx+66},{cy-190} L{cx+66},{cy-100}"
        fill="none" stroke="url(#shackle)" stroke-width="30" stroke-linecap="round"/>
  <path d="M{cx-58},{cy-190} A58,58 0 0 1 {cx+20},{cy-246}" fill="none" stroke="#fff" stroke-opacity="0.5" stroke-width="5" stroke-linecap="round"/>
  <rect x="{cx-128}" y="{cy-112}" width="256" height="230" rx="30" fill="url(#lockBody)" stroke="url(#gold)" stroke-width="8"/>
  <clipPath id="lockClip"><rect x="{cx-124}" y="{cy-108}" width="248" height="222" rx="27"/></clipPath>
  <rect x="{cx-128}" y="{cy+66}" width="256" height="48" fill="url(#haz)" clip-path="url(#lockClip)"/>
  <rect x="{cx-128}" y="{cy+62}" width="256" height="6" fill="url(#gold)"/>
  <text x="{cx}" y="{cy-38}" text-anchor="middle" font-family="Ops" font-size="66" fill="#000" fill-opacity="0.7" transform="translate(0,3)">NAVI</text>
  <text x="{cx}" y="{cy-38}" text-anchor="middle" font-family="Ops" font-size="66" fill="url(#gold)">NAVI</text>
  <circle cx="{cx}" cy="{cy+4}" r="21" fill="#2a1600"/>
  <path d="M{cx-11},{cy+12} L{cx-18},{cy+50} L{cx+18},{cy+50} L{cx+11},{cy+12} Z" fill="#2a1600"/>
  <circle cx="{cx-106}" cy="{cy-90}" r="6" fill="url(#gold)"/><circle cx="{cx+106}" cy="{cy-90}" r="6" fill="url(#gold)"/>
  <rect x="{cx-120}" y="{cy-106}" width="240" height="10" rx="5" fill="#fff" fill-opacity="0.12"/>
</g>
"""


def chains_page():
    body = ""
    for p0, p1 in CHAINS[2:] + CHAINS[:2]:
        body += f'<g filter="url(#dshadow)">{chain_svg(p0, p1)}</g>\n'
    body += padlock()
    return head(TW, TH, STEEL_DEFS) + body + TAIL


def emit_page():
    cx, cy = LOCK
    body = (f'<circle cx="{cx}" cy="{cy+4}" r="15" fill="#fff"/>'
            f'<path d="M{cx-7},{cy+10} L{cx-13},{cy+45} L{cx+13},{cy+45} L{cx+7},{cy+10} Z" fill="#fff"/>')
    return head(TW, TH) + body + TAIL


def stencil_page():
    b = ""
    b += ('<text x="140" y="206" font-family="Russo" font-size="56" fill="#ff3d1f" '
          'textLength="490" lengthAdjust="spacingAndGlyphs">НЕ ВІДКРИВАТИ</text>\n')
    b += ('<text x="508" y="318" font-family="Russo" font-size="40" fill="#f2efe8" '
          'textLength="300" lengthAdjust="spacingAndGlyphs">DO NOT OPEN</text>\n')
    # warning triangle on the side
    b += ('<g transform="translate(222,492) scale(0.84,1)">'
          '<path d="M0,-66 L66,52 L-66,52 Z" fill="#FFE100" stroke="#0d0d0f" stroke-width="6" stroke-linejoin="round"/>'
          '<rect x="-7" y="-28" width="14" height="48" rx="5" fill="#0d0d0f"/><circle cx="0" cy="36" r="8" fill="#0d0d0f"/></g>\n')
    # side door
    b += ('<g transform="translate(377,0) scale(0.84,1)">'
          '<text x="0" y="740" text-anchor="middle" font-family="Russo" font-size="120" fill="#FFE100">★</text>'
          '<text x="0" y="972" text-anchor="middle" font-family="Russo" font-size="30" fill="#f2efe8">CLASS:</text>'
          '<text x="0" y="1012" text-anchor="middle" font-family="Russo" font-size="34" fill="#FFE100" '
          'textLength="230" lengthAdjust="spacingAndGlyphs">LEGENDARY</text></g>\n')
    return head(TW, TH) + b + TAIL


def hud_page():
    Y, R = "#FFE100", "#ff3d1f"
    x0, y0, x1, y1 = PX + 30, PT + 20, PX + TW - 30, PT + 1420
    L = 120
    b = '<g fill="none" stroke="#FFE100" stroke-width="5" stroke-opacity="0.9">'
    for (x, y, sx, sy) in [(x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)]:
        b += f'<path d="M{x},{y + sy*L} L{x},{y} L{x + sx*L},{y}"/>'
    b += "</g>\n"
    b += (f'<circle cx="{x0+22}" cy="{y0-70}" r="11" fill="{R}"/>'
          f'<text x="{x0+48}" y="{y0-59}" font-family="Orbitron" font-weight="800" font-size="34" fill="{R}" letter-spacing="5">CONTAINMENT BREACH</text>'
          f'<text x="{x0+48}" y="{y0-26}" font-family="Orbitron" font-weight="800" font-size="18" fill="#cfcfcf" fill-opacity="0.75" letter-spacing="4">CASE Nº 0001 · SECTOR B</text>\n')
    b += (f'<text x="{x1}" y="{y0-59}" text-anchor="end" font-family="Orbitron" font-weight="800" font-size="30" fill="{Y}" letter-spacing="5">ENERGY 999%</text>'
          f'<g transform="translate({x1-330},{y0-42})">' +
          "".join(f'<rect x="{i*33}" y="0" width="26" height="14" fill="{Y if i < 9 else R}" fill-opacity="{0.95 if i < 9 else 1}"/>' for i in range(10)) +
          '</g>\n')
    cx = SW / 2
    by = PT + 1395 + 175
    b += (f'<text x="{cx}" y="{by}" text-anchor="middle" font-family="Orbitron" font-weight="800" font-size="62" '
          f'fill="{Y}" letter-spacing="10">★ LEGENDARY DROP ★</text>'
          f'<rect x="{cx-430}" y="{by+26}" width="860" height="5" fill="{Y}"/>'
          f'<text x="{cx}" y="{by+74}" text-anchor="middle" font-family="Orbitron" font-weight="800" font-size="24" '
          f'fill="#e8e2c8" letter-spacing="8">DROP CHANCE 0.26% · DO YOU DARE TO OPEN IT?</text>\n')
    return head(SW, SH) + b + TAIL


open(f"{OUT}/chains.html", "w").write(chains_page())
open(f"{OUT}/emit.html", "w").write(emit_page())
open(f"{OUT}/stencil.html", "w").write(stencil_page())
open(f"{OUT}/hud.html", "w").write(hud_page())
print("ok")
