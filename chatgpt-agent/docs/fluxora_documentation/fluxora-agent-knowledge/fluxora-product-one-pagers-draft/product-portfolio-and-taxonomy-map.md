---
title: "Fluxora Product Portfolio and Taxonomy Map"
document_id: "PROD-PORT-001"
content_type: "product_portfolio"
product_line: "Portfolio"
owner: "Product Operations"
approval_status: "Draft — requires designated owner approval"
effective_date: "2026-07-16"
review_date: "TBD"
confidentiality: "Internal"
supersedes: "None"
source_basis:
  - "Fluxora SE Copilot Demo — Design Spec"
  - "Fluxora SE Copilot Demo Implementation Plan"
---

# Current taxonomy

| Product | Current category | In CRM product-line vocabulary | Source status | Action |
|---|---|---:|---|---|
| Lakehouse Core | Lakehouse storage / data platform | Yes | Partial demo claims | Extract FAQ/PRD/roadmap and approve one-pager |
| PipelineOps | Pipeline orchestration | Yes | Partial demo claims | Extract FAQ/PRD/roadmap and approve one-pager |
| ModelServe | ML model serving | Yes | Partial demo claims | Extract FAQ/PRD/roadmap and approve one-pager |
| Governance Suite | Data access governance | Yes | Partial demo claims | Extract FAQ/PRD/roadmap and approve one-pager |
| StreamSync | Unresolved | No | No product claims available | Decide standalone/module/codename and update CRM if sellable |

# Required taxonomy decisions

1. Confirm the official display name, short name, and capitalization for each product.
2. Define whether each item is a product, module, add-on, capability, or internal codename.
3. Define product-to-product dependencies and packaging.
4. Define CRM picklist values and historical aliases.
5. Define which products may appear in customer-ready RFP and competitive material.
6. Define the owner and review cadence for every product entry.

# Agent routing implication

The Agent should not map a user request for StreamSync to PipelineOps or another product by inference. It should ask for the intended product relationship until the taxonomy is approved.
