---
title: "Fluxora RFP Response Guidelines"
document_id: "RFP-GDE-001"
content_type: "rfp_response_guidance"
product_line: "Portfolio"
owner: "RFP Program"
approval_status: "Draft — requires designated owner approval"
effective_date: "2026-07-16"
review_date: "TBD"
confidentiality: "Internal"
supersedes: "None"
source_basis:
  - "Fluxora SE Copilot Demo — Design Spec"
  - "Fluxora SE Copilot Demo Implementation Plan"
---

# Source order

1. Current approved Security/Compliance/Legal/Pricing source
2. Current approved product or architecture source
3. Approved master RFP answer
4. Current approved FAQ
5. Historical answer only as a lead

# Required output fields

| Field | Requirement |
|---|---|
| Question | Preserve the customer's meaning |
| Answer | Concise, direct, and source-backed |
| Source | File title and section |
| Confidence | High only when approved and in scope |
| Caveat | Product, deployment, region, version, or contract limitation |
| SME review | Required when unsupported, stale, conflicting, or customer-specific |

# Writing pattern

1. Answer the exact question in the first sentence.
2. Add one or two sentences of scope or implementation detail only when sourced.
3. Avoid marketing superlatives.
4. Avoid absolute terms such as always, never, fully compliant, guaranteed, or zero risk.
5. Do not expose internal roadmap or competitive content.
6. Use `Not verified — SME review required` rather than a plausible guess.

# Conflict rule

When CRM `RFP_Response__c` conflicts with the approved library, prefer the approved current source and flag the CRM response for correction. Do not silently reuse a stale deal-specific answer.
