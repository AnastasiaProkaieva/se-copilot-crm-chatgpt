import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crm_data.accounts import generate_accounts
from crm_data.opportunities import generate_opportunities
from crm_data.pocs import (
    generate_pocs,
    STATUSES,
    ENVIRONMENT_TYPES,
    SUCCESS_CRITERIA_TEMPLATES,
)


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


def test_poc_success_criteria_fits_the_deals_product_line():
    rng = random.Random(42)
    accounts = generate_accounts(rng, count=200)
    opps = generate_opportunities(rng, accounts, count=350)
    opp_product = {o["opportunity_id"]: o["product_line"] for o in opps}
    pocs = generate_pocs(rng, opps, count=120)

    def criteria_matches(product_line, criteria):
        templates = SUCCESS_CRITERIA_TEMPLATES[product_line]
        prefixes = [t.split("{n}")[0] for t in templates]
        return any(criteria.startswith(p) for p in prefixes)

    for p in pocs:
        product_line = opp_product[p["opportunity_id"]]
        assert criteria_matches(product_line, p["success_criteria"]), (
            f"{p['poc_id']} criteria {p['success_criteria']!r} "
            f"does not fit product line {product_line}"
        )
