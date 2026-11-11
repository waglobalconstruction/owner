"""Overlay layers (paint / spray / stickers) for the contest template, in template pixels.

Usage: python3 overlay.py OUT_DIR FONT_DIR  -> OUT_DIR/{paint,spray,stickers}.html (2393x1481)
"""
import gen
from gen import YEL, BLK, DEFS, knife, iso_view, title_block, stamp, hardhat_sticker, fonts_css

OUT = gen.OUT
TW, TH = 2393, 1481

FRONT_SHEET = [(1200, 536), (1805, 536), (1832, 562), (1832, 1118), (1700, 1118), (1660, 1150),
               (1370, 1150), (1330, 1118), (1176, 1118), (1176, 562)]
SIDE_SHEET = [(258, 598), (495, 598), (495, 1100), (258, 1100)]


def pts(p):
    return " ".join(f"{x},{y}" for x, y in p)


EXTRA = f"""
<defs>
  <clipPath id="frontSheet"><polygon points="{pts(FRONT_SHEET)}"/></clipPath>
  <clipPath id="sideSheet"><polygon points="{pts(SIDE_SHEET)}"/></clipPath>
  <pattern id="tGridMinor" width="36" height="36" patternUnits="userSpaceOnUse">
    <path d="M36 0H0V36" fill="none" stroke="#fff" stroke-opacity="0.16" stroke-width="1.3"/>
  </pattern>
  <pattern id="tGridMajor" width="180" height="180" patternUnits="userSpaceOnUse">
    <path d="M180 0H0V180" fill="none" stroke="#fff" stroke-opacity="0.34" stroke-width="2"/>
  </pattern>
  <pattern id="sGridMinor" width="36" height="36" patternUnits="userSpaceOnUse" patternTransform="scale(0.8,1)">
    <path d="M36 0H0V36" fill="none" stroke="#fff" stroke-opacity="0.16" stroke-width="1.3"/>
  </pattern>
  <pattern id="sGridMajor" width="180" height="180" patternUnits="userSpaceOnUse" patternTransform="scale(0.8,1)">
    <path d="M180 0H0V180" fill="none" stroke="#fff" stroke-opacity="0.34" stroke-width="2"/>
  </pattern>
  <linearGradient id="buildGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ff4fb8"/>
    <stop offset="0.5" stop-color="#ffd23a"/>
    <stop offset="1" stop-color="#3fe0ff"/>
  </linearGradient>
</defs>
"""


def page(body):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fonts_css()}
html,body{{margin:0;padding:0;background:transparent;}}
svg{{display:block;}}
</style></head><body>
<div style="position:absolute;left:-9999px;font-family:Stencil">a</div>
<div style="position:absolute;left:-9999px;font-family:Ops">a</div>
<div style="position:absolute;left:-9999px;font-family:Marker">a</div>
<svg id="art" xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}">
{DEFS}{EXTRA}{body}</svg></body></html>"""


def paint_layer():
    s = ""
    # blueprint grids on the recessed "sheets"
    s += (f'<g clip-path="url(#frontSheet)"><rect x="1150" y="520" width="720" height="660" fill="url(#tGridMinor)"/>'
          f'<rect x="1150" y="520" width="720" height="660" fill="url(#tGridMajor)"/></g>\n')
    s += (f'<g clip-path="url(#sideSheet)"><rect x="240" y="580" width="280" height="540" fill="url(#sGridMinor)"/>'
          f'<rect x="240" y="580" width="280" height="540" fill="url(#sGridMajor)"/></g>\n')
    # technical drawing of the "rare special item"
    s += '<g transform="translate(1162,452) scale(1.08)">' + knife() + '</g>\n'
    s += '<g transform="translate(587,793)">' + iso_view() + '</g>\n'
    s += '<g transform="translate(914,618)">' + title_block() + '</g>\n'
    s += stamp(1440, 1012, 50, -14)
    # stencils
    s += ('<g transform="translate(150,205)" fill="#fff" opacity="0.92">'
          '<path d="M0,0 l0,-34 l-14,0 l24,-27 l24,27 l-14,0 l0,34 Z"/>'
          '<text x="46" y="0" font-family="Stencil" font-size="54" textLength="360" lengthAdjust="spacingAndGlyphs">THIS SIDE UP</text></g>\n')
    s += (f'<text transform="translate(222,552) scale(0.82,1)" text-anchor="middle" font-family="Stencil" '
          f'font-size="140" fill="{YEL}">01</text>\n')
    s += ('<text x="1505" y="302" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="21" '
          'fill="#fff" fill-opacity="0.85" letter-spacing="5">CASE Nº CC-2026-0001 · HANDLE WITH CARE</text>\n')
    s += (f'<text x="1505" y="1266" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="22" '
          f'fill="{YEL}" letter-spacing="6">CRAFT IT · BUILD IT · OPEN IT</text>\n')
    return page(s)


def spray_layer():
    tx, ty, tl = 1532, 520, 760
    text = "BLUEPRINT CASE"
    common = (f'x="{tx}" y="{ty}" text-anchor="middle" font-family="Stencil" font-size="94" '
              f'textLength="{tl}" lengthAdjust="spacingAndGlyphs"')
    s = f'<text {common} fill="{YEL}" opacity="0.5" filter="url(#spray)">{text}</text>\n'
    s += '<g fill="#FFE100">\n'
    for _ in range(320):
        x = gen.rnd.uniform(tx - tl / 2 - 30, tx + tl / 2 + 30)
        y = gen.rnd.gauss(ty - 36, 30)
        s += f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{gen.rnd.uniform(0.6, 2.2):.2f}" opacity="{gen.rnd.uniform(0.25, 0.75):.2f}"/>\n'
    s += "</g>\n"
    s += f'<g fill="{YEL}">\n'
    for x, L, w in [(1218, 60, 6), (1300, 92, 7), (1395, 70, 5.5), (1478, 98, 6.5),
                    (1590, 150, 7.5), (1690, 110, 6.5), (1795, 64, 5.5), (1872, 44, 5)]:
        y0 = ty - 6
        s += (f'  <path d="M{x - w/2:.1f},{y0} L{x - w/2:.1f},{y0 + L} A{w/2:.2f},{w/2:.2f} 0 0 0 {x + w/2:.1f},{y0 + L} '
              f'L{x + w/2:.1f},{y0} Z"/>\n')
        s += f'  <ellipse cx="{x}" cy="{y0 + L + 1}" rx="{w*0.62:.2f}" ry="{w*0.8:.2f}"/>\n'
    s += "</g>\n"
    s += f'<text {common} fill="{YEL}">{text}</text>\n'
    return page(s)


def stickers_layer():
    s = ""
    # NAVI die-cut on the lid's left end
    s += (f'<g transform="translate(690,290) rotate(-6) scale(1.12)" filter="url(#shadow)">'
          f'<rect x="-104" y="-44" width="208" height="88" rx="16" fill="#f4f4f2"/>'
          f'<rect x="-96" y="-36" width="192" height="72" rx="11" fill="{YEL}"/>'
          f'<rect x="-96" y="-36" width="192" height="72" rx="11" fill="none" stroke="{BLK}" stroke-width="5"/>'
          f'<text y="21" text-anchor="middle" font-family="Ops" font-size="60" fill="{BLK}" letter-spacing="4">NAVI</text></g>\n')
    # hard-hat badge and BUILD MODE on the corner pillar
    s += hardhat_sticker(748, 748, 1.18, 10)
    s += (f'<g transform="translate(752,972) rotate(-8) scale(0.88)" filter="url(#shadow)">'
          f'<text text-anchor="middle" y="16" font-family="Marker" font-size="58" fill="none" stroke="#fff" stroke-width="18" stroke-linejoin="round">BUILD MODE</text>'
          f'<text text-anchor="middle" y="16" font-family="Marker" font-size="58" fill="none" stroke="{BLK}" stroke-width="7" stroke-linejoin="round">BUILD MODE</text>'
          f'<text text-anchor="middle" y="16" font-family="Marker" font-size="58" fill="url(#buildGrad)">BUILD MODE</text></g>\n')
    # FRAGILE label on the side door panel (squeezed for the side's perspective)
    s += (f'<g transform="translate(378,846) scale(0.86,1.05) rotate(4)" filter="url(#shadow)">'
          f'<rect x="-82" y="-78" width="164" height="156" rx="8" fill="#f4f4f2"/>'
          f'<rect x="-72" y="-68" width="144" height="136" rx="4" fill="#f2efe6"/>'
          f'<rect x="-66" y="-62" width="132" height="124" rx="3" fill="none" stroke="#d32f2f" stroke-width="4"/>'
          f'<path d="M-14,-50 L14,-50 L10,-20 Q0,-10 -10,-20 Z M-2,-14 L-2,10 M-12,12 L10,12" fill="none" stroke="#d32f2f" stroke-width="4" stroke-linejoin="round"/>'
          f'<path d="M-4,-48 L2,-38 L-3,-31 L3,-24" fill="none" stroke="#f2efe6" stroke-width="2.4"/>'
          f'<text y="38" text-anchor="middle" font-family="Ops" font-size="27" fill="#d32f2f">FRAGILE</text>'
          f'<text y="55" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="10.5" fill="#1d1d1d" letter-spacing="0.6">CONTAINS KNIVES</text>'
          f'</g>\n')
    # caution tape across the lower-left corner
    txt = "CAUTION ▲ CASE UNDER CONSTRUCTION ▲ CAUTION ▲ CASE UNDER CONSTRUCTION ▲ CAUTION"
    s += (f'<g transform="translate(30,1000) rotate(22)" filter="url(#shadow)">'
          f'<rect x="0" y="-31" width="690" height="62" fill="{YEL}"/>'
          f'<rect x="0" y="-31" width="690" height="6" fill="{BLK}"/>'
          f'<rect x="0" y="25" width="690" height="6" fill="{BLK}"/>'
          f'<clipPath id="tapeClip"><rect x="0" y="-31" width="690" height="62"/></clipPath>'
          f'<text x="16" y="10" font-family="Ops" font-size="27" fill="{BLK}" letter-spacing="1.4" clip-path="url(#tapeClip)">{txt}</text>'
          f'<rect x="0" y="-31" width="690" height="62" fill="url(#tapeShade)"/></g>\n')
    return page(s)


if __name__ == "__main__":
    gen.rnd.seed(21)
    open(f"{OUT}/paint.html", "w").write(paint_layer())
    open(f"{OUT}/spray.html", "w").write(spray_layer())
    open(f"{OUT}/stickers.html", "w").write(stickers_layer())
    print("ok")
