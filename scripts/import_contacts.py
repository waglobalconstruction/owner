#!/usr/bin/env python3
"""Import the business-card client database into Corporate Office.

Source: Google Sheet "Client Database — Business Card Contacts (Global Construction)",
exported as CSV to data/source/client_database_business_cards.csv.

Output:
  data/contacts/clients.json  — client contacts (management group → property → contact)
  data/contacts/vendors.json  — material suppliers, kept apart and never used for sales outreach

Every record keeps its sheet row number and a direct link to that row, so any draft an
agent prepares can cite exactly where the contact came from.

Usage:
  python3 scripts/import_contacts.py                 # rebuild the JSON files
  python3 scripts/import_contacts.py --embed dashboard/corporate_office.html
                                                     # also refresh the snapshot inside the dashboard page
"""
import argparse
import csv
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_CSV = ROOT / 'data/source/client_database_business_cards.csv'
OUT_DIR = ROOT / 'data/contacts'

SHEET_ID = '17F2O0fcfELgxKHQfZRLxuIK60jMmq-Ay6MNqneR2dP0'
SHEET_TITLE = 'Client Database — Business Card Contacts (Global Construction)'
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit'
VENDOR_MARKER = 'VENDORS / SUPPLIERS'

# Records the owner asked to hold for verification, keyed by (property, contact name as printed).
MANUAL_REVIEW = {
    ('Garden Pointe Apartments', 'Shelby McPhearson (she/her)'): {
        'code': 'contact_unclear',
        'reason_ru': 'На визитке напечатано Shelby McPhearson, от руки написано Kerri Garrison — уточнить, кто актуальный контакт.',
    },
    ('The Windsor Apartments', 'Dorota'): {
        'code': 'email_unverified',
        'reason_ru': 'Напечатанное имя (Christian Easley) зачёркнуто, от руки — «Dorota»; её настоящий email отличается от напечатанного '
                     '(без префикса «PM») — перепроверить email перед использованием.',
    },
}
FIRST_NAME_ONLY = re.compile(r'first name\b.*\bonly', re.I)


def row_url(row):
    return f'{SHEET_URL}#gid=0&range=A{row}:I{row}'


def clean(v):
    # The sheet stores a few quotes doubled (""Stacey""); keep the text, not the escaping.
    return re.sub(r'"{2,}', '"', (v or '').strip())


def source(row):
    return {'sheet_id': SHEET_ID, 'sheet_title': SHEET_TITLE, 'row': row, 'url': row_url(row)}


def review_flags(rec):
    flags = []
    manual = MANUAL_REVIEW.get((rec['property'], rec['contact_name']))
    if manual:
        flags.append(dict(manual))
    if FIRST_NAME_ONLY.search(rec['notes']) and not manual:
        flags.append({'code': 'surname_missing',
                      'reason_ru': f'На визитке только имя ({rec["contact_name"]}) — фамилия не указана, требует уточнения.'})
    return flags


def load_rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))


def parse(rows):
    header = [clean(c) for c in rows[0]]
    if header[:3] != ['Management Group', 'Community/Property', 'Contact Name']:
        raise SystemExit(f'Unexpected header: {header}')
    clients, vendors, in_vendors, vendor_cols = [], [], False, None
    for i, raw in enumerate(rows[1:], start=2):   # sheet rows are 1-based and row 1 is the header
        cells = [clean(c) for c in raw] + [''] * 9
        if not any(cells):
            continue
        if cells[0].startswith(VENDOR_MARKER):
            in_vendors = True
            continue
        if in_vendors:
            if cells[0] == 'Company':
                vendor_cols = cells
                continue
            vendors.append({
                'id': f'v{i:03d}', 'kind': 'vendor', 'company': cells[0], 'contact_name': cells[1], 'title': cells[2],
                'phone': cells[3], 'fax': cells[4], 'email': cells[5], 'address': cells[6], 'notes': cells[7],
                'sales_outreach': False, 'source': source(i),
            })
            continue
        rec = {
            'id': f'c{i:03d}', 'kind': 'client', 'management_group': cells[0], 'property': cells[1],
            'contact_name': cells[2], 'title': cells[3], 'phone': cells[4], 'fax': cells[5],
            'email': cells[6], 'address': cells[7], 'notes': cells[8],
        }
        rec['review_flags'] = review_flags(rec)
        rec['status'] = 'needs_review' if rec['review_flags'] else 'ok'
        rec['sales_outreach'] = True
        rec['source'] = source(i)
        clients.append(rec)
    if in_vendors and vendor_cols is None:
        raise SystemExit('Vendor block found without its header row')
    return clients, vendors


def build(clients, vendors):
    groups = {}
    for c in clients:
        groups.setdefault(c['management_group'], set()).add(c['property'])
    meta = {
        'source': {'sheet_id': SHEET_ID, 'sheet_title': SHEET_TITLE, 'url': SHEET_URL},
        'imported': date.today().isoformat(),
        'counts': {
            'clients': len(clients),
            'needs_review': sum(c['status'] == 'needs_review' for c in clients),
            'management_groups': len(groups),
            'properties': len({(c['management_group'], c['property']) for c in clients}),
            'vendors': len(vendors),
        },
        'rules': {
            'drafts_only': 'Агенты не отправляют письма сами: черновик → правки → только после явного «да, отправляй».',
            'cite_source': 'Каждый черновик ссылается на строку таблицы, из которой взят контакт (source.url).',
            'needs_review': 'Контакты со status=needs_review не используются как получатели, пока их не проверят.',
            'vendors': 'Поставщики (vendors.json) не участвуют в продажах и рассылках.',
        },
    }
    return meta


def embed(page, clients, vendors, meta):
    """Replace the CONTACTS snapshot between the markers in the dashboard page."""
    slim = lambda r, keys: {k: r[k] for k in keys if r.get(k)}
    ckeys = ['id', 'management_group', 'property', 'contact_name', 'title', 'phone', 'fax', 'email', 'address', 'notes', 'status']
    vkeys = ['id', 'company', 'contact_name', 'title', 'phone', 'fax', 'email', 'address', 'notes']
    data = {
        'sheet': SHEET_URL, 'title': SHEET_TITLE, 'imported': meta['imported'], 'counts': meta['counts'],
        'clients': [dict(slim(c, ckeys), row=c['source']['row'], flags=[f['reason_ru'] for f in c['review_flags']]) for c in clients],
        'vendors': [dict(slim(v, vkeys), row=v['source']['row']) for v in vendors],
    }
    blob = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    text = page.read_text(encoding='utf-8')
    new, n = re.subn(r'/\* CONTACTS:BEGIN \*/.*?/\* CONTACTS:END \*/',
                     lambda _: f'/* CONTACTS:BEGIN */{blob}/* CONTACTS:END */', text, flags=re.S)
    if n != 1:
        raise SystemExit(f'{page}: expected one CONTACTS:BEGIN/END block, found {n}')
    page.write_text(new, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--csv', type=Path, default=SRC_CSV)
    ap.add_argument('--embed', type=Path, help='dashboard HTML whose CONTACTS snapshot should be refreshed')
    args = ap.parse_args()

    clients, vendors = parse(load_rows(args.csv))
    meta = build(clients, vendors)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / 'clients.json').write_text(json.dumps({'meta': meta, 'clients': clients}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (OUT_DIR / 'vendors.json').write_text(json.dumps({'meta': {'source': meta['source'], 'imported': meta['imported'],
        'rule': meta['rules']['vendors']}, 'vendors': vendors}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if args.embed:
        embed(args.embed, clients, vendors, meta)

    c = meta['counts']
    print(f"Clients: {c['clients']} ({c['management_groups']} management groups, {c['properties']} properties), "
          f"needs review: {c['needs_review']}; vendors (kept apart): {c['vendors']}")
    for r in clients:
        if r['status'] == 'needs_review':
            print(f"  review · row {r['source']['row']:>2} · {r['property']} · {r['contact_name']}: {r['review_flags'][0]['code']}")


if __name__ == '__main__':
    main()
