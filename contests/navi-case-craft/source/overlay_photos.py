"""'NAVI LEGENDS CASE' with NAVI's official championship photos.

Usage: python3 overlay_photos.py OUT_DIR FONT_DIR PHOTO_DIR
  PHOTO_DIR holds h2010.webp, h2021.webp, h2024.png (navi.gg/en/company/history banners).
Writes graded photo crops plus OUT_DIR/{photo,paint,spray,stickers}.html (2393x1481).
"""
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import overlay
import overlay_legends as L
from overlay import page, pts, FRONT_SHEET, SIDE_SHEET, YEL, BLK

OUT = overlay.OUT
PHOTOS = sys.argv[3]


def grade(img, warmth=0.42, vignette=0.55):
    """Unify photos from different years: warm gold duotone mixed with the original colour."""
    img = ImageEnhance.Contrast(img.convert("RGB")).enhance(1.12)
    a = np.asarray(img).astype(np.float32) / 255.0
    lum = a @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    stops = np.array([0.0, 0.3, 0.62, 0.85, 1.0])
    cols = np.array([(6, 4, 2), (60, 38, 10), (196, 140, 40), (250, 214, 120), (255, 248, 226)], dtype=np.float32) / 255
    duo = np.stack([np.interp(lum, stops, cols[:, c]) for c in range(3)], axis=-1)
    outp = a * (1 - warmth) + duo * warmth
    h, w = lum.shape
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    outp *= (1 - vignette * np.clip(r - 0.55, 0, 1) ** 1.5)[..., None]
    return Image.fromarray((np.clip(outp, 0, 1) * 255).astype(np.uint8))


def crop(fn, box, size, **kw):
    im = Image.open(f"{PHOTOS}/{fn}").convert("RGB").crop(box).resize(size, Image.LANCZOS)
    return grade(im, **kw)


# front recessed panel: 2021 Stockholm Major (s1mple lifting the trophy)
crop("h2021.webp", (540, 420, 1190, 916), (1040, 794), warmth=0.30).save(f"{OUT}/p2021.png")
# side door: 2024 Copenhagen Major (trophy + Ukrainian flags)
crop("h2024.png", (860, 20, 1400, 1000), (540, 980), warmth=0.30).save(f"{OUT}/p2024.png")
# polaroid on the pillar: 2010 IEM World Championship
crop("h2010.webp", (560, 40, 1460, 990), (720, 760), warmth=0.45, vignette=0.35).save(f"{OUT}/p2010.png")


def photo_layer():
    s = f"""
<defs>
  <clipPath id="fClip"><polygon points="{pts(FRONT_SHEET)}"/></clipPath>
  <clipPath id="sClip"><polygon points="{pts(SIDE_SHEET)}"/></clipPath>
</defs>
<g clip-path="url(#fClip)">
  <image href="file://{OUT}/p2021.png" x="1150" y="520" width="710" height="546" preserveAspectRatio="xMidYMid slice"/>
  <rect x="1150" y="1066" width="710" height="100" fill="#000"/>
</g>
<g clip-path="url(#sClip)">
  <image href="file://{OUT}/p2024.png" x="250" y="590" width="252" height="520" preserveAspectRatio="xMidYMid slice"/>
</g>
"""
    return page(s)


def paint_layer():
    s = L.GOLD_DEFS
    s += """
<defs>
  <linearGradient id="fadeUp" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000" stop-opacity="0"/>
    <stop offset="0.55" stop-color="#000" stop-opacity="0.75"/>
    <stop offset="1" stop-color="#000" stop-opacity="0.95"/>
  </linearGradient>
</defs>
"""
    # front caption over the 2021 photo
    s += f'<g clip-path="url(#frontSheet)"><rect x="1150" y="930" width="710" height="140" fill="url(#fadeUp)"/></g>\n'
    s += L.engraved(1505, 1022, "2021 ★ PGL MAJOR STOCKHOLM", 34, anchor="middle", tl=560)
    s += L.engraved(1505, 1062, "s1mple · electronic · Boombl4 · Perfecto · b1t", 25, family="Inter", weight="900",
                    anchor="middle", tl=560, fill="#fff7e0")
    s += L.engraved(1505, 1098, "CHAMPIONS WITHOUT LOSING A SINGLE MAP", 13.5, family="JetBrains Mono", weight="800",
                    anchor="middle", ls=3, fill="#ffd54a")
    # gold frame lines on the two photo panels
    s += f'<polygon points="{pts(FRONT_SHEET)}" fill="none" stroke="url(#gold)" stroke-width="5" stroke-linejoin="round"/>\n'
    s += f'<polygon points="{pts(SIDE_SHEET)}" fill="none" stroke="url(#gold)" stroke-width="5"/>\n'
    # side-door caption over the 2024 photo (squeezed for perspective)
    s += f'<g clip-path="url(#sideSheet)"><rect x="250" y="930" width="260" height="175" fill="url(#fadeUp)"/></g>\n'
    s += '<g transform="translate(376,0) scale(0.84,1)">'
    s += L.engraved(0, 1006, "2024 ★", 50, anchor="middle")
    s += L.engraved(0, 1036, "COPENHAGEN MAJOR", 16, family="JetBrains Mono", weight="800", anchor="middle", ls=1.5, fill="#ffd54a")
    s += L.engraved(0, 1062, "Aleksib · iM · b1t", 17, family="Inter", weight="900", anchor="middle", fill="#fff7e0")
    s += L.engraved(0, 1084, "jL · w0nderful", 17, family="Inter", weight="900", anchor="middle", fill="#fff7e0")
    s += "</g>\n"
    # lid and rails
    s += L.engraved(150, 207, "NATUS VINCERE", 50, tl=410)
    s += ('<text x="1505" y="302" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="21" '
          'fill="#fff" fill-opacity="0.9" letter-spacing="5">NATUS VINCERE · 2× MAJOR CHAMPIONS</text>\n')
    s += ('<text x="1505" y="1266" text-anchor="middle" font-family="JetBrains Mono" font-weight="800" font-size="22" '
          'fill="#ffd54a" letter-spacing="7">BORN TO WIN · SINCE 2009</text>\n')
    return page(s)


def stickers_layer():
    s = L.GOLD_DEFS
    # NAVI die-cut on the lid's left end
    s += (f'<g transform="translate(690,290) rotate(-6) scale(1.12)" filter="url(#shadow)">'
          f'<rect x="-104" y="-44" width="208" height="88" rx="16" fill="#f4f4f2"/>'
          f'<rect x="-96" y="-36" width="192" height="72" rx="11" fill="{YEL}"/>'
          f'<rect x="-96" y="-36" width="192" height="72" rx="11" fill="none" stroke="{BLK}" stroke-width="5"/>'
          f'<text y="21" text-anchor="middle" font-family="Ops" font-size="60" fill="{BLK}" letter-spacing="4">NAVI</text></g>\n')
    # gold "2x Major champions" medal, side face top-left
    s += (f'<g transform="translate(222,492) rotate(-8) scale(0.92,1.0)" filter="url(#shadow)">'
          f'<circle r="80" fill="#f4f4f2"/>'
          f'<circle r="73" fill="url(#medal)"/>'
          f'<circle r="66" fill="{BLK}"/>'
          f'<text font-family="Ops" font-size="13.5" fill="#ffd54a" letter-spacing="1">'
          f'<textPath href="#medalRing" textLength="330" lengthAdjust="spacing">MAJOR CHAMPIONS ★ 2021 ★ 2024 ★ </textPath></text>'
          f'<circle r="42" fill="url(#medal)"/>'
          f'<text y="14" text-anchor="middle" font-family="Ops" font-size="44" fill="{BLK}">2×</text>'
          + L.star(-17, -22, 9, fill=BLK) + L.star(17, -22, 9, fill=BLK) +
          f'</g>\n')
    # 2010 polaroid on the corner pillar
    s += (f'<g transform="translate(752,836) rotate(-5)" filter="url(#shadow)">'
          f'<rect x="-136" y="-178" width="272" height="356" rx="4" fill="#f6f3ea"/>'
          f'<image href="file://{OUT}/p2010.png" x="-120" y="-162" width="240" height="253" preserveAspectRatio="xMidYMid slice"/>'
          f'<rect x="-120" y="-162" width="240" height="253" fill="none" stroke="#000" stroke-opacity="0.25"/>'
          f'<text x="0" y="128" text-anchor="middle" font-family="Marker" font-size="27" fill="#111" textLength="232" lengthAdjust="spacingAndGlyphs">2010 ★ Triple Crown</text>'
          f'<text x="0" y="160" text-anchor="middle" font-family="Marker" font-size="15.5" fill="#333" '
          f'textLength="236" lengthAdjust="spacingAndGlyphs">Zeus · markeloff · Edward · starix · ceh9</text>'
          f'<rect x="-46" y="-196" width="92" height="34" fill="#ffe36a" opacity="0.82" transform="rotate(3)"/>'
          f'</g>\n')
    return page(s)


if __name__ == "__main__":
    open(f"{OUT}/photo.html", "w").write(photo_layer())
    open(f"{OUT}/paint.html", "w").write(paint_layer())
    open(f"{OUT}/spray.html", "w").write(L.title_layer())
    open(f"{OUT}/stickers.html", "w").write(stickers_layer())
    print("ok")
