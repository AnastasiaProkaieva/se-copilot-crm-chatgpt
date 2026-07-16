import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts


def test_account_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    assert len(accounts) == 200
    assert accounts[0]["account_id"] == "ACC-0001"
    assert accounts[-1]["account_id"] == "ACC-0200"


def test_account_ids_are_unique():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    ids = [a["account_id"] for a in accounts]
    assert len(ids) == len(set(ids))


def test_account_fields_present():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=5)
    for a in accounts:
        assert a["name"]
        assert a["industry"]
        assert isinstance(a["employee_count"], int) and a["employee_count"] > 0
        assert a["region"]
        assert isinstance(a["tech_stack_tags"], str)
