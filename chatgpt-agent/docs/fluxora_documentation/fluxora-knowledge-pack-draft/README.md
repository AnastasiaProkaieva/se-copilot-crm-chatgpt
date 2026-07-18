# Fluxora Knowledge Pack — Draft for Approval

**Status:** Draft, not approved for external/customer use  
**Generated:** 2026-07-16  
**Intended use:** Source-controlled knowledge files for the **Fluxora SE Copilot** Workspace Agent.

## What is in this pack

This package supplies the missing knowledge-library structure requested by the SE Copilot design:

- Five product one-pagers: Lakehouse Core, ModelServe, PipelineOps, Governance Suite, and a source-empty StreamSync shell
- Competitor battlecards: Databricks, Snowflake, and Confluent
- Security and compliance reference material
- A master RFP answer library and gap register
- Fluxora terminology and writing guidance
- Knowledge governance, roadmap handling, and source-extraction templates
- An `upload-ready/` folder containing consolidated versions suitable for attaching to an Agent after review

## Important source limitation

The product FAQ, PRD, and roadmap files were not available in the current conversation, ChatGPT file library, or the connected Drive search. Therefore:

1. Only claims explicitly present in the supplied Fluxora demo design are recorded as **source-backed demo claims**.
2. All other product capabilities, integrations, limits, pricing terms, certifications, service levels, roadmap items, and competitive differentiators are marked **Not verified** or **Source required**.
3. No file in this package is genuinely "approved" until the named Product, Security, Legal, Compliance, Pricing, or Competitive Intelligence owner signs it off.

## Known source-backed demo claims

- Fluxora is a fictional data/AI infrastructure platform spanning lakehouse storage, pipeline orchestration, and ML model serving.
- Established product-line vocabulary in the CRM design: **Lakehouse Core, PipelineOps, ModelServe, Governance Suite**.
- Data at rest: **AES-256**.
- Data in transit: **TLS 1.2+**.
- Fluxora maintains a current **SOC 2 Type II** report, available under NDA.
- Governance Suite provides row- and column-level access policies scoped by team, workspace, or business unit.
- Lakehouse Core supports customer-managed VPC deployment on AWS, GCP, and Azure.
- Fluxora pricing is described in the demo as primarily consumption-based for compute and storage, with optional seat-based Governance Suite add-ons.

These statements are preserved as demo-source claims. They still require business-owner approval before being presented as real-world contractual or compliance commitments.

## StreamSync decision required

`StreamSync` is not present in the current CRM product-line vocabulary. Before using it in the Agent, decide whether it is:

- a standalone sellable product,
- a PipelineOps module,
- a Lakehouse Core ingestion capability, or
- a roadmap/codename that should remain internal.

If it is sellable, add it to the Salesforce product-line picklist and update product routing in the Agent and skills.

## Recommended workflow

1. Add the 15 source documents—FAQ, PRD, and roadmap for each product—to a controlled source folder.
2. Complete `06-source-extraction/product-document-extraction-template.md` for each source.
3. Replace every `Not verified` entry with a source-cited statement or leave it explicitly unresolved.
4. Have Product approve one-pagers; Security/Compliance/Legal approve security and RFP content; Competitive Intelligence approve battlecards.
5. Upload only current, approved files from `upload-ready/` to the Agent.
6. Do not upload raw roadmaps to a broadly shared, customer-facing Agent unless access controls and roadmap rules are enforced.

## Folder map

| Folder | Purpose |
|---|---|
| `00-governance/` | Approval, source precedence, confidentiality, and retrieval rules |
| `01-product-one-pagers/` | Editable product-specific one-pagers |
| `02-competitor-battlecards/` | Internal competitive guidance |
| `03-security-compliance/` | Security claim register and control gaps |
| `04-rfp/` | Canonical answer library and unanswered-question routing |
| `05-language/` | Terminology, capitalization, voice, and writing rules |
| `06-source-extraction/` | Templates for converting FAQ/PRD/roadmap content into approved claims |
| `upload-ready/` | Consolidated Agent knowledge files; still draft until approved |
