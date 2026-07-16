import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.rfp_responses import generate_rfp_responses, CATEGORIES


def test_rfp_response_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    responses = generate_rfp_responses(rng, opps, count=70)
    assert len(responses) == 70
    assert responses[0]["rfp_response_id"] == "RFP-0001"
    assert responses[-1]["rfp_response_id"] == "RFP-0070"


def test_rfp_response_opportunity_ids_are_valid_or_blank():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    responses = generate_rfp_responses(rng, opps, count=70)
    valid_ids = {o["opportunity_id"] for o in opps}
    for r in responses:
        assert r["opportunity_id"] == "" or r["opportunity_id"] in valid_ids


def test_rfp_response_has_some_master_answers():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    responses = generate_rfp_responses(rng, opps, count=70)
    master_answers = [r for r in responses if r["opportunity_id"] == ""]
    assert len(master_answers) > 0


def test_rfp_response_category_and_text_fields():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    responses = generate_rfp_responses(rng, opps, count=70)
    for r in responses:
        assert r["category"] in CATEGORIES
        assert r["question"]
        assert r["answer_text"]
