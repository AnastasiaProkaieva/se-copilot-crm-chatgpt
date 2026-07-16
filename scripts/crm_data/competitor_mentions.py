"""Generates competitor-mention records linked to Opportunities."""

import random

COMPETITOR_NAMES = ["Databricks", "Snowflake", "Confluent"]
THREAT_LEVELS = ["Low", "Medium", "High"]

CONTEXT_TEMPLATES = {
    "Databricks": "Customer's data science team already has {competitor} notebooks in production; migration friction is the main objection.",
    "Snowflake": "Customer standardized on {competitor} for warehousing and is comparing total cost of ownership.",
    "Confluent": "Customer runs {competitor} for streaming and wants to know how PipelineOps interoperates with existing Kafka topics.",
}


def generate_competitor_mentions(
    rng: random.Random, opportunities: list[dict], count: int = 150
) -> list[dict]:
    opportunity_ids = [o["opportunity_id"] for o in opportunities]

    mentions = []
    for i in range(1, count + 1):
        competitor = rng.choice(COMPETITOR_NAMES)
        mentions.append(
            {
                "mention_id": f"CMP-{i:04d}",
                "opportunity_id": rng.choice(opportunity_ids),
                "competitor_name": competitor,
                "context": CONTEXT_TEMPLATES[competitor].format(competitor=competitor),
                "threat_level": rng.choice(THREAT_LEVELS),
            }
        )
    return mentions
