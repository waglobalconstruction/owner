# NAVI × CS:GO Skins — Case Craft: «Blueprint Case»

Дизайн кейса для конкурса **Case Craft** (NAVI × CS:GO Skins).

**Идея:** «craft» — значит строить. Кейс оформлен как инженерный чертёж
(blueprint), а жёлто-чёрная строительная разметка совпадает с фирменными
цветами NAVI. Внутри «по чертежу» — редкий нож.

| Файл | Что это |
|---|---|
| `blueprint-case.png` | Основная работа для загрузки в форму (3200×2400, тёмный фон) |
| `blueprint-case-transparent.png` | Тот же кейс без фона (PNG с прозрачностью) |
| `source/gen.py`, `source/render.js` | Исходник (SVG-генератор) и рендер через Playwright |

## Как перерисовать

```bash
# шрифты (Google Fonts, OFL): Saira Stencil One, Black Ops One, Permanent Marker
python3 source/gen.py OUT_DIR FONTS_DIR      # создаёт case.html и case_clean.html
node source/render.js OUT_DIR/case.html blueprint-case.png 2
node source/render.js OUT_DIR/case_clean.html blueprint-case-transparent.png 2 transparent
```
