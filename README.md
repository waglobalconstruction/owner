# Global Construction — Corporate Office

Data and agent helpers for the Corporate Office dashboard.

## Client contact base

Source: Google Sheet «Client Database — Business Card Contacts (Global Construction)»
(`17F2O0fcfELgxKHQfZRLxuIK60jMmq-Ay6MNqneR2dP0`).

| File | What it is |
|---|---|
| `data/source/client_database_business_cards.csv` | Raw CSV export of the sheet (rows match sheet rows) |
| `data/contacts/clients.json` | 78 client contacts: management group → property → contact, each with its sheet row and link |
| `data/contacts/vendors.json` | 3 material suppliers (Sherwin-Williams, HD Supply, The Home Depot) — kept apart, never used for sales or newsletters |
| `scripts/import_contacts.py` | Rebuilds the JSON from the CSV and refreshes the snapshot inside the dashboard |
| `agents/sales_contacts.py` | Read access for agents and `prepare_draft()` — builds a draft that cites the sheet row; there is no send |
| `dashboard/corporate_office.html` | The Corporate Office page with the base embedded (Sales card, «База клиентов» in the Sales panel, suppliers in «Проекты и бригады») |

### Rules the agents follow

- Drafts only: draft → edits → real sending only after an explicit «да, отправляй» from the owner.
- Every draft built from the base links to the sheet row the contact came from.
- Contacts with `status: needs_review` are not used as recipients until verified; the dashboard blocks
  «Да, отправляй» for them and for suppliers.

Held for review (6):

| Row | Property | Contact | Why |
|---|---|---|---|
| 66 | Garden Pointe Apartments (Allied) | Shelby McPhearson | Handwritten «Kerri Garrison» on the card — confirm the current contact |
| 77 | The Windsor Apartments (Avenue5) | Dorota | Printed name crossed out; her real email differs from the printed one — verify before use |
| 22 | Crestview West Apartments | Arnie | First name only |
| 23 | Benson Village Apartments | Tammy | First name only |
| 32 | Auburn Square Apartments | Jennifer | First name only |
| 74 | Yarrow Wood Highlands | Matt | First name only |

### Updating after the sheet changes

1. Export the sheet as CSV into `data/source/client_database_business_cards.csv`.
2. `python3 scripts/import_contacts.py --embed dashboard/corporate_office.html`
3. `python3 -m unittest discover -s tests`

Once a flagged contact is verified, fix the row in the sheet and remove its entry from `MANUAL_REVIEW`
in `scripts/import_contacts.py` (first-name-only rows clear themselves when the note on the card row changes).
