# NAVI × CS:GO Skins — Case Craft: «Blueprint Case»

Дизайн кейса для конкурса **Case Craft** (NAVI × CS:GO Skins).

**Идея:** «craft» — значит строить. Кейс оформлен как инженерный чертёж
(blueprint), а жёлто-чёрная строительная разметка совпадает с фирменными
цветами NAVI. Внутри «по чертежу» — редкий нож.

| Файл | Что это |
|---|---|
| `blueprint-chest.png` | **Основная работа** — в формате кейса конкурса (сундук, 3200×2400) |
| `blueprint-chest-transparent.png` | Сундук без фона (PNG с прозрачностью) |
| `blueprint-case.png` | Альтернативный вариант — кейс-чемодан в 3/4 |
| `blueprint-case-transparent.png` | Чемодан без фона |
| `source/chest.py`, `source/gen.py`, `source/render.js` | Исходники (SVG-генераторы) и рендер через Playwright |

## Как перерисовать

```bash
# шрифты (Google Fonts, OFL): Saira Stencil One, Black Ops One, Permanent Marker
python3 source/chest.py OUT_DIR FONTS_DIR    # сундук: chest.html, chest_clean.html
python3 source/gen.py OUT_DIR FONTS_DIR      # чемодан: case.html, case_clean.html
node source/render.js OUT_DIR/case.html blueprint-case.png 2
node source/render.js OUT_DIR/case_clean.html blueprint-case-transparent.png 2 transparent
```
