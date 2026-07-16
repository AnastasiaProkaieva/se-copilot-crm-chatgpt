"""Generates Opportunity (deal) records linked to Accounts."""

import random

from faker import Faker

STAGES = [
    "Discovery",
    "Technical Validation",
    "POC",
    "Business Case",
    "Negotiation",
    "Closed Won",
    "Closed Lost",
]

PRODUCT_LINES = ["Lakehouse Core", "PipelineOps", "ModelServe", "Governance Suite"]

COMPETITORS = ["Databricks", "Snowflake", "Confluent", ""]

POD_NAMES = ["Enterprise", "Strategic", "Mid-Market"]


def generate_opportunities(
    rng: random.Random, accounts: list[dict], count: int = 350
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    account_ids = [a["account_id"] for a in accounts]

    opportunities = []
    for i in range(1, count + 1):
        stage = rng.choice(STAGES)
        amount = rng.randint(40_000, 1_200_000)
        close_date = fake.date_between(start_date="-6M", end_date="+6M")

        opportunities.append(
            {
                "opportunity_id": f"OPP-{i:04d}",
                "account_id": rng.choice(account_ids),
                "stage": stage,
                "amount": amount,
                "close_date": close_date.isoformat(),
                "pod": rng.choice(POD_NAMES),
                "product_line": rng.choice(PRODUCT_LINES),
                "primary_competitor": rng.choice(COMPETITORS),
            }
        )
    return opportunities
