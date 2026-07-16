import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.roster import generate_se_roster
from crm_data.opportunity_team_members import generate_opportunity_team_members


def test_team_member_count_and_id_format():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    roster = generate_se_roster(rng)
    members = generate_opportunity_team_members(rng, opps, roster, count=400)
    assert len(members) == 400
    assert members[0]["team_member_id"] == "OTM-0001"
    assert members[-1]["team_member_id"] == "OTM-0400"


def test_team_member_opportunity_ids_reference_existing_opportunities():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    roster = generate_se_roster(rng)
    members = generate_opportunity_team_members(rng, opps, roster, count=400)
    valid_ids = {o["opportunity_id"] for o in opps}
    for m in members:
        assert m["opportunity_id"] in valid_ids


def test_se_team_members_reference_existing_roster_ids():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    roster = generate_se_roster(rng)
    members = generate_opportunity_team_members(rng, opps, roster, count=400)
    valid_se_ids = {r["se_id"] for r in roster}
    for m in members:
        if m["member_type"] == "SE":
            assert m["member_name"] in valid_se_ids
