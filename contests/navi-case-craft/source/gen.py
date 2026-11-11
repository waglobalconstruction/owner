"""Generate the 'Blueprint Case' design as SVG inside an HTML page.

Usage: python3 gen.py OUT_DIR FONT_DIR
Writes OUT_DIR/case.html (with studio background) and OUT_DIR/case_clean.html (transparent).
"""
import math
import random
import sys

OUT, FONTS = sys.argv[1], sys.argv[2]

W, H = 1600, 1200
YEL = "#FFE100"
BLK = "#0d0d0f"
INK = "#03060d"
LINE = "rgba(255,255,255,0.88)"

# Case geometry (oblique view)
FX0, FY0, FW, FH = 330, 430, 900, 520     # front face
DX, DY = 150, -120                        # depth vector
DEPTH = 192                               # local depth units for top/side
TOP_M = f"matrix(1,0,{-DX/DEPTH:.5f},{-DY/DEPTH:.5f},{FX0+DX},{FY0+DY})"
SIDE_M = f"matrix({DX/DEPTH:.5f},{DY/DEPTH:.5f},0,1,{FX0+FW},{FY0})"
LID = 130


def top_pt(x, y):
    """Top-face local -> screen (y=0 back edge, y=DEPTH front edge)."""
    return (FX0 + DX + x - y * DX / DEPTH, FY0 + DY - y * DY / DEPTH)


rnd = random.Random(7)


def fonts_css():
    return f"""
@font-face {{ font-family: 'Stencil'; src: url('file://{FONTS}/SairaStencilOne.ttf'); }}
@font-face {{ font-family: 'Ops'; src: url('file://{FONTS}/BlackOpsOne.ttf'); }}
@font-face {{ font-family: 'Marker'; src: url('file://{FONTS}/PermanentMarker.ttf'); }}
@font-face {{ font-family: 'RubikMono'; src: url('file://{FONTS}/RubikMonoOne.ttf'); }}
"""


DEFS = f"""
<defs>
  <linearGradient id="frontBase" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1a5fc0"/>
    <stop offset="0.55" stop-color="#114a9e"/>
    <stop offset="1" stop-color="#0a3175"/>
  </linearGradient>
  <linearGradient id="topBase" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#1c64c8"/>
    <stop offset="1" stop-color="#2a76dc"/>
  </linearGradient>
  <linearGradient id="sideBase" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#0c3f8c"/>
    <stop offset="1" stop-color="#072a62"/>
  </linearGradient>
  <radialGradient id="frontVignette" cx="0.45" cy="0.4" r="0.75">
    <stop offset="0.55" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.45"/>
  </radialGradient>
  <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0.10"/>
    <stop offset="0.35" stop-color="#fff" stop-opacity="0.0"/>
    <stop offset="0.6" stop-color="#fff" stop-opacity="0.05"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <linearGradient id="metal" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#8b929c"/>
    <stop offset="0.45" stop-color="#4a5059"/>
    <stop offset="1" stop-color="#23272d"/>
  </linearGradient>
  <linearGradient id="metalH" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#3a4048"/>
    <stop offset="0.5" stop-color="#9aa1aa"/>
    <stop offset="1" stop-color="#2b3036"/>
  </linearGradient>
  <linearGradient id="tapeShade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000" stop-opacity="0.18"/>
    <stop offset="0.2" stop-color="#fff" stop-opacity="0.10"/>
    <stop offset="0.45" stop-color="#000" stop-opacity="0.08"/>
    <stop offset="0.7" stop-color="#fff" stop-opacity="0.12"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.2"/>
  </linearGradient>
  <radialGradient id="studio" cx="0.52" cy="0.46" r="0.7">
    <stop offset="0" stop-color="#2a2f38"/>
    <stop offset="0.55" stop-color="#15181d"/>
    <stop offset="1" stop-color="#08090b"/>
  </radialGradient>
  <radialGradient id="floorGlow" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{YEL}" stop-opacity="0.16"/>
    <stop offset="1" stop-color="{YEL}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="gridMinor" width="30" height="30" patternUnits="userSpaceOnUse">
    <path d="M30 0H0V30" fill="none" stroke="#fff" stroke-opacity="0.10" stroke-width="1"/>
  </pattern>
  <pattern id="gridMajor" width="150" height="150" patternUnits="userSpaceOnUse">
    <path d="M150 0H0V150" fill="none" stroke="#fff" stroke-opacity="0.24" stroke-width="1.6"/>
  </pattern>
  <pattern id="bgGrid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#5c8fd6" stroke-opacity="0.07" stroke-width="1"/>
  </pattern>
  <pattern id="haz" width="44" height="44" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
    <rect width="22" height="44" fill="{YEL}"/>
    <rect x="22" width="22" height="44" fill="{BLK}"/>
  </pattern>
  <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse">
    <path d="M0 1 L10 5 L0 9 Z" fill="#fff"/>
  </marker>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="5"/>
  </filter>
  <filter id="spray" x="-10%" y="-30%" width="120%" height="160%">
    <feGaussianBlur stdDeviation="7"/>
  </filter>
  <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="3" dy="5" stdDeviation="4" flood-color="#000" flood-opacity="0.55"/>
  </filter>
  <filter id="floorBlur" x="-20%" y="-200%" width="140%" height="500%">
    <feGaussianBlur stdDeviation="18"/>
  </filter>
  <filter id="grunge" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="4" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.3 1.45" result="m"/>
    <feComposite in="SourceGraphic" in2="m" operator="in"/>
  </filter>
  <filter id="paperNoise" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="3" seed="11" result="n"/>
    <feColorMatrix in="n" type="saturate" values="0" result="g"/>
    <feComponentTransfer in="g"><feFuncA type="table" tableValues="0 0.10"/></feComponentTransfer>
  </filter>
  <clipPath id="frontClip"><rect width="{FW}" height="{FH}"/></clipPath>
  <clipPath id="topClip"><rect width="{FW}" height="{DEPTH}"/></clipPath>
  <clipPath id="sideClip"><rect width="{DEPTH}" height="{FH}"/></clipPath>
  <path id="ringText" d="M0,0 m-52,0 a52,52 0 1,1 104,0 a52,52 0 1,1 -104,0"/>
</defs>
"""


def dim_h(x1, x2, y, label, ext_from):
    """Horizontal dimension line with extension lines and a label."""
    mid = (x1 + x2) / 2
    tw = len(label) * 9.6 + 14
    return f"""
  <g stroke="#fff" stroke-width="1.4" fill="none" opacity="0.9">
    <line x1="{x1}" y1="{ext_from}" x2="{x1}" y2="{y + (6 if y < ext_from else -6)}" stroke-dasharray="1 0"/>
    <line x1="{x2}" y1="{ext_from}" x2="{x2}" y2="{y + (6 if y < ext_from else -6)}"/>
    <line x1="{x1}" y1="{y}" x2="{mid - tw/2}" y2="{y}" marker-start="url(#arr)"/>
    <line x1="{mid + tw/2}" y1="{y}" x2="{x2}" y2="{y}" marker-end="url(#arr)"/>
  </g>
  <text x="{mid}" y="{y + 5}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="15" fill="#fff">{label}</text>
"""


def callout(x1, y1, x2, y2, text, anchor="start"):
    tx = x2 + (8 if anchor == "start" else -8)
    return f"""
  <circle cx="{x1}" cy="{y1}" r="3.2" fill="#fff"/>
  <polyline points="{x1},{y1} {x2},{y2} {x2 + (70 if anchor=='start' else -70)},{y2}" fill="none" stroke="#fff" stroke-width="1.3" opacity="0.9"/>
  <text x="{tx}" y="{y2 - 6}" text-anchor="{anchor}" font-family="JetBrains Mono" font-weight="600" font-size="12.5" fill="#fff" letter-spacing="0.5">{text}</text>
"""


def knife():
    # Bowie-style knife drawn as a technical line drawing, centreline at y=300
    blade = ("M250,281 L448,281 C495,281 535,284 568,291 "
             "C548,305 522,317 488,321 L250,321 Z")
    grind = "M262,309 L470,309 C505,308 535,301 560,293"
    fuller = "M276,292 L418,292 A5,5 0 0 1 418,302 L276,302 A5,5 0 0 1 276,292 Z"
    guard = "M234,262 L250,266 L250,334 L234,338 Q228,300 234,262 Z"
    handle = ("M86,283 L232,279 L232,321 L200,321 Q190,333 178,321 "
              "Q166,333 154,321 Q142,333 130,321 L86,317 Z")
    pommel = "M60,286 Q60,280 66,280 L88,282 L88,318 L66,320 Q60,320 60,314 Z"
    s = f"""
  <g fill="none" stroke="{LINE}" stroke-width="2.2" stroke-linejoin="round">
    <path d="{blade}" fill="#fff" fill-opacity="0.06"/>
    <path d="{grind}" stroke-width="1.4" stroke-dasharray="6 4"/>
    <path d="{fuller}" stroke-width="1.6"/>
    <path d="{guard}" fill="#fff" fill-opacity="0.08"/>
    <path d="{handle}" fill="#fff" fill-opacity="0.05"/>
    <path d="{pommel}" fill="#fff" fill-opacity="0.08"/>
    <circle cx="74" cy="300" r="6.5" stroke-width="1.6"/>
  </g>
  <g stroke="{LINE}" stroke-width="1.1" opacity="0.7">
"""
    for x in range(98, 226, 12):
        s += f'    <line x1="{x}" y1="287" x2="{x + 8}" y2="315"/>\n'
    s += "  </g>\n"
    # centreline (dash-dot)
    s += ('  <line x1="38" y1="300" x2="596" y2="300" stroke="#fff" stroke-width="1" '
          'stroke-dasharray="22 5 3 5" opacity="0.55"/>\n')
    # detail circle around the guard
    s += ('  <circle cx="242" cy="300" r="52" fill="none" stroke="#fff" stroke-width="1.3" '
          'stroke-dasharray="8 5" opacity="0.85"/>\n')
    s += ('  <circle cx="281" cy="261" r="12" fill="#0f448f" stroke="#fff" stroke-width="1.4"/>'
          '<text x="281" y="266" text-anchor="middle" font-family="JetBrains Mono" '
          'font-weight="800" font-size="13" fill="#fff">A</text>\n')
    s += dim_h(60, 568, 226, "505", 278)
    s += dim_h(250, 568, 368, "BLADE 318", 324)
    s += callout(150, 322, 132, 412, "GRIP: RUBBER")
    s += callout(330, 302, 300, 432, "FULLER")
    s += ('  <text x="150" y="174" font-family="JetBrains Mono" font-weight="700" font-size="13" '
          'fill="#fff" opacity="0.9" letter-spacing="1.5">FIG.1 — CONTENTS: ★ RARE SPECIAL ITEM</text>\n')
    return s


def iso_view():
    # tiny wireframe of the case itself
    sx = 0.13
    ox, oy = 628, 182
    def p(x, y):
        return f"{ox + (x - FX0) * sx:.1f},{oy + (y - 310) * sx:.1f}"
    front = [(FX0, FY0), (FX0 + FW, FY0), (FX0 + FW, FY0 + FH), (FX0, FY0 + FH)]
    top = [(FX0, FY0), (FX0 + DX, FY0 + DY), (FX0 + FW + DX, FY0 + DY), (FX0 + FW, FY0)]
    side = [(FX0 + FW, FY0), (FX0 + FW + DX, FY0 + DY), (FX0 + FW + DX, FY0 + FH + DY), (FX0 + FW, FY0 + FH)]
    s = '  <g fill="none" stroke="#fff" stroke-width="1.4" stroke-linejoin="round" opacity="0.9">\n'
    for poly in (front, top, side):
        s += '    <polygon points="' + " ".join(p(*q) for q in poly) + '"/>\n'
    s += f'    <line x1="{p(FX0, FY0 + LID).split(",")[0]}" y1="{p(FX0, FY0 + LID).split(",")[1]}" ' \
         f'x2="{p(FX0 + FW, FY0 + LID).split(",")[0]}" y2="{p(FX0 + FW, FY0 + LID).split(",")[1]}" stroke-dasharray="4 3"/>\n'
    s += "  </g>\n"
    s += (f'  <text x="{ox}" y="{oy + 100}" font-family="JetBrains Mono" font-weight="700" font-size="12" '
          f'fill="#fff" letter-spacing="1.2" opacity="0.9">VIEW B — ISO</text>\n')
    return s


def title_block():
    x, y, w = 586, 372, 300
    rows = [26, 26, 24]
    s = f'  <g font-family="JetBrains Mono" fill="#fff">\n'
    s += f'    <rect x="{x}" y="{y}" width="{w}" height="{sum(rows)}" fill="#062457" fill-opacity="0.55" stroke="#fff" stroke-width="1.6"/>\n'
    yy = y
    cells = [
        [("PROJECT", 84), ("CASE CRAFT 2026", 216)],
        [("ITEM", 84), ("BLUEPRINT CASE", 216)],
        [("SCALE 1:1", 100), ("REV. A", 80), ("SHEET 01/01", 120)],
    ]
    for r, h in zip(cells, rows):
        xx = x
        for i, (txt, cw) in enumerate(r):
            if xx > x:
                s += f'    <line x1="{xx}" y1="{yy}" x2="{xx}" y2="{yy + h}" stroke="#fff" stroke-width="1.1"/>\n'
            bold = "800" if (len(r) == 2 and i == 1) else "600"
            size = 14 if bold == "800" else 11.5
            s += f'    <text x="{xx + 8}" y="{yy + h/2 + 4.5}" font-weight="{bold}" font-size="{size}" letter-spacing="0.8">{txt}</text>\n'
            xx += cw
        yy += h
        if yy < y + sum(rows):
            s += f'    <line x1="{x}" y1="{yy}" x2="{x + w}" y2="{yy}" stroke="#fff" stroke-width="1.1"/>\n'
    s += "  </g>\n"
    return s


def stamp(cx, cy, r, rot):
    return f"""
  <g transform="translate({cx},{cy}) rotate({rot})" opacity="0.95">
    <g filter="url(#grunge)">
      <circle r="{r}" fill="none" stroke="#ff3b3b" stroke-width="4"/>
      <circle r="{r - 8}" fill="none" stroke="#ff3b3b" stroke-width="1.6"/>
      <rect x="{-r - 6}" y="-15" width="{2*r + 12}" height="30" fill="#ff3b3b"/>
      <text y="7" text-anchor="middle" font-family="Ops" font-size="21" fill="#fff" letter-spacing="1">APPROVED</text>
      <text y="-24" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="10" fill="#ff3b3b" letter-spacing="1.5">QC • 2026</text>
      <text y="33" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="10" fill="#ff3b3b" letter-spacing="1.5">DROP OK</text>
    </g>
  </g>
"""


def hardhat_sticker(cx, cy, scale, rot):
    return f"""
  <g transform="translate({cx},{cy}) rotate({rot}) scale({scale})" filter="url(#shadow)">
    <circle r="76" fill="#f4f4f2"/>
    <circle r="68" fill="{BLK}"/>
    <text font-family="Ops" font-size="14" fill="{YEL}" letter-spacing="1.2">
      <textPath href="#ringText" startOffset="0" textLength="318" lengthAdjust="spacing">HEADSHOT PROTECTION ★ CERTIFIED ★ </textPath>
    </text>
    <circle r="40" fill="{YEL}"/>
    <g transform="translate(0,6)" fill="{BLK}">
      <path d="M-25,4 A25,25 0 0 1 25,4 Z"/>
      <rect x="-5" y="-23" width="10" height="27" rx="3" fill="{YEL}" opacity="0.9"/>
      <rect x="-31" y="3" width="62" height="9" rx="4.5"/>
    </g>
  </g>
"""


def caution_tape():
    txt = "CAUTION ▲ CASE UNDER CONSTRUCTION ▲ CAUTION ▲ CASE UNDER CONSTRUCTION"
    return f"""
  <g transform="translate(-60,352) rotate(27)" filter="url(#shadow)">
    <rect x="0" y="-23" width="560" height="46" fill="{YEL}"/>
    <rect x="0" y="-23" width="560" height="5" fill="{BLK}"/>
    <rect x="0" y="18" width="560" height="5" fill="{BLK}"/>
    <text x="14" y="8" font-family="Ops" font-size="20" fill="{BLK}" letter-spacing="1.2">{txt}</text>
    <rect x="0" y="-23" width="560" height="46" fill="url(#tapeShade)"/>
  </g>
"""


def spray_title():
    # Yellow stencil spray across the lid, with overspray and drips.
    tx, ty, tl = 450, 98, 590
    text = "BLUEPRINT CASE"
    common = f'x="{tx}" y="{ty}" text-anchor="middle" font-family="Stencil" font-size="84" textLength="{tl}" lengthAdjust="spacingAndGlyphs"'
    s = f'  <text {common} fill="{YEL}" opacity="0.55" filter="url(#spray)">{text}</text>\n'
    # overspray speckles
    s += '  <g fill="#FFE100">\n'
    for _ in range(260):
        x = rnd.uniform(tx - tl / 2 - 30, tx + tl / 2 + 30)
        y = rnd.gauss(ty - 30, 30)
        if y < 4:
            continue
        s += f'    <circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(0.5, 1.9):.2f}" opacity="{rnd.uniform(0.25, 0.75):.2f}"/>\n'
    s += "  </g>\n"
    # drips
    s += f'  <g fill="{YEL}">\n'
    for x, L, w in [(205, 40, 5), (300, 50, 6), (420, 44, 4.5), (520, 96, 6.5), (612, 60, 5.5), (700, 38, 4)]:
        y0 = ty - 6
        s += (f'    <path d="M{x - w/2:.1f},{y0} L{x - w/2:.1f},{y0 + L} A{w/2:.2f},{w/2:.2f} 0 0 0 {x + w/2:.1f},{y0 + L} '
              f'L{x + w/2:.1f},{y0} Z"/>\n')
        s += f'    <ellipse cx="{x}" cy="{y0 + L + 1}" rx="{w*0.62:.2f}" ry="{w*0.8:.2f}"/>\n'
    s += "  </g>\n"
    s += f'  <text {common} fill="{YEL}">{text}</text>\n'
    return s


def scratches(w, h, n, edge_bias=True):
    s = '  <g stroke="#fff" stroke-linecap="round" fill="none">\n'
    for _ in range(n):
        if edge_bias and rnd.random() < 0.7:
            side = rnd.choice("lrtb")
            x = rnd.uniform(0, 40) if side == "l" else rnd.uniform(w - 40, w) if side == "r" else rnd.uniform(0, w)
            y = rnd.uniform(0, 40) if side == "t" else rnd.uniform(h - 40, h) if side == "b" else rnd.uniform(0, h)
        else:
            x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        a = rnd.uniform(0, math.pi)
        L = rnd.uniform(6, 26)
        s += (f'    <line x1="{x:.1f}" y1="{y:.1f}" x2="{x + L*math.cos(a):.1f}" y2="{y + L*math.sin(a):.1f}" '
              f'stroke-width="{rnd.uniform(0.6, 1.8):.2f}" opacity="{rnd.uniform(0.08, 0.28):.2f}"/>\n')
    s += "  </g>\n"
    return s


def rivet(x, y, r=5):
    return (f'<circle cx="{x}" cy="{y}" r="{r + 1.5}" fill="#121417"/>'
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#metal)"/>'
            f'<circle cx="{x - r*0.3:.1f}" cy="{y - r*0.35:.1f}" r="{r*0.35:.1f}" fill="#fff" opacity="0.55"/>')


def latch(cx):
    y0 = LID - 44
    return f"""
  <g filter="url(#shadow)">
    <rect x="{cx - 38}" y="{y0}" width="76" height="98" rx="9" fill="#15181c"/>
    <rect x="{cx - 33}" y="{y0 + 4}" width="66" height="90" rx="7" fill="url(#metalH)"/>
    <rect x="{cx - 24}" y="{y0 + 14}" width="48" height="56" rx="5" fill="{YEL}" stroke="#15181c" stroke-width="3"/>
    <rect x="{cx - 24}" y="{y0 + 14}" width="48" height="56" rx="5" fill="url(#haz)" opacity="0.0"/>
    <rect x="{cx - 14}" y="{y0 + 24}" width="28" height="7" rx="3.5" fill="#15181c"/>
    <rect x="{cx - 14}" y="{y0 + 37}" width="28" height="7" rx="3.5" fill="#15181c"/>
    <rect x="{cx - 14}" y="{y0 + 50}" width="28" height="7" rx="3.5" fill="#15181c"/>
    {rivet(cx - 22, y0 + 82, 4)}{rivet(cx + 22, y0 + 82, 4)}
  </g>
"""


def corner_caps():
    s = ""
    cap = 66
    for (x, y, sx, sy) in [(0, 0, 1, 1), (FW, 0, -1, 1), (0, FH, 1, -1), (FW, FH, -1, -1)]:
        path = (f"M{x},{y} L{x + sx*cap},{y} Q{x + sx*cap},{y + sy*22} {x + sx*22},{y + sy*22} "
                f"L{x + sx*22},{y + sy*22} Q{x + sx*22},{y + sy*cap} {x},{y + sy*cap} Z")
        s += f'  <path d="{path}" fill="url(#metal)" stroke="#121417" stroke-width="3" stroke-linejoin="round"/>\n'
        s += "  " + rivet(x + sx*12, y + sy*12, 4.5) + "\n"
        s += "  " + rivet(x + sx*44, y + sy*11, 3.6) + rivet(x + sx*11, y + sy*44, 3.6) + "\n"
    return s


def front():
    s = f'<g transform="translate({FX0},{FY0})">\n'
    s += '<g clip-path="url(#frontClip)">\n'
    s += f'  <rect width="{FW}" height="{FH}" fill="url(#frontBase)"/>\n'
    s += f'  <rect width="{FW}" height="{FH}" fill="url(#gridMinor)"/>\n'
    s += f'  <rect width="{FW}" height="{FH}" fill="url(#gridMajor)"/>\n'
    s += f'  <rect width="{FW}" height="{FH}" filter="url(#paperNoise)"/>\n'
    s += f'  <rect width="{FW}" height="{LID}" fill="#000" opacity="0.10"/>\n'
    s += knife()
    s += iso_view()
    s += title_block()
    s += stamp(642, 338, 48, -14)
    s += spray_title()
    # seam between lid and body
    s += f'  <rect y="{LID - 4}" width="{FW}" height="11" fill="#04132e"/>\n'
    s += f'  <rect y="{LID + 7}" width="{FW}" height="2" fill="#fff" opacity="0.22"/>\n'
    s += f'  <rect y="{LID - 6}" width="{FW}" height="2" fill="#000" opacity="0.35"/>\n'
    # hazard bumper
    s += f'  <rect y="{FH - 50}" width="{FW}" height="50" fill="url(#haz)"/>\n'
    s += f'  <rect y="{FH - 54}" width="{FW}" height="5" fill="#15181c"/>\n'
    s += f'  <rect y="{FH - 49}" width="{FW}" height="2" fill="#fff" opacity="0.25"/>\n'
    s += (f'  <g><rect x="290" y="{FH - 43}" width="320" height="34" rx="4" fill="{BLK}" stroke="{YEL}" stroke-width="2"/>'
          f'<text x="450" y="{FH - 21}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="12.5" '
          f'fill="{YEL}" letter-spacing="1.6">CRAFT IT · BUILD IT · OPEN IT</text>'
          f'{rivet(302, FH - 26, 3.2)}{rivet(598, FH - 26, 3.2)}</g>\n')
    s += caution_tape()
    s += hardhat_sticker(816, 270, 0.8, 12)
    s += scratches(FW, FH, 70)
    s += f'  <rect width="{FW}" height="{FH}" fill="url(#frontVignette)"/>\n'
    s += f'  <rect width="{FW}" height="{FH}" fill="url(#sheen)"/>\n'
    # top rim highlight
    s += f'  <rect width="{FW}" height="3" fill="#fff" opacity="0.45"/>\n'
    s += "</g>\n"
    s += latch(95) + latch(FW - 95)
    s += corner_caps()
    s += "</g>\n"
    return s


def top():
    s = f'<g transform="{TOP_M}">\n<g clip-path="url(#topClip)">\n'
    s += f'  <rect width="{FW}" height="{DEPTH}" fill="url(#topBase)"/>\n'
    s += f'  <rect width="{FW}" height="{DEPTH}" fill="url(#gridMinor)"/>\n'
    s += f'  <rect width="{FW}" height="{DEPTH}" fill="url(#gridMajor)"/>\n'
    # raised ribs
    for y in (26, DEPTH - 30):
        s += f'  <rect x="18" y="{y}" width="{FW - 36}" height="12" rx="6" fill="#0b3b85"/>\n'
        s += f'  <rect x="18" y="{y}" width="{FW - 36}" height="4" rx="2" fill="#fff" opacity="0.3"/>\n'
    # stencil "THIS SIDE UP"
    s += ('  <g fill="#fff" opacity="0.9">'
          '<path d="M52,124 l0,-36 l-13,0 l22,-24 l22,24 l-13,0 l0,36 Z"/>'
          '<text x="92" y="122" font-family="Stencil" font-size="38" textLength="212" lengthAdjust="spacingAndGlyphs">THIS SIDE UP</text>'
          '</g>\n')
    # NAVI sticker (die-cut)
    s += (f'  <g transform="translate(738,100) rotate(-6)">'
          f'<rect x="-104" y="-44" width="208" height="88" rx="16" fill="#f4f4f2"/>'
          f'<rect x="-96" y="-36" width="192" height="72" rx="11" fill="{YEL}"/>'
          f'<rect x="-96" y="-36" width="192" height="72" rx="11" fill="none" stroke="{BLK}" stroke-width="5"/>'
          f'<text y="21" text-anchor="middle" font-family="Ops" font-size="60" fill="{BLK}" letter-spacing="4">NAVI</text>'
          f'</g>\n')
    s += scratches(FW, DEPTH, 30)
    s += f'  <rect width="{FW}" height="{DEPTH}" fill="#fff" opacity="0.04"/>\n'
    s += f'  <rect y="{DEPTH - 5}" width="{FW}" height="5" fill="#fff" opacity="0.4"/>\n'
    s += "</g>\n"
    # top-face corner caps
    for x in (0, FW - 60):
        s += f'  <rect x="{x}" y="{DEPTH - 50}" width="60" height="50" fill="url(#metal)" stroke="#121417" stroke-width="3"/>\n'
    s += "</g>\n"
    return s


def side():
    s = f'<g transform="{SIDE_M}">\n<g clip-path="url(#sideClip)">\n'
    s += f'  <rect width="{DEPTH}" height="{FH}" fill="url(#sideBase)"/>\n'
    s += f'  <rect width="{DEPTH}" height="{FH}" fill="url(#gridMinor)"/>\n'
    s += f'  <rect width="{DEPTH}" height="{FH}" fill="url(#gridMajor)"/>\n'
    s += f'  <rect width="{DEPTH}" height="{LID}" fill="#000" opacity="0.12"/>\n'
    s += (f'  <text x="96" y="104" text-anchor="middle" font-family="Stencil" font-size="96" fill="{YEL}" '
          f'opacity="0.95">01</text>\n')
    # FRAGILE label
    s += (f'  <g transform="translate(96,262)">'
          f'<rect x="-78" y="-74" width="156" height="148" rx="6" fill="#f2efe6"/>'
          f'<rect x="-70" y="-66" width="140" height="132" rx="3" fill="none" stroke="#d32f2f" stroke-width="4"/>'
          f'<path d="M-14,-52 L14,-52 L10,-22 Q0,-12 -10,-22 Z M-2,-16 L-2,8 M-12,10 L10,10" fill="none" stroke="#d32f2f" stroke-width="4" stroke-linejoin="round"/>'
          f'<path d="M-4,-50 L2,-40 L-3,-33 L3,-26" fill="none" stroke="#f2efe6" stroke-width="2.4"/>'
          f'<text y="38" text-anchor="middle" font-family="Ops" font-size="27" fill="#d32f2f">FRAGILE</text>'
          f'<text y="56" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="11" fill="#1d1d1d" letter-spacing="0.6">CONTAINS KNIVES</text>'
          f'</g>\n')
    # barcode
    s += '  <g fill="#fff" opacity="0.85">\n'
    x = 40
    while x < 152:
        w = rnd.choice([1.5, 2.5, 3.5, 1.5, 5])
        s += f'    <rect x="{x:.1f}" y="372" width="{w}" height="46"/>\n'
        x += w + rnd.choice([1.5, 2.5, 3])
    s += "  </g>\n"
    s += ('  <text x="96" y="436" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" '
          'font-size="11" fill="#fff" opacity="0.85" letter-spacing="1">CC-2026-0001</text>\n')
    s += f'  <rect y="{LID - 4}" width="{DEPTH}" height="11" fill="#031029"/>\n'
    s += f'  <rect y="{FH - 50}" width="{DEPTH}" height="50" fill="url(#haz)"/>\n'
    s += f'  <rect y="{FH - 54}" width="{DEPTH}" height="5" fill="#15181c"/>\n'
    s += scratches(DEPTH, FH, 25)
    s += f'  <rect width="{DEPTH}" height="{FH}" fill="#000" opacity="0.38"/>\n'
    s += f'  <rect width="3" height="{FH}" fill="#fff" opacity="0.30"/>\n'
    s += "</g>\n"
    # side corner caps (front edge)
    s += f'  <rect x="0" y="0" width="46" height="66" fill="url(#metal)" stroke="#121417" stroke-width="3"/>\n'
    s += f'  <rect x="0" y="{FH - 66}" width="46" height="66" fill="url(#metal)" stroke="#121417" stroke-width="3"/>\n'
    s += f'  <rect width="46" height="{FH}" fill="#000" opacity="0.0"/>\n'
    s += "</g>\n"
    return s


def handle():
    (ax, ay), (bx, by) = top_pt(355, 104), top_pt(575, 104)
    h = 62
    s = f"""
<g>
  <ellipse cx="{(ax+bx)/2}" cy="{ay + 8}" rx="{(bx-ax)/2 + 30}" ry="16" fill="#000" opacity="0.35" filter="url(#soft)"/>
  <path d="M{ax},{ay} C{ax},{ay - h*1.25} {bx},{by - h*1.25} {bx},{by}" fill="none" stroke="#08090b" stroke-width="34" stroke-linecap="round"/>
  <path d="M{ax},{ay} C{ax},{ay - h*1.25} {bx},{by - h*1.25} {bx},{by}" fill="none" stroke="#1b1e23" stroke-width="26" stroke-linecap="round"/>
  <path d="M{ax + 30},{ay - h*0.72} C{ax + 60},{ay - h*0.98} {bx - 60},{by - h*0.98} {bx - 30},{by - h*0.72}" fill="none" stroke="#5a616b" stroke-width="5" stroke-linecap="round" opacity="0.8"/>
"""
    for (px, py) in ((ax, ay), (bx, by)):
        s += (f'  <path d="M{px - 34},{py + 10} L{px + 18},{py + 10} L{px + 38},{py - 6} L{px - 14},{py - 6} Z" '
              f'fill="{YEL}" stroke="#08090b" stroke-width="3.5" stroke-linejoin="round"/>\n')
        s += f'  {rivet(px + 2, py + 2, 4.5)}\n'
    s += "</g>\n"
    return s


def outline():
    p = f"M{FX0},{FY0} L{FX0+DX},{FY0+DY} L{FX0+FW+DX},{FY0+DY} L{FX0+FW+DX},{FY0+FH+DY} L{FX0+FW},{FY0+FH} L{FX0},{FY0+FH} Z"
    return f"""
<g fill="none" stroke-linejoin="round" stroke-linecap="round">
  <path d="{p}" stroke="{INK}" stroke-width="8"/>
  <path d="M{FX0},{FY0} L{FX0+FW},{FY0} L{FX0+FW+DX},{FY0+DY} M{FX0+FW},{FY0} L{FX0+FW},{FY0+FH}" stroke="{INK}" stroke-width="4"/>
  <path d="M{FX0+3},{FY0+2} L{FX0+FW-2},{FY0+2}" stroke="#fff" stroke-width="2" opacity="0.5"/>
</g>
"""


def background():
    return f"""
<rect width="{W}" height="{H}" fill="url(#studio)"/>
<rect width="{W}" height="{H}" fill="url(#bgGrid)"/>
<ellipse cx="860" cy="985" rx="760" ry="110" fill="url(#floorGlow)"/>
"""


def floor_shadow():
    return f"""
<ellipse cx="{FX0 + FW/2 + 70}" cy="{FY0 + FH + 6}" rx="{FW/2 + 120}" ry="34" fill="#000" opacity="0.75" filter="url(#floorBlur)"/>
<polygon points="{FX0+12},{FY0+FH} {FX0+FW},{FY0+FH} {FX0+FW+DX},{FY0+FH+DY} {FX0+FW+DX+40},{FY0+FH+DY+60} {FX0+40},{FY0+FH+18}" fill="#000" opacity="0.5" filter="url(#soft)"/>
"""


def build(with_bg):
    svg = f'<svg id="art" xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
    svg += DEFS
    if with_bg:
        svg += background()
    svg += floor_shadow()
    svg += side() + top() + front() + handle() + outline()
    svg += "</svg>\n"
    bg = "#0b0c0e" if with_bg else "transparent"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fonts_css()}
html,body{{margin:0;padding:0;background:{bg};}}
svg{{display:block;}}
</style></head><body>
<!-- warm up fonts -->
<div style="position:absolute;left:-9999px;font-family:Stencil">a</div>
<div style="position:absolute;left:-9999px;font-family:Ops">a</div>
<div style="position:absolute;left:-9999px;font-family:Marker">a</div>
{svg}</body></html>"""


if __name__ == "__main__":
    rnd.seed(7)
    open(f"{OUT}/case.html", "w").write(build(True))
    rnd.seed(7)
    open(f"{OUT}/case_clean.html", "w").write(build(False))
    print("ok")
