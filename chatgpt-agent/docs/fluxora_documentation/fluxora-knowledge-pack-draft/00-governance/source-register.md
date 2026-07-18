---
title: "Fluxora Knowledge Source Register"
document_id: "GOV-004"
content_type: "source_register"
product_line: "Portfolio"
owner: "Knowledge Operations"
approval_status: "Draft — requires designated owner approval"
effective_date: "2026-07-16"
review_date: "TBD"
confidentiality: "Internal"
supersedes: "None"
source_basis:
  - "Fluxora SE Copilot Demo — Design Spec"
  - "Fluxora SE Copilot Demo Implementation Plan"
---

# Current sources

| Source | Type | Available | Approval status | Use |
|---|---|---:|---|---|
| Fluxora SE Copilot Demo — Design Spec | Design | Yes | Approved for demo design | Company context, product taxonomy, Agent architecture, demo scenario |
| Fluxora SE Copilot Demo Implementation Plan | Implementation plan | Yes | Planning source | Synthetic CRM vocabulary and five reusable RFP answer templates |
| Lakehouse Core FAQ | FAQ | No | Unknown | Required to finalize product one-pager |
| Lakehouse Core PRD | PRD | No | Unknown | Required to validate architecture and limits |
| Lakehouse Core roadmap | Roadmap | No | Unknown | Internal only; do not treat as GA |
| ModelServe FAQ / PRD / roadmap | Product sources | No | Unknown | Required |
| PipelineOps FAQ / PRD / roadmap | Product sources | No | Unknown | Required |
| Governance Suite FAQ / PRD / roadmap | Product sources | No | Unknown | Required |
| StreamSync FAQ / PRD / roadmap | Product sources | No | Unknown | Required; product taxonomy unresolved |

# Source-backed demo claims

| Claim ID | Claim | Source category | Scope |
|---|---|---|---|
| DEMO-001 | Fluxora spans lakehouse storage, pipeline orchestration, and ML model serving | Design spec | Company portfolio |
| DEMO-002 | CRM product lines are Lakehouse Core, PipelineOps, ModelServe, and Governance Suite | Design spec / implementation plan | CRM taxonomy |
| DEMO-003 | Data at rest uses AES-256 | RFP template in implementation plan | Security; approval still required |
| DEMO-004 | Data in transit uses TLS 1.2+ | RFP template in implementation plan | Security; approval still required |
| DEMO-005 | A current SOC 2 Type II report is available under NDA | RFP template in implementation plan | Compliance; approval still required |
| DEMO-006 | Governance Suite supports row- and column-level policies scoped by team, workspace, or business unit | RFP template in implementation plan | Governance Suite |
| DEMO-007 | Lakehouse Core supports customer-managed VPC deployment on AWS, GCP, and Azure | RFP template in implementation plan | Lakehouse Core |
| DEMO-008 | Demo pricing is primarily consumption-based, with optional Governance Suite seat add-ons | RFP template in implementation plan | Pricing; owner approval required |

# Missing source action

Upload or link the fifteen FAQ/PRD/roadmap documents, then complete the extraction template before changing any one-pager to Approved.
