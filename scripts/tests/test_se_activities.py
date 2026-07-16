import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.roster import generate_se_roster
from crm_data.se_activities import generate_se_activities, ACTIVITY_TYPES


def test_activity_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    roster = generate_se_roster(rng)
    activities = generate_se_activities(rng, opps, roster, count=900)
    assert len(activities) == 900
    assert activities[0]["activity_id"] == "ACT-0001"
    assert activities[-1]["activity_id"] == "ACT-0900"


def test_activity_foreign_keys_reference_existing_rows():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    roster = generate_se_roster(rng)
    activities = generate_se_activities(rng, opps, roster, count=900)
    valid_opp_ids = {o["opportunity_id"] for o in opps}
    valid_se_ids = {r["se_id"] for r in roster if r["role"] in ("SE", "SE Manager")}
    for a in activities:
        assert a["opportunity_id"] in valid_opp_ids
        assert a["se_id"] in valid_se_ids
        assert a["activity_type"] in ACTIVITY_TYPES
        assert a["notes"]
