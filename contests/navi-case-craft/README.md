# NAVI × CS:GO Skins — Case Craft: «Blueprint Case»

Дизайн кейса для конкурса **Case Craft** (NAVI × CS:GO Skins).

**Идея:** «craft» — значит строить. Кейс оформлен как инженерный чертёж
(blueprint), а жёлто-чёрная строительная разметка совпадает с фирменными
цветами NAVI. Внутри «по чертежу» — редкий нож.

| Файл | Что это |
|---|---|
| `blueprint-case-template.png` | **Работа для формы** — дизайн на официальном чистом кейсе конкурса (2393×1481, прозрачный фон, как шаблон) |
| `blueprint-case-template-showcase.png` | Та же работа на тёмном фоне — для показа / соцсетей |
| `blueprint-chest.png` | Рисованная версия в форме сундука (3200×2400) |
| `blueprint-chest-transparent.png` | Сундук без фона (PNG с прозрачностью) |
| `blueprint-case.png` | Альтернативный вариант — кейс-чемодан в 3/4 |
| `blueprint-case-transparent.png` | Чемодан без фона |
| `source/recolor.py`, `source/overlay.py`, `source/render_layers.js` | Наложение на шаблон: перекраска по яркости + слои краски/спрея/наклеек |
| `source/chest.py`, `source/gen.py`, `source/render.js` | Рисованные версии (SVG-генераторы) и рендер через Playwright |

## Как перерисовать

```bash
# шрифты (Google Fonts, OFL): Saira Stencil One, Black Ops One, Permanent Marker
python3 source/chest.py OUT_DIR FONTS_DIR    # сундук: chest.html, chest_clean.html
python3 source/gen.py OUT_DIR FONTS_DIR      # чемодан: case.html, case_clean.html
node source/render.js OUT_DIR/case.html blueprint-case.png 2
node source/render.js OUT_DIR/case_clean.html blueprint-case-transparent.png 2 transparent
```

### Наложение на официальный шаблон

Нужна чистая картинка кейса из формы (ссылка «взяти її тут»), 2393×1481 PNG.

```bash
python3 source/overlay.py LAYERS_DIR FONTS_DIR        # paint/spray/stickers.html
node source/render_layers.js LAYERS_DIR               # -> paint/spray/stickers.png
python3 -I source/recolor.py template.png OUT_DIR LAYERS_DIR   # -> OUT_DIR/final.png
```

Корпус перекрашивается градиентной картой по яркости (фактура, царапины и блики
сохраняются), ремни крышки — в жёлто-чёрную полосу, фурнитура остаётся металлом,
логотип CSG○SKINS не трогается.
