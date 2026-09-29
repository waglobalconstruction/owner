"""Client contact base for the Sales department (and other agents).

Read-only access to data/contacts/clients.json plus one way to turn a contact into an email:
a *draft* that cites the sheet row it came from and waits for the owner. There is no send
function here on purpose — sending happens only in Corporate Office after an explicit
«да, отправляй» from the owner (draft → edits → yes, send).
"""
import json
from datetime import datetime
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / 'data/contacts'


def _load(name):
    return json.loads((DATA / name).read_text(encoding='utf-8'))


def clients():
    return _load('clients.json')['clients']


def vendors():
    """Suppliers. Never used for sales emails or newsletters."""
    return _load('vendors.json')['vendors']


def find(query='', management_group=None, include_needs_review=True):
    q = query.lower().strip()
    out = []
    for c in clients():
        if management_group and c['management_group'] != management_group:
            continue
        if not include_needs_review and c['status'] == 'needs_review':
            continue
        hay = ' '.join([c['management_group'], c['property'], c['contact_name'], c['title'], c['email'], c['address']]).lower()
        if q in hay:
            out.append(c)
    return out


def by_email(email):
    e = (email or '').strip().lower()
    return next((c for c in clients() if c['email'].lower() == e), None)


class NotAllowed(Exception):
    pass


def prepare_draft(contact_id, subject, body, dept='sales'):
    """Build an email draft for the owner's review. Nothing is sent.

    Refuses vendors and contacts that still need review — those must be verified first.
    """
    if any(v['id'] == contact_id for v in vendors()):
        raise NotAllowed('Поставщики не участвуют в продажах и рассылках.')
    c = next((x for x in clients() if x['id'] == contact_id), None)
    if c is None:
        raise KeyError(contact_id)
    if c['status'] == 'needs_review':
        raise NotAllowed('Контакт требует проверки: ' + '; '.join(f['reason_ru'] for f in c['review_flags']))
    if not c['email']:
        raise NotAllowed('У контакта нет email.')
    name = c['contact_name'] if not c['contact_name'].startswith('(') else c['property']
    return {
        'dept': dept,
        'kind': 'Письмо',
        'status': 'draft',                    # becomes "sent" only through the owner's «да, отправляй»
        'requires_owner_approval': True,
        'to': f'{name} <{c["email"]}>',
        't1': subject,
        't2': f'{c["management_group"]} · {c["property"]}',
        'sources': [{
            'type': 'Google Sheets',
            'title': f'База клиентов — строка {c["source"]["row"]}: {c["contact_name"]} · {c["property"]}',
            'meta': f'{c["management_group"]} · {c["title"]}',
            'url': c['source']['url'],
        }],
        'versions': [{'text': f'To: {c["email"]}\nSubject: {subject}\n\n{body}', 'note': 'первый черновик',
                      'at': datetime.now().strftime('%H:%M')}],
    }
