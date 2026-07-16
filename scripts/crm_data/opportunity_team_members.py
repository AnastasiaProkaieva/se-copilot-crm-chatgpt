"""Links AEs and SEs to Opportunities."""

import random

from faker import Faker

SE_ROLES = ["Primary SE", "Supporting SE"]
AE_ROLES = ["Deal Owner"]


def generate_opportunity_team_members(
    rng: random.Random,
    opportunities: list[dict],
    roster: list[dict],
    count: int = 400,
) -> list[dict]:
    fake = Faker()
    fake.seed_instance(rng.randint(0, 2**32 - 1))

    se_ids_by_pod: dict[str, list[str]] = {}
    for r in roster:
        if r["role"] == "SE":
            se_ids_by_pod.setdefault(r["pod"], []).append(r["se_id"])
    all_se_ids = [r["se_id"] for r in roster if r["role"] == "SE"]

    # Staff opportunities in order with a coherent (AE, SE) pair each, so a
    # given deal has exactly one Deal Owner and one SE. With count=400 this
    # fully staffs the first 200 opportunities — the pool the demo scenario
    # draws its hero deal from.
    members = []
    i = 0
    for opp in opportunities:
        if i >= count:
            break
        i += 1
        members.append(
            {
                "team_member_id": f"OTM-{i:04d}",
                "opportunity_id": opp["opportunity_id"],
                "member_type": "AE",
                "member_name": fake.name(),
                "role": rng.choice(AE_ROLES),
            }
        )
        if i >= count:
            break
        i += 1
        pod_ses = se_ids_by_pod.get(opp["pod"], all_se_ids)
        members.append(
            {
                "team_member_id": f"OTM-{i:04d}",
                "opportunity_id": opp["opportunity_id"],
                "member_type": "SE",
                "member_name": rng.choice(pod_ses),
                "role": rng.choice(SE_ROLES),
            }
        )
    return members
