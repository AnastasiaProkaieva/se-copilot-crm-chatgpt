import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities, STAGES, PRODUCT_LINES


def test_opportunity_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    assert len(opps) == 350
    assert opps[0]["opportunity_id"] == "OPP-0001"
    assert opps[-1]["opportunity_id"] == "OPP-0350"


def test_opportunity_account_ids_reference_existing_accounts():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    valid_ids = {a["account_id"] for a in accounts}
    for o in opps:
        assert o["account_id"] in valid_ids


def test_opportunity_stage_and_product_line_values():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    for o in opps:
        assert o["stage"] in STAGES
        assert o["product_line"] in PRODUCT_LINES
        assert isinstance(o["amount"], int) and o["amount"] > 0


def test_closed_lost_or_won_opportunities_have_past_or_future_dates_as_strings():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    for o in opps:
        # ISO format YYYY-MM-DD, 10 chars, two dashes
        assert len(o["close_date"]) == 10
        assert o["close_date"][4] == "-" and o["close_date"][7] == "-"
