---
title: "Fluxora Product Source Ingestion Prompt"
document_id: "SRC-PRM-001"
content_type: "source_ingestion_prompt"
product_line: "Portfolio"
owner: "Knowledge Operations"
approval_status: "Draft — requires designated owner approval"
effective_date: "2026-07-16"
review_date: "TBD"
confidentiality: "Internal"
supersedes: "None"
source_basis:
  - "Fluxora Knowledge Governance Policy"
---

# Prompt

Use this prompt after attaching the FAQ, PRD, and roadmap for one product:

```text
Create an approval-ready Fluxora product knowledge package for [PRODUCT].

Sources attached:
- FAQ: [FILE]
- PRD: [FILE]
- Roadmap: [FILE]

Requirements:

1. Extract only claims explicitly supported by the sources.
2. Cite the source file and section/page for every material claim.
3. Separate content into:
   - Current generally available capability
   - Preview capability
   - Limitation or exclusion
   - Architecture/deployment fact
   - Security/governance fact
   - Pricing/packaging fact
   - Roadmap item
4. Do not turn roadmap content into a current capability or commitment.
5. When sources disagree, show the conflict and do not resolve it by inference.
6. Flag confidential or customer-unsafe content.
7. Produce:
   - Source metadata and claim register
   - Product one-pager
   - FAQ answer set
   - POC success-criteria library
   - Known limitations
   - RFP-ready claims
   - Unanswered questions and required SMEs
8. Use “Not verified — SME review required” for unsupported claims.
9. Preserve Fluxora terminology and writing-guide rules.
10. Keep approval_status as Draft until the named owner signs off.
```

# Review prompt

```text
Compare the generated [PRODUCT] one-pager against all attached sources.
List every sentence that lacks a source, overstates a source, merges GA and roadmap content, omits a material limitation, or uses customer-unsafe language. Do not rewrite until the discrepancy table is complete.
```
