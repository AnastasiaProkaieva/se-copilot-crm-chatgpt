import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.competitor_mentions import (
    generate_competitor_mentions,
    COMPETITOR_NAMES,
    THREAT_LEVELS,
)


def test_mention_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    mentions = generate_competitor_mentions(rng, opps, count=150)
    assert len(mentions) == 150
    assert mentions[0]["mention_id"] == "CMP-0001"
    assert mentions[-1]["mention_id"] == "CMP-0150"


def test_mention_opportunity_ids_reference_existing_opportunities():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    mentions = generate_competitor_mentions(rng, opps, count=150)
    valid_ids = {o["opportunity_id"] for o in opps}
    for m in mentions:
        assert m["opportunity_id"] in valid_ids


def test_mention_competitor_and_threat_values():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    mentions = generate_competitor_mentions(rng, opps, count=150)
    for m in mentions:
        assert m["competitor_name"] in COMPETITOR_NAMES
        assert m["threat_level"] in THREAT_LEVELS
        assert m["context"]
