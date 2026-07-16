import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.pocs import generate_pocs, STATUSES, ENVIRONMENT_TYPES


def test_poc_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    pocs = generate_pocs(rng, opps, count=120)
    assert len(pocs) == 120
    assert pocs[0]["poc_id"] == "POC-0001"
    assert pocs[-1]["poc_id"] == "POC-0120"


def test_poc_opportunity_ids_reference_existing_opportunities():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    pocs = generate_pocs(rng, opps, count=120)
    valid_ids = {o["opportunity_id"] for o in opps}
    for p in pocs:
        assert p["opportunity_id"] in valid_ids


def test_poc_status_and_environment_values():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    pocs = generate_pocs(rng, opps, count=120)
    for p in pocs:
        assert p["status"] in STATUSES
        assert p["environment_type"] in ENVIRONMENT_TYPES
        assert p["success_criteria"]
