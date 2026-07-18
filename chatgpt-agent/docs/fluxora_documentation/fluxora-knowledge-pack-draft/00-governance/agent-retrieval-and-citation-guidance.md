---
title: "Fluxora Agent Retrieval and Citation Guidance"
document_id: "GOV-003"
content_type: "agent_retrieval_policy"
product_line: "Portfolio"
owner: "Sales Engineering Operations"
approval_status: "Draft — requires designated owner approval"
effective_date: "2026-07-16"
review_date: "TBD"
confidentiality: "Internal"
supersedes: "None"
source_basis:
  - "Fluxora SE Copilot Demo — Design Spec"
  - "Fluxora SE Copilot Demo Implementation Plan"
---

# Retrieval sequence

1. Classify the request: product, architecture, security, compliance, pricing, RFP, competitor, or roadmap.
2. Search the matching approved knowledge file.
3. Check approval status, effective date, review date, confidentiality, and product scope.
4. Use Salesforce only for live deal facts; use knowledge files for product and policy facts.
5. Cite the knowledge file title and section for material claims.
6. When no approved answer exists, state `Not verified — SME review required` and name the owner.

# Output labels

Use these labels where ambiguity matters:

- **Knowledge-file fact**
- **CRM fact**
- **Public-source fact**
- **Hypothesis**
- **Competitive positioning**
- **Roadmap item**
- **Recommendation**

# Product-doc rules

- FAQ: usable only when current and approved.
- PRD: internal design source; extract released facts, but do not expose internal rationale or unreleased behavior.
- Roadmap: never treat as current capability or commitment.
- One-pager: preferred concise source after approval.

# Citation pattern

For internal answers, cite in this form:

`Source: <document title>, <section>, effective <date>`

For conflicting sources, cite both and stop before producing customer-ready text.
