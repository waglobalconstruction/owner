import csv
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'scripts'))

import import_contacts  # noqa: E402
from agents import sales_contacts  # noqa: E402


class ImportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = import_contacts.load_rows(import_contacts.SRC_CSV)
        cls.clients, cls.vendors = import_contacts.parse(cls.rows)

    def test_counts(self):
        self.assertEqual(len(self.clients), 78)
        self.assertEqual(len(self.vendors), 3)

    def test_vendors_kept_apart(self):
        self.assertEqual({v['company'] for v in self.vendors}, {'Sherwin-Williams', 'HD Supply', 'The Home Depot'})
        client_emails = {c['email'].lower() for c in self.clients}
        self.assertFalse(client_emails & {v['email'].lower() for v in self.vendors})
        self.assertTrue(all(not v['sales_outreach'] for v in self.vendors))

    def test_source_row_matches_sheet(self):
        for c in self.clients:
            row = self.rows[c['source']['row'] - 1]
            self.assertEqual(row[2].strip(), c['contact_name'])
            self.assertIn(f"range=A{c['source']['row']}:I{c['source']['row']}", c['source']['url'])

    def test_review_flags(self):
        flagged = {(c['property'], c['contact_name']): c['review_flags'][0]['code'] for c in self.clients if c['status'] == 'needs_review'}
        self.assertEqual(flagged, {
            ('Garden Pointe Apartments', 'Shelby McPhearson (she/her)'): 'contact_unclear',
            ('The Windsor Apartments', 'Dorota'): 'email_unverified',
            ('Crestview West Apartments', 'Arnie'): 'surname_missing',
            ('Benson Village Apartments', 'Tammy'): 'surname_missing',
            ('Auburn Square Apartments', 'Jennifer'): 'surname_missing',
            ('Yarrow Wood Highlands', 'Matt'): 'surname_missing',
        })

    def test_json_is_current(self):
        saved = json.loads((ROOT / 'data/contacts/clients.json').read_text(encoding='utf-8'))['clients']
        self.assertEqual(saved, self.clients, 'run scripts/import_contacts.py')


class SalesAccessTest(unittest.TestCase):
    def test_draft_cites_row_and_is_not_sent(self):
        c = sales_contacts.find('Heidi Witt')[0]
        d = sales_contacts.prepare_draft(c['id'], 'Hello', 'Body')
        self.assertEqual(d['status'], 'draft')
        self.assertTrue(d['requires_owner_approval'])
        self.assertEqual(d['to'], 'Heidi Witt <sequoias@alliedresidential.com>')
        self.assertEqual(d['sources'][0]['url'], c['source']['url'])
        self.assertFalse(hasattr(sales_contacts, 'send'))

    def test_needs_review_and_vendors_refused(self):
        dorota = sales_contacts.by_email('PM.TheWindsor@avenue5apt.com')
        with self.assertRaises(sales_contacts.NotAllowed):
            sales_contacts.prepare_draft(dorota['id'], 's', 'b')
        with self.assertRaises(sales_contacts.NotAllowed):
            sales_contacts.prepare_draft(sales_contacts.vendors()[0]['id'], 's', 'b')

    def test_find_by_group(self):
        self.assertEqual(len(sales_contacts.find(management_group='Weidner Apartment Homes')), 3)


if __name__ == '__main__':
    unittest.main()
