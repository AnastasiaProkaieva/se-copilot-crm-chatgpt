"""Generates Fluxora's target Account records (companies being sold to)."""

import random

from faker import Faker

INDUSTRIES = [
    "Financial Services",
    "Healthcare",
    "Retail & E-commerce",
    "Media & Entertainment",
    "Manufacturing",
    "Logistics",
    "Insurance",
    "Telecommunications",
    "Gaming",
    "Ad Tech",
]

REGIONS = ["AMER", "EMEA", "APAC", "LATAM"]

TECH_STACK_TAGS = [
    "AWS",
    "GCP",
    "Azure",
    "Kubernetes",
    "Snowflake",
    "Kafka",
    "Spark",
    "Airflow",
    "dbt",
    "Postgres",
]


def generate_accounts(rng: random.Random, count: int = 200) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    accounts = []
    for i in range(1, count + 1):
        tags = rng.sample(TECH_STACK_TAGS, k=rng.randint(2, 4))
        accounts.append(
            {
                "account_id": f"ACC-{i:04d}",
                "name": fake.company(),
                "industry": rng.choice(INDUSTRIES),
                "employee_count": rng.randint(200, 20000),
                "region": rng.choice(REGIONS),
                "tech_stack_tags": ", ".join(tags),
            }
        )
    return accounts
