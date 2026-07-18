---
name: fluxora-product-knowledge
description: Retrieves and explains approved Fluxora product, architecture, security, governance, RFP, and competitor knowledge without requiring a CRM record. Use for product questions, battlecard lookup, competitor comparison, technical positioning, reusable answer retrieval, and institutional-knowledge search.
compatibility: Requires approved Fluxora knowledge files. Salesforce CRM is optional and should be used only when the user asks for deal-specific context or RFP_Response__c records.
metadata:
  owner: Fluxora Sales Engineering
  version: "0.1.0"
---

# Fluxora Product and Competitive Knowledge

## Required workflow

1. Classify the request as product, architecture, security, compliance, governance, pricing, RFP, or competitor.
2. Search the most relevant approved knowledge files.
3. Apply [source and freshness rules](references/source-rules.md).
4. Answer using verified claims only.
5. Cite file name and section for material claims.
6. Separate:
   - Verified product fact
   - Competitive positioning guidance
   - Limitation or caveat
   - Recommended discovery question
7. If the user asks for deal-specific advice, retrieve CRM context through **Salesforce CRM** and label it separately.

## Guardrails

- Do not turn battlecard positioning into an unsupported factual claim about a competitor.
- Do not infer roadmap, pricing, certifications, or deployment support.
- Do not use old RFP answers when a newer approved source conflicts.
- Do not include confidential internal positioning in customer-ready copy unless the user explicitly asks for internal guidance.

## Final checks

- Every material claim has an approved source.
- Competitive facts and sales positioning are clearly separated.
- Stale or conflicting sources are called out.
- When no approved answer exists, name the required SME instead of guessing.
