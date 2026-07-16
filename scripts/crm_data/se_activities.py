"""Generates SE activity log records (calls, demos, RFP work, check-ins)."""

import random

from faker import Faker

ACTIVITY_TYPES = [
    "Discovery Call",
    "Technical Demo",
    "POC Check-in",
    "RFP Work",
    "Internal Sync",
]

NOTE_TEMPLATES = {
    "Discovery Call": "Discussed current {tag} stack and pain points around scaling data pipelines.",
    "Technical Demo": "Walked through {tag} integration and answered questions on governance controls.",
    "POC Check-in": "Reviewed POC progress against success criteria; {tag} environment stable.",
    "RFP Work": "Drafted responses covering {tag} security and compliance questions.",
    "Internal Sync": "Synced with AE on deal strategy and next steps involving {tag}.",
}

TAGS = ["Lakehouse Core", "PipelineOps", "ModelServe", "Governance Suite"]


def generate_se_activities(
    rng: random.Random,
    opportunities: list[dict],
    roster: list[dict],
    count: int = 900,
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    opportunity_ids = [o["opportunity_id"] for o in opportunities]
    se_ids = [r["se_id"] for r in roster if r["role"] in ("SE", "SE Manager")]

    activities = []
    for i in range(1, count + 1):
        activity_type = rng.choice(ACTIVITY_TYPES)
        tag = rng.choice(TAGS)
        activities.append(
            {
                "activity_id": f"ACT-{i:04d}",
                "opportunity_id": rng.choice(opportunity_ids),
                "se_id": rng.choice(se_ids),
                "activity_type": activity_type,
                "activity_date": fake.date_between(
                    start_date="-4M", end_date="today"
                ).isoformat(),
                "notes": NOTE_TEMPLATES[activity_type].format(tag=tag),
            }
        )
    return activities
