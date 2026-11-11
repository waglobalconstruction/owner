# NAVI × CS:GO Skins — Case Craft

## Основная работа: «NAVI LEGENDS CASE» с фото чемпионов

Тот же чёрно-золотой кейс, но с официальными фото NAVI трёх чемпионских моментов:

- **спереди** — 2021, PGL Major Stockholm: s1mple поднимает трофей, рядом electronic · Boombl4 · Perfecto · b1t;
- **на боковой дверце** — 2024, Copenhagen Major с флагами Украины: Aleksib · iM · b1t · jL · w0nderful;
- **полароид на угловой стойке** — 2010, IEM World Championship: Zeus · markeloff · Edward · starix · ceh9.

Фото: официальные баннеры истории клуба NAVI (navi.gg/en/company/history), сведены в общую золотую гамму.

| Файл | Что это |
|---|---|
| `navi-legends-photo-template.png` | **Работа для формы** — на официальном чистом кейсе (2393×1481, прозрачный фон) |
| `navi-legends-photo-showcase.png` | Та же работа с золотым сиянием — для показа и соцсетей |

## Вариант без фото: «NAVI LEGENDS CASE» (Зала славы)

Чёрный матовый кейс с золотой фурнитурой и жёлтыми ремнями. На передней панели —
золотая «Зала славы» всех чемпионских составов NAVI:

- **2010 · Triple Crown** (IEM · ESWC · WCG) — Zeus · markeloff · Edward · starix · ceh9
- **2021 · Stockholm Major** (без единой проигранной карты) — s1mple · electronic · Boombl4 · Perfecto · b1t
- **2024 · Copenhagen Major** (первый мейджор CS2) — Aleksib · iM · b1t · jL · w0nderful
- Coach B1ad3 · Icons GuardiaN · flamie · seized

Плюс «LEGENDS CASE» с двумя звёздами мейджоров, «BORN TO WIN» (Natus Vincere — «рождённые побеждать»),
«EST. 2009», медаль «2× Major Champions», наклейка NAVI и флаг Украины.

| Файл | Что это |
|---|---|
| `navi-legends-case-template.png` | **Работа для формы** — на официальном чистом кейсе (2393×1481, прозрачный фон) |
| `navi-legends-case-showcase.png` | Та же работа с золотым сиянием — для показа и соцсетей |

## Запасной вариант: «Blueprint Case»

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
python3 -I source/recolor.py template.png OUT_DIR LAYERS_DIR   # -> OUT_DIR/final.png (Blueprint)

# NAVI LEGENDS CASE:
python3 source/overlay_legends.py LAYERS_DIR FONTS_DIR && node source/render_layers.js LAYERS_DIR
python3 -I source/recolor.py template.png OUT_DIR LAYERS_DIR legends

# NAVI LEGENDS CASE с фото (PHOTO_DIR: h2010.webp, h2021.webp, h2024.png с navi.gg/en/company/history):
python3 source/overlay_photos.py LAYERS_DIR FONTS_DIR PHOTO_DIR && node source/render_layers.js LAYERS_DIR photo,paint,spray,stickers
python3 -I source/recolor.py template.png OUT_DIR LAYERS_DIR legends
python3 -I source/showcase.py OUT_DIR/final.png showcase.png
```

Корпус перекрашивается градиентной картой по яркости (фактура, царапины и блики
сохраняются), ремни крышки — в жёлто-чёрную полосу, фурнитура остаётся металлом,
логотип CSG○SKINS не трогается.
