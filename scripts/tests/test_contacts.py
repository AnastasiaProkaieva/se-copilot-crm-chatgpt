import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.contacts import generate_contacts


def test_contact_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    contacts = generate_contacts(rng, accounts, count=600)
    assert len(contacts) == 600
    assert contacts[0]["contact_id"] == "CON-0001"
    assert contacts[-1]["contact_id"] == "CON-0600"


def test_contact_account_ids_reference_existing_accounts():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    contacts = generate_contacts(rng, accounts, count=600)
    valid_ids = {a["account_id"] for a in accounts}
    for c in contacts:
        assert c["account_id"] in valid_ids


def test_contact_role_values():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    contacts = generate_contacts(rng, accounts, count=600)
    for c in contacts:
        assert c["role"] in {"Economic Buyer", "Technical Evaluator", "Champion"}
