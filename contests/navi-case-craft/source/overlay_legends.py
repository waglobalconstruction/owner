"""'NAVI LEGENDS CASE' overlay layers for the contest template (2393x1481 px).

Usage: python3 overlay_legends.py OUT_DIR FONT_DIR -> OUT_DIR/{paint,spray,stickers}.html
"""
import overlay
from overlay import page, YEL, BLK

OUT = overlay.OUT

GOLD_DEFS = """
<defs>
  <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff4c2"/>
    <stop offset="0.38" stop-color="#ffd54a"/>
    <stop offset="0.62" stop-color="#d49a1c"/>
    <stop offset="1" stop-color="#ffe27a"/>
  </linearGradient>
  <linearGradient id="goldH" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#b5800f"/>
    <stop offset="0.5" stop-color="#ffe9a0"/>
    <stop offset="1" stop-color="#b5800f"/>
  </linearGradient>
  <radialGradient id="medal" cx="0.4" cy="0.35" r="0.75">
    <stop offset="0" stop-color="#fff6cf"/>
    <stop offset="0.45" stop-color="#ffd24a"/>
    <stop offset="1" stop-color="#a8730c"/>
  </radialGradient>
  <filter id="glow" x="-20%" y="-60%" width="140%" height="220%">
    <feGaussianBlur stdDeviation="9"/>
  </filter>
  <path id="medalRing" d="M0,0 m-54,0 a54,54 0 1,1 108,0 a54,54 0 1,1 -108,0"/>
</defs>
"""


def star(cx, cy, r, fill="url(#gold)", extra=""):
    pts = []
    import math
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" {extra}/>'


def engraved(x, y, text, size, family="Ops", anchor="start", fill="url(#gold)", tl=None, ls=0, weight="400", extra=""):
    t = f' textLength="{tl}" lengthAdjust="spacingAndGlyphs"' if tl else ""
    common = (f'x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" font-weight="{weight}" '
              f'font-size="{size}" letter-spacing="{ls}"{t} {extra}')
    return (f'<text {common} fill="#000" fill-opacity="0.65" transform="translate(0,{max(2, size*0.05):.1f})">{text}</text>'
            f'<text {common} fill="{fill}">{text}</text>\n')


ROWS = [
    ("2010", False, "TRIPLE CROWN", "IEM · ESWC · ARBALET CUP", "Zeus · markeloff · Edward · starix · ceh9"),
    ("2021", True, "STOCKHOLM MAJOR", "CHAMPIONS · 0 MAPS LOST", "s1mple · electronic · Boombl4 · Perfecto · b1t"),
    ("2024", True, "COPENHAGEN MAJOR", "FIRST CS2 MAJOR CHAMPIONS", "Aleksib · iM · b1t · jL · w0nderful"),
]


def hall_of_fame():
    s = ""
    x0, x1 = 1204, 1806
    s += engraved(1505, 598, "HALL OF FAME", 24, anchor="middle", ls=9)
    s += f'<rect x="{x0}" y="584" width="120" height="2.5" fill="url(#goldH)"/><rect x="{x1-120}" y="584" width="120" height="2.5" fill="url(#goldH)"/>\n'
    y = 622
    for year, major, label, sub, names in ROWS:
        s += engraved(x0, y + 54, year, 54)
        if major:
            s += star(x0 + 172, y + 34, 17)
        s += engraved(x0 + 206, y + 30, label, 19, family="JetBrains Mono", weight="800", ls=3, fill="#ffd54a")
        s += engraved(x0 + 206, y + 54, sub, 13.5, family="JetBrains Mono", weight="700", ls=2, fill="#fff1c4")
        s += engraved(x0, y + 100, names, 27, family="Inter", weight="900", tl=x1 - x0, fill="#fff7e0")
        s += f'<rect x="{x0}" y="{y + 118}" width="{x1 - x0}" height="2" fill="url(#goldH)" opacity="0.8"/>\n'
        y += 130
    s += engraved(1505, y + 22, "COACH B1ad3  ·  ICONS GuardiaN · flamie · seized", 16, family="JetBrains Mono",
                  weight="800", anchor="middle", tl=x1 - x0 - 20, fill="#ffd54a")
    s += engraved(1505, y + 52, "NATUS VINCERE · EST. 2009", 14, family="JetBrains Mono",
                  weight="700", anchor="middle", ls=6, fill="#fff1c4")
    return s


def paint_layer():
    s = GOLD_DEFS
    s += hall_of_fame()
    # lid's left end
    s += engraved(150, 207, "NATUS VINCERE", 50, tl=410)
    # side face: EST. 2009 and stacked BORN TO WIN on the door panel
    s += f'<g transform="translate(222,0) scale(0.84,1)">'
    s += engraved(0, 466, "EST.", 30, anchor="middle", ls=4)
    s += engraved(0, 548, "2009", 74, anchor="middle")
    s += "</g>\n"
    s += '<g transform="translate(376,0) scale(0.84,1)">'
    s += engraved(0, 712, "BORN", 84, anchor="middle", tl=250)
    s += engraved(0, 792, "TO", 62, anchor="middle")
    s += engraved(0, 900, "WIN", 96, anchor="middle", tl=230)
    s += star(-52, 975, 26) + star(52, 975, 26)
    s += "</g>\n"
    s += ('<text x="1505" y="302" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="21" '
          'fill="#fff" fill-opacity="0.9" letter-spacing="5">NATUS VINCERE · 2× MAJOR CHAMPIONS</text>\n')
    s += ('<text x="1505" y="1266" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="22" '
          'fill="#ffd54a" letter-spacing="7">BORN TO WIN · SINCE 2009</text>\n')
    return page(s)


def title_layer():
    s = GOLD_DEFS
    tx, ty, tl = 1532, 516, 640
    common = (f'x="{tx}" y="{ty}" text-anchor="middle" font-family="Ops" font-size="92" '
              f'textLength="{tl}" lengthAdjust="spacingAndGlyphs"')
    s += f'<text {common} fill="#ffcf2e" opacity="0.55" filter="url(#glow)">LEGENDS CASE</text>\n'
    s += f'<text {common} fill="#000" fill-opacity="0.7" transform="translate(0,4)">LEGENDS CASE</text>\n'
    s += f'<text {common} fill="url(#gold)">LEGENDS CASE</text>\n'
    for cx in (1172, 1892):
        s += star(cx, 482, 34, fill="#ffcf2e", extra='opacity="0.5" filter="url(#glow)"')
        s += star(cx, 485, 30, fill="#000", extra='opacity="0.6"')
        s += star(cx, 482, 30)
    return page(s)


def stickers_layer():
    s = GOLD_DEFS
    # NAVI die-cut on the lid's left end
    s += (f'<g transform="translate(690,290) rotate(-6) scale(1.12)" filter="url(#shadow)">'
          f'<rect x="-104" y="-44" width="208" height="88" rx="16" fill="#f4f4f2"/>'
          f'<rect x="-96" y="-36" width="192" height="72" rx="11" fill="{YEL}"/>'
          f'<rect x="-96" y="-36" width="192" height="72" rx="11" fill="none" stroke="{BLK}" stroke-width="5"/>'
          f'<text y="21" text-anchor="middle" font-family="Ops" font-size="60" fill="{BLK}" letter-spacing="4">NAVI</text></g>\n')
    # gold "2x Major champions" medal on the corner pillar
    s += (f'<g transform="translate(750,752) rotate(-8) scale(1.22)" filter="url(#shadow)">'
          f'<circle r="80" fill="#f4f4f2"/>'
          f'<circle r="73" fill="url(#medal)"/>'
          f'<circle r="66" fill="{BLK}"/>'
          f'<text font-family="Ops" font-size="13.5" fill="#ffd54a" letter-spacing="1">'
          f'<textPath href="#medalRing" textLength="330" lengthAdjust="spacing">MAJOR CHAMPIONS ★ 2021 ★ 2024 ★ </textPath></text>'
          f'<circle r="42" fill="url(#medal)"/>'
          f'<text y="14" text-anchor="middle" font-family="Ops" font-size="44" fill="{BLK}">2×</text>'
          + star(-17, -22, 9, fill=BLK) + star(17, -22, 9, fill=BLK) +
          f'</g>\n')
    # Ukrainian flag sticker lower on the pillar
    s += (f'<g transform="translate(748,990) rotate(-6)" filter="url(#shadow)">'
          f'<rect x="-86" y="-58" width="172" height="116" rx="12" fill="#f4f4f2"/>'
          f'<rect x="-78" y="-50" width="156" height="50" fill="#0057B7"/>'
          f'<rect x="-78" y="0" width="156" height="50" fill="#FFD700"/>'
          f'</g>\n')
    return page(s)


if __name__ == "__main__":
    open(f"{OUT}/paint.html", "w").write(paint_layer())
    open(f"{OUT}/spray.html", "w").write(title_layer())
    open(f"{OUT}/stickers.html", "w").write(stickers_layer())
    print("ok")
