"""'Blueprint Case' livery on a front-view armoured chest (the contest's case format).

Usage: python3 chest.py OUT_DIR FONT_DIR   -> OUT_DIR/chest.html, OUT_DIR/chest_clean.html
Reuses drawing helpers from gen.py.
"""
import gen
from gen import (W, H, YEL, BLK, INK, DEFS, knife, iso_view, title_block, stamp,
                 hardhat_sticker, rivet, scratches, fonts_css)

OUT = gen.OUT

# geometry (front view, seen slightly from above)
TB_Y, TF_Y = 300, 380            # lid top: back / front edge
TB_X0, TB_X1 = 250, 1350
TF_X0, TF_X1 = 190, 1410
LID_Y1 = 520                     # lid front bottom
SEAM_Y1 = 532
BODY_X0, BODY_X1, BODY_Y1 = 200, 1400, 960
PL_X0, PL_X1, PL_Y1 = 182, 1418, 1004
PIL = [(196, 266), (1334, 1404)]       # corner pillars
STR = [(352, 420), (1180, 1248)]       # straps
BUMP_Y0 = 920


def back_x(x):
    return TB_X0 + (x - TF_X0) * (TB_X1 - TB_X0) / (TF_X1 - TF_X0)


EXTRA_DEFS = f"""
<defs>
  <linearGradient id="lidFront" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2069cf"/>
    <stop offset="1" stop-color="#0f4594"/>
  </linearGradient>
  <linearGradient id="bodyFront" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#15529f"/>
    <stop offset="1" stop-color="#0a3170"/>
  </linearGradient>
  <linearGradient id="lidTop" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#2a6fcc"/>
    <stop offset="1" stop-color="#3a86e6"/>
  </linearGradient>
  <linearGradient id="pillar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#2a2f36"/>
    <stop offset="0.35" stop-color="#7d858f"/>
    <stop offset="0.6" stop-color="#4c535c"/>
    <stop offset="1" stop-color="#1c2025"/>
  </linearGradient>
  <linearGradient id="strapShade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000" stop-opacity="0.35"/>
    <stop offset="0.3" stop-color="#fff" stop-opacity="0.12"/>
    <stop offset="0.7" stop-color="#000" stop-opacity="0.05"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.4"/>
  </linearGradient>
  <linearGradient id="plinth" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#5a616a"/>
    <stop offset="0.4" stop-color="#2c3137"/>
    <stop offset="1" stop-color="#121417"/>
  </linearGradient>
  <linearGradient id="buildGrad" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ff4fb8"/>
    <stop offset="0.5" stop-color="#ffd23a"/>
    <stop offset="1" stop-color="#3fe0ff"/>
  </linearGradient>
  <radialGradient id="bodyVig" cx="0.5" cy="0.4" r="0.75">
    <stop offset="0.5" stop-color="#000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.45"/>
  </radialGradient>
  <clipPath id="lidTopClip"><polygon points="{TB_X0},{TB_Y} {TB_X1},{TB_Y} {TF_X1},{TF_Y} {TF_X0},{TF_Y}"/></clipPath>
  <clipPath id="lidFrontClip"><rect x="{TF_X0}" y="{TF_Y}" width="{TF_X1-TF_X0}" height="{LID_Y1-TF_Y}"/></clipPath>
  <clipPath id="bodyClip"><rect x="{BODY_X0}" y="{SEAM_Y1}" width="{BODY_X1-BODY_X0}" height="{BODY_Y1-SEAM_Y1}"/></clipPath>
  <clipPath id="caseClip">
    <polygon points="{TB_X0},{TB_Y} {TB_X1},{TB_Y} {TF_X1},{TF_Y} {TF_X0},{TF_Y}"/>
    <rect x="{TF_X0}" y="{TF_Y}" width="{TF_X1-TF_X0}" height="{LID_Y1-TF_Y}"/>
    <rect x="{BODY_X0}" y="{LID_Y1}" width="{BODY_X1-BODY_X0}" height="{BODY_Y1-LID_Y1}"/>
    <rect x="{PL_X0}" y="{BODY_Y1}" width="{PL_X1-PL_X0}" height="{PL_Y1-BODY_Y1}" rx="8"/>
  </clipPath>
</defs>
"""


def grid(clip, x, y, w, h, base):
    return (f'<g clip-path="url(#{clip})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{base})"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#gridMinor)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#gridMajor)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#paperNoise)"/></g>\n')


def lid_top():
    s = grid("lidTopClip", TF_X0, TB_Y, TF_X1 - TF_X0, TF_Y - TB_Y, "lidTop")
    # ribs along the lid top
    for y in (318, 362):
        s += f'<line x1="{back_x(TF_X0)+20}" y1="{y}" x2="{back_x(TF_X1)-20}" y2="{y}" stroke="#0b3b85" stroke-width="7" stroke-linecap="round" clip-path="url(#lidTopClip)"/>\n'
        s += f'<line x1="{back_x(TF_X0)+20}" y1="{y-2}" x2="{back_x(TF_X1)-20}" y2="{y-2}" stroke="#fff" stroke-opacity="0.25" stroke-width="2" clip-path="url(#lidTopClip)"/>\n'
    # THIS SIDE UP stencil (squashed for perspective)
    s += ('<g transform="translate(478,354) scale(1,0.6)" fill="#fff" opacity="0.92">'
          '<path d="M0,0 l0,-30 l-11,0 l19,-22 l19,22 l-11,0 l0,30 Z"/>'
          '<text x="34" y="0" font-family="Stencil" font-size="40" textLength="190" lengthAdjust="spacingAndGlyphs">THIS SIDE UP</text></g>\n')
    # NAVI sticker on the lid top
    s += (f'<g transform="translate(800,341) scale(0.72,0.5) rotate(-4)" filter="url(#shadow)">'
          f'<rect x="-104" y="-44" width="208" height="88" rx="16" fill="#f4f4f2"/>'
          f'<rect x="-96" y="-36" width="192" height="72" rx="11" fill="{YEL}"/>'
          f'<rect x="-96" y="-36" width="192" height="72" rx="11" fill="none" stroke="{BLK}" stroke-width="5"/>'
          f'<text y="21" text-anchor="middle" font-family="Ops" font-size="60" fill="{BLK}" letter-spacing="4">NAVI</text></g>\n')
    # BUILD MODE graffiti sticker
    s += (f'<g transform="translate(1010,343) scale(0.66,0.48) rotate(4)" filter="url(#shadow)">'
          f'<text text-anchor="middle" y="16" font-family="Marker" font-size="50" fill="none" stroke="#fff" stroke-width="16" stroke-linejoin="round">BUILD MODE</text>'
          f'<text text-anchor="middle" y="16" font-family="Marker" font-size="50" fill="none" stroke="{BLK}" stroke-width="6" stroke-linejoin="round">BUILD MODE</text>'
          f'<text text-anchor="middle" y="16" font-family="Marker" font-size="50" fill="url(#buildGrad)">BUILD MODE</text></g>\n')
    s += f'<polygon points="{TB_X0},{TB_Y} {TB_X1},{TB_Y} {TF_X1},{TF_Y} {TF_X0},{TF_Y}" fill="#fff" opacity="0.04"/>\n'
    # pillar and strap tops
    for x0, x1 in PIL + STR:
        fill = "url(#pillar)" if (x0, x1) in PIL else YEL
        s += (f'<polygon points="{x0},{TF_Y} {x1},{TF_Y} {back_x(x1):.1f},{TB_Y} {back_x(x0):.1f},{TB_Y}" '
              f'fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>\n')
        if (x0, x1) in STR:
            s += (f'<polygon points="{x0},{TF_Y} {x1},{TF_Y} {back_x(x1):.1f},{TB_Y} {back_x(x0):.1f},{TB_Y}" '
                  f'fill="url(#haz)" opacity="0.9" stroke="{INK}" stroke-width="3"/>\n')
            s += (f'<polygon points="{x0},{TF_Y} {x1},{TF_Y} {back_x(x1):.1f},{TB_Y} {back_x(x0):.1f},{TB_Y}" fill="#fff" opacity="0.12"/>\n')
    s += f'<line x1="{TF_X0}" y1="{TF_Y}" x2="{TF_X1}" y2="{TF_Y}" stroke="#fff" stroke-opacity="0.55" stroke-width="3"/>\n'
    return s


def lid_front():
    s = grid("lidFrontClip", TF_X0, TF_Y, TF_X1 - TF_X0, LID_Y1 - TF_Y, "lidFront")
    s += f'<rect x="{TF_X0}" y="{LID_Y1-14}" width="{TF_X1-TF_X0}" height="14" fill="#000" opacity="0.25"/>\n'
    return s


def body():
    s = grid("bodyClip", BODY_X0, SEAM_Y1, BODY_X1 - BODY_X0, BODY_Y1 - SEAM_Y1, "bodyFront")
    # blueprint content (knife drawing, iso view, title block, stamp, hard-hat sticker)
    sc = 0.86
    tx, ty = 436 - 38 * sc, 600 - 155 * sc
    s += f'<g transform="translate({tx:.1f},{ty:.1f}) scale({sc})">\n'
    s += knife() + iso_view() + title_block() + stamp(642, 338, 48, -14) + hardhat_sticker(816, 270, 0.8, 12)
    s += "</g>\n"
    # hazard bumper with nameplate
    s += f'<rect x="{BODY_X0}" y="{BUMP_Y0}" width="{BODY_X1-BODY_X0}" height="{BODY_Y1-BUMP_Y0}" fill="url(#haz)"/>\n'
    s += f'<rect x="{BODY_X0}" y="{BUMP_Y0-5}" width="{BODY_X1-BODY_X0}" height="5" fill="#15181c"/>\n'
    s += (f'<g><rect x="640" y="{BUMP_Y0+5}" width="320" height="30" rx="4" fill="{BLK}" stroke="{YEL}" stroke-width="2"/>'
          f'<text x="800" y="{BUMP_Y0+25}" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="12.5" '
          f'fill="{YEL}" letter-spacing="1.6">CRAFT IT · BUILD IT · OPEN IT</text>'
          f'{rivet(652, BUMP_Y0+20, 3.2)}{rivet(948, BUMP_Y0+20, 3.2)}</g>\n')
    s += f'<rect x="{BODY_X0}" y="{SEAM_Y1}" width="{BODY_X1-BODY_X0}" height="{BODY_Y1-SEAM_Y1}" fill="url(#bodyVig)"/>\n'
    return s


def seam():
    return (f'<rect x="{BODY_X0}" y="{LID_Y1}" width="{BODY_X1-BODY_X0}" height="{SEAM_Y1-LID_Y1}" fill="#04132e"/>\n'
            f'<rect x="{BODY_X0}" y="{SEAM_Y1}" width="{BODY_X1-BODY_X0}" height="2" fill="#fff" opacity="0.2"/>\n')


def pillars_and_straps():
    s = ""
    for x0, x1 in PIL:
        for (y0, y1) in ((TF_Y, LID_Y1), (SEAM_Y1, BODY_Y1)):
            s += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="url(#pillar)" stroke="{INK}" stroke-width="3"/>\n'
            for yy in range(y0 + 22, y1 - 10, 46):
                s += rivet((x0 + x1) / 2, yy, 5) + "\n"
    for x0, x1 in STR:
        for (y0, y1) in ((TF_Y, LID_Y1), (SEAM_Y1, BODY_Y1)):
            s += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="url(#haz)" stroke="{INK}" stroke-width="3"/>\n'
            s += f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="url(#strapShade)"/>\n'
            s += rivet(x0 + 14, y0 + 16, 4) + rivet(x1 - 14, y0 + 16, 4) + rivet(x0 + 14, y1 - 16, 4) + rivet(x1 - 14, y1 - 16, 4) + "\n"
    return s


def spray_title():
    tx, ty, tl = 800, 490, 700
    text = "BLUEPRINT CASE"
    common = (f'x="{tx}" y="{ty}" text-anchor="middle" font-family="Stencil" font-size="100" '
              f'textLength="{tl}" lengthAdjust="spacingAndGlyphs"')
    s = f'<text {common} fill="{YEL}" opacity="0.55" filter="url(#spray)">{text}</text>\n'
    s += '<g fill="#FFE100">\n'
    for _ in range(300):
        x = gen.rnd.uniform(tx - tl / 2 - 40, tx + tl / 2 + 40)
        y = gen.rnd.gauss(ty - 36, 34)
        if y < TF_Y + 4:
            continue
        s += f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="{gen.rnd.uniform(0.5, 2):.2f}" opacity="{gen.rnd.uniform(0.25, 0.75):.2f}"/>\n'
    s += "</g>\n"
    s += f'<g fill="{YEL}">\n'
    for x, L, w in [(492, 40, 5.5), (590, 66, 6.5), (700, 46, 5), (812, 110, 7), (930, 58, 6), (1040, 84, 6), (1120, 36, 4.5)]:
        y0 = ty - 6
        s += (f'  <path d="M{x - w/2:.1f},{y0} L{x - w/2:.1f},{y0 + L} A{w/2:.2f},{w/2:.2f} 0 0 0 {x + w/2:.1f},{y0 + L} '
              f'L{x + w/2:.1f},{y0} Z"/>\n')
        s += f'  <ellipse cx="{x}" cy="{y0 + L + 1}" rx="{w*0.62:.2f}" ry="{w*0.8:.2f}"/>\n'
    s += "</g>\n"
    s += f'<text {common} fill="{YEL}">{text}</text>\n'
    return s


def latch(cx):
    y0 = LID_Y1 - 50
    return f"""
<g filter="url(#shadow)">
  <rect x="{cx - 40}" y="{y0}" width="80" height="104" rx="9" fill="#15181c"/>
  <rect x="{cx - 35}" y="{y0 + 4}" width="70" height="96" rx="7" fill="url(#metalH)"/>
  <rect x="{cx - 25}" y="{y0 + 14}" width="50" height="60" rx="5" fill="{YEL}" stroke="#15181c" stroke-width="3"/>
  <rect x="{cx - 15}" y="{y0 + 25}" width="30" height="7" rx="3.5" fill="#15181c"/>
  <rect x="{cx - 15}" y="{y0 + 39}" width="30" height="7" rx="3.5" fill="#15181c"/>
  <rect x="{cx - 15}" y="{y0 + 53}" width="30" height="7" rx="3.5" fill="#15181c"/>
  {rivet(cx - 23, y0 + 88, 4)}{rivet(cx + 23, y0 + 88, 4)}
</g>
"""


def fragile():
    return (f'<g transform="translate(1262,820) rotate(7) scale(0.86)" filter="url(#shadow)">'
            f'<rect x="-82" y="-78" width="164" height="156" rx="8" fill="#f4f4f2"/>'
            f'<rect x="-72" y="-68" width="144" height="136" rx="4" fill="#f2efe6"/>'
            f'<rect x="-66" y="-62" width="132" height="124" rx="3" fill="none" stroke="#d32f2f" stroke-width="4"/>'
            f'<path d="M-14,-50 L14,-50 L10,-20 Q0,-10 -10,-20 Z M-2,-14 L-2,10 M-12,12 L10,12" fill="none" stroke="#d32f2f" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-4,-48 L2,-38 L-3,-31 L3,-24" fill="none" stroke="#f2efe6" stroke-width="2.4"/>'
            f'<text y="38" text-anchor="middle" font-family="Ops" font-size="27" fill="#d32f2f">FRAGILE</text>'
            f'<text y="55" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="10.5" fill="#1d1d1d" letter-spacing="0.6">CONTAINS KNIVES</text>'
            f'</g>\n')


def caution_tape():
    txt = "CAUTION ▲ CASE UNDER CONSTRUCTION ▲ CAUTION ▲ CASE UNDER CONSTRUCTION"
    return f"""
<g clip-path="url(#caseClip)">
 <g transform="translate(120,770) rotate(26)" filter="url(#shadow)">
  <rect x="0" y="-24" width="620" height="48" fill="{YEL}"/>
  <rect x="0" y="-24" width="620" height="5" fill="{BLK}"/>
  <rect x="0" y="19" width="620" height="5" fill="{BLK}"/>
  <text x="14" y="8" font-family="Ops" font-size="21" fill="{BLK}" letter-spacing="1.2">{txt}</text>
  <rect x="0" y="-24" width="620" height="48" fill="url(#tapeShade)"/>
 </g>
</g>
"""


def plinth():
    s = f'<rect x="{PL_X0}" y="{BODY_Y1}" width="{PL_X1-PL_X0}" height="{PL_Y1-BODY_Y1}" rx="8" fill="url(#plinth)" stroke="{INK}" stroke-width="3"/>\n'
    for x in range(PL_X0 + 40, PL_X1 - 20, 120):
        s += rivet(x, (BODY_Y1 + PL_Y1) / 2, 4.5)
    s += "\n"
    return s


def wear():
    s = '<g clip-path="url(#caseClip)">\n'
    s += f'<g transform="translate({BODY_X0},{TB_Y})">' + scratches(BODY_X1 - BODY_X0, PL_Y1 - TB_Y, 120) + '</g>\n'
    s += f'<rect x="{TF_X0}" y="{TB_Y}" width="{TF_X1-TF_X0}" height="{PL_Y1-TB_Y}" fill="url(#sheen)"/>\n'
    s += "</g>\n"
    return s


def outline():
    p = (f"M{TB_X0},{TB_Y} L{TB_X1},{TB_Y} L{TF_X1},{TF_Y} L{TF_X1},{LID_Y1} L{BODY_X1},{LID_Y1} "
         f"L{BODY_X1},{BODY_Y1} L{PL_X1},{BODY_Y1} L{PL_X1},{PL_Y1} L{PL_X0},{PL_Y1} L{PL_X0},{BODY_Y1} "
         f"L{BODY_X0},{BODY_Y1} L{BODY_X0},{LID_Y1} L{TF_X0},{LID_Y1} L{TF_X0},{TF_Y} Z")
    return (f'<path d="{p}" fill="none" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>\n'
            f'<line x1="{TF_X0}" y1="{TF_Y}" x2="{TF_X1}" y2="{TF_Y}" stroke="{INK}" stroke-width="4"/>\n'
            f'<line x1="{TF_X0}" y1="{LID_Y1}" x2="{TF_X1}" y2="{LID_Y1}" stroke="{INK}" stroke-width="5"/>\n')


def background():
    return f"""
<rect width="{W}" height="{H}" fill="url(#studio)"/>
<rect width="{W}" height="{H}" fill="url(#bgGrid)"/>
<ellipse cx="800" cy="1010" rx="780" ry="110" fill="url(#floorGlow)"/>
"""


def floor_shadow():
    return (f'<ellipse cx="800" cy="{PL_Y1 + 4}" rx="690" ry="34" fill="#000" opacity="0.8" filter="url(#floorBlur)"/>\n')


def build(with_bg):
    gen.rnd.seed(11)
    svg = f'<svg id="art" xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">\n'
    svg += DEFS + EXTRA_DEFS
    if with_bg:
        svg += background()
    svg += floor_shadow()
    svg += lid_top() + lid_front() + body() + seam() + pillars_and_straps()
    svg += spray_title() + latch(386) + latch(1214)
    svg += caution_tape() + fragile() + plinth() + wear() + outline()
    svg += "</svg>\n"
    bg = "#0b0c0e" if with_bg else "transparent"
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
{fonts_css()}
html,body{{margin:0;padding:0;background:{bg};}}
svg{{display:block;}}
</style></head><body>
<div style="position:absolute;left:-9999px;font-family:Stencil">a</div>
<div style="position:absolute;left:-9999px;font-family:Ops">a</div>
<div style="position:absolute;left:-9999px;font-family:Marker">a</div>
{svg}</body></html>"""


if __name__ == "__main__":
    open(f"{OUT}/chest.html", "w").write(build(True))
    open(f"{OUT}/chest_clean.html", "w").write(build(False))
    print("ok")
