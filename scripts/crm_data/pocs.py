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

SUCCESS_CRITERIA_TEMPLATES = [
    "Ingest {n}TB of historical data within SLA",
    "Achieve sub-{n}s query latency on the benchmark dashboard",
    "Migrate {n} existing pipelines with zero data loss",
    "Deploy {n} ML models to production via ModelServe",
    "Demonstrate role-based access control across {n} business units",
]


def generate_pocs(
    rng: random.Random, opportunities: list[dict], count: int = 120
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    opportunity_ids = [o["opportunity_id"] for o in opportunities]

    pocs = []
    for i in range(1, count + 1):
        start_date = fake.date_between(start_date="-4M", end_date="today")
        duration_days = rng.randint(14, 45)
        end_date = start_date + timedelta(days=duration_days)
        template = rng.choice(SUCCESS_CRITERIA_TEMPLATES)
        n = rng.choice([1, 2, 3, 5, 10])

        pocs.append(
            {
                "poc_id": f"POC-{i:04d}",
                "opportunity_id": rng.choice(opportunity_ids),
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "success_criteria": template.format(n=n),
                "status": rng.choice(STATUSES),
                "environment_type": rng.choice(ENVIRONMENT_TYPES),
            }
        )
    return pocs
