"""Generates buyer-side Contact records linked to Accounts."""

import random

from faker import Faker

ROLES = ["Economic Buyer", "Technical Evaluator", "Champion"]

TITLES = [
    "VP of Engineering",
    "Head of Data Engineering",
    "Chief Data Officer",
    "Director of Platform Engineering",
    "Senior Data Engineer",
    "Staff Software Engineer",
    "Director of Infrastructure",
    "VP of Data Science",
]


def generate_contacts(
    rng: random.Random, accounts: list[dict], count: int = 600
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    account_ids = [a["account_id"] for a in accounts]

    contacts = []
    for i in range(1, count + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()
        contacts.append(
            {
                "contact_id": f"CON-{i:04d}",
                "account_id": rng.choice(account_ids),
                "first_name": first_name,
                "last_name": last_name,
                "title": rng.choice(TITLES),
                "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
                "role": rng.choice(ROLES),
            }
        )
    return contacts
