# Global Construction — rules for Claude

## One design everywhere (owner's decision, 02.11.2026)

Every screen, page and document we make for Global follows the brand style of the October 2026 drying flyer.
This covers the Corporate Office, the crew app, the board, the login page, estimates, proposals, price lists and
client-facing pages. Do not invent a new look for a new page.

- Use `design/global.css` (tokens `--g-*`, classes `g-*`) and the logo `design/global-logo.svg`. `design/style-guide.html`
  shows every part; `design/README.md` has the rules.
- White cards on a cool ground, sky-blue hero panel (`g-sky`), one brand red `#D90A0A` for the main action or the one card
  that matters, charcoal band `#1E1E1E` at the bottom with (425) 683-3109, wa.globalconstruction@gmail.com and
  «Licensed · Bonded · Insured · WA Lic. CC GLOBACR761B9».
- Montserrat 800–900 for headlines and big numbers, Inter for text. Uppercase letter-spaced eyebrows. A red period at the
  end of a headline («Corporate Office.»).
- Status colours (ok green, waiting amber, overdue dark red) stay separate from the brand red.
- Light and dark theme both work; phone width (390 px) works.
- No Space Needle, real buildings or other trademarks in pictures.

## Office dashboard

- `dashboard/corporate_office.html` is the copy of the Corporate Office kept in GitHub. The live office and the crew app
  run on the owner's Mac (`~/Documents/Corporate Office/corporate-office/`: `index.html`, `crew/*.html`); keep both in the
  same design.
- Drafts only: nothing is sent without the owner's «да, отправляй».
- After changing the client sheet: `python3 scripts/import_contacts.py --embed dashboard/corporate_office.html`,
  then `python3 -m unittest discover -s tests`.
