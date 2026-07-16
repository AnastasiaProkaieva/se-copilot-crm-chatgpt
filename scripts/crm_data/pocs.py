"""Generates POC (proof-of-concept) tracking records linked to Opportunities."""

import random
from datetime import timedelta

from faker import Faker

STATUSES = [
    "Not Started",
    "In Progress",
    "At Risk",
    "Completed - Success",
    "Completed - Failed",
]

ENVIRONMENT_TYPES = ["Customer Cloud", "Fluxora Sandbox", "Hybrid"]

# Success-criteria templates keyed by product line, so a POC's stated goal
# fits the product the deal is actually about. Each template takes an {n}.
SUCCESS_CRITERIA_TEMPLATES = {
    "Lakehouse Core": [
        "Ingest {n}TB of historical data within SLA",
        "Achieve sub-{n}s query latency on the benchmark dashboard",
    ],
    "PipelineOps": [
        "Migrate {n} existing pipelines with zero data loss",
        "Run {n} scheduled pipelines with automated failure recovery",
    ],
    "ModelServe": [
        "Deploy {n} ML models to production via ModelServe",
        "Serve {n}k inference requests/sec under the latency SLA",
    ],
    "Governance Suite": [
        "Demonstrate role-based access control across {n} business units",
        "Apply column-level masking policies to {n} sensitive datasets",
    ],
}

# Fallback for any opportunity missing a product line.
_ANY_TEMPLATES = [t for ts in SUCCESS_CRITERIA_TEMPLATES.values() for t in ts]


def generate_pocs(
    rng: random.Random, opportunities: list[dict], count: int = 120
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    pocs = []
    for i in range(1, count + 1):
        opp = rng.choice(opportunities)
        start_date = fake.date_between(start_date="-4M", end_date="today")
        duration_days = rng.randint(14, 45)
        end_date = start_date + timedelta(days=duration_days)
        templates = SUCCESS_CRITERIA_TEMPLATES.get(
            opp.get("product_line"), _ANY_TEMPLATES
        )
        template = rng.choice(templates)
        n = rng.choice([1, 2, 3, 5, 10])

        pocs.append(
            {
                "poc_id": f"POC-{i:04d}",
                "opportunity_id": opp["opportunity_id"],
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "success_criteria": template.format(n=n),
                "status": rng.choice(STATUSES),
                "environment_type": rng.choice(ENVIRONMENT_TYPES),
            }
        )
    return pocs
