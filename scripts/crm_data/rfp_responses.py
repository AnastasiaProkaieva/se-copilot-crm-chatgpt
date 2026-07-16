"""Generates RFP/security-questionnaire response records.

Roughly 30% of rows are reusable "master answers" not tied to any single
Opportunity (opportunity_id == ""); the rest are deal-specific responses.
"""

import random

CATEGORIES = [
    "Security",
    "Compliance",
    "Data Governance",
    "Architecture",
    "Pricing & Licensing",
]

QA_TEMPLATES = {
    "Security": (
        "Does Fluxora encrypt data at rest and in transit?",
        "Yes. All data at rest is encrypted with AES-256, and all data in transit uses TLS 1.2+.",
    ),
    "Compliance": (
        "Is Fluxora SOC 2 Type II certified?",
        "Yes, Fluxora maintains a current SOC 2 Type II report, available under NDA upon request.",
    ),
    "Data Governance": (
        "How does Fluxora support role-based access control across business units?",
        "Governance Suite provides row- and column-level access policies scoped by team, workspace, or business unit.",
    ),
    "Architecture": (
        "Can Fluxora deploy in a customer's own cloud VPC?",
        "Yes, Lakehouse Core supports customer-managed VPC deployment on AWS, GCP, and Azure.",
    ),
    "Pricing & Licensing": (
        "Is pricing based on compute usage or seat count?",
        "Fluxora pricing is primarily consumption-based (compute + storage), with optional seat-based add-ons for Governance Suite.",
    ),
}


def generate_rfp_responses(
    rng: random.Random, opportunities: list[dict], count: int = 70
) -> list[dict]:
    opportunity_ids = [o["opportunity_id"] for o in opportunities]

    responses = []
    for i in range(1, count + 1):
        category = rng.choice(CATEGORIES)
        question, answer = QA_TEMPLATES[category]
        is_master_answer = rng.random() < 0.3
        responses.append(
            {
                "rfp_response_id": f"RFP-{i:04d}",
                "opportunity_id": "" if is_master_answer else rng.choice(opportunity_ids),
                "question": question,
                "category": category,
                "answer_text": answer,
            }
        )
    return responses
