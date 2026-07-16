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
    mentions = []
    for i in range(1, count + 1):
        opp = rng.choice(opportunities)
        # Keep the mention coherent with the deal: if the opportunity names a
        # primary competitor, the mention is about that same competitor;
        # otherwise pick any competitor.
        competitor = opp.get("primary_competitor") or rng.choice(COMPETITOR_NAMES)
        mentions.append(
            {
                "mention_id": f"CMP-{i:04d}",
                "opportunity_id": opp["opportunity_id"],
                "competitor_name": competitor,
                "context": CONTEXT_TEMPLATES[competitor].format(competitor=competitor),
                "threat_level": rng.choice(THREAT_LEVELS),
            }
        )
    return mentions
