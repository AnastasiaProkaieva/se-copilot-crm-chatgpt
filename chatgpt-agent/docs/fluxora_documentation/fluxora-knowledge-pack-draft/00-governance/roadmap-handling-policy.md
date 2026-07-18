---
title: "Fluxora Roadmap Handling Policy"
document_id: "GOV-002"
content_type: "roadmap_policy"
product_line: "Portfolio"
owner: "Product Operations"
approval_status: "Draft — requires designated owner approval"
effective_date: "2026-07-16"
review_date: "TBD"
confidentiality: "Confidential"
supersedes: "None"
source_basis:
  - "Fluxora SE Copilot Demo — Design Spec"
  - "Fluxora SE Copilot Demo Implementation Plan"
---

# Rule

A roadmap is a planning artifact, not a contractual commitment or proof of current functionality.

# Allowed status vocabulary

Use only an owner-approved lifecycle label:

- In discovery
- Planned
- Targeted
- Private preview
- Public preview
- Generally available
- Deferred
- Removed

# Customer-facing rules

- Do not say a roadmap item "will ship" unless a specifically authorized commitment exists.
- Do not provide dates, quarters, or release names unless Product and Legal approve the disclosure.
- Use conditional language: "planned," "targeted," or "under consideration."
- State that timing and scope may change.
- Never use a roadmap item to answer an RFP question about current functionality.
- Never use a roadmap item to satisfy a POC criterion unless the POC explicitly tests a preview with written approval.

# Agent retrieval rule

Roadmap files should carry `confidentiality: Confidential` and `approval_status: Draft` or `Reviewed` unless an owner has approved a customer-shareable excerpt. The Agent must prefer current GA product documentation over roadmap content.

# Recommended architecture

Keep raw roadmaps outside the broadly shared Agent knowledge set. Instead, create a short, separately permissioned roadmap brief containing only approved disclosure language.
