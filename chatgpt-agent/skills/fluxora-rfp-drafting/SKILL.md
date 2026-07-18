---
name: fluxora-rfp-drafting
description: Drafts Fluxora RFP, security, compliance, architecture, governance, and pricing-questionnaire responses from approved internal knowledge and Salesforce RFP_Response__c records. Use for pasted questions, uploaded questionnaires, answer reuse, gap analysis, and SME review routing.
compatibility: Uses approved Fluxora knowledge files. Salesforce CRM is required when retrieving reusable or opportunity-specific RFP_Response__c records.
metadata:
  owner: Fluxora Sales Engineering
  version: "0.1.0"
---

# Fluxora RFP Drafting

## Inputs

Accept pasted questions, an uploaded questionnaire, or a request to find an approved answer.

## Required workflow

1. Extract and number individual questions without changing their meaning.
2. Classify each question:
   - Security
   - Compliance
   - Data Governance
   - Architecture
   - Pricing and Licensing
3. Search approved knowledge files and **Salesforce CRM** RFP_Response__c records.
4. Apply the [source-precedence rules](references/source-precedence.md).
5. Draft answers only from supported claims.
6. Flag conflicts, stale content, and unsupported questions.
7. Produce the [required output](references/output-template.md).

## Guardrails

Never invent or extrapolate:

- Certifications or audit status
- Encryption algorithms or key-management behavior
- Data residency or subprocessors
- Deployment support
- SLAs, uptime, RTO, or RPO
- Roadmap commitments
- Contract, licensing, or pricing terms

Do not treat prior deal-specific language as globally approved policy.

## Final checks

- Every substantive claim has a source.
- Current approved documents override older CRM answers.
- Customer-specific language is separated from reusable baseline language.
- Unsupported answers are marked `SME review required` rather than guessed.
- The answer is written in Fluxora's approved voice without adding marketing superlatives not present in sources.
