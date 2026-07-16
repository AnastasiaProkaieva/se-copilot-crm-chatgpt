"""Generates Fluxora's fixed 42-person Sales Engineering roster."""

import random

from faker import Faker

ROSTER_SIZE = 42
POD_NAMES = ["Enterprise", "Strategic", "Mid-Market"]


def generate_se_roster(rng: random.Random) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    roster = []

    director_id = "SE-001"
    roster.append(
        {
            "se_id": director_id,
            "name": fake.name(),
            "pod": rng.choice(POD_NAMES),
            "role": "Director",
            "manager_id": None,
        }
    )

    manager_ids = []
    for i in range(2, 4):
        se_id = f"SE-{i:03d}"
        manager_ids.append(se_id)
        roster.append(
            {
                "se_id": se_id,
                "name": fake.name(),
                "pod": POD_NAMES[(i - 2) % len(POD_NAMES)],
                "role": "SE Manager",
                "manager_id": director_id,
            }
        )

    for i in range(4, ROSTER_SIZE + 1):
        se_id = f"SE-{i:03d}"
        pod = rng.choice(POD_NAMES)
        pod_managers = [
            m
            for m in roster
            if m["role"] == "SE Manager" and m["pod"] == pod
        ]
        manager_id = (
            rng.choice(pod_managers)["se_id"]
            if pod_managers
            else rng.choice(manager_ids)
        )
        roster.append(
            {
                "se_id": se_id,
                "name": fake.name(),
                "pod": pod,
                "role": "SE",
                "manager_id": manager_id,
            }
        )

    return roster
