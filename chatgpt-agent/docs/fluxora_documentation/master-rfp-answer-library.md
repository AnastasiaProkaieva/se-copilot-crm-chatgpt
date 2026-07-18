---
title: "Fluxora Master RFP Answer Library"
document_id: "RFP-MAS-001"
content_type: "master_rfp_answers"
product_line: "Portfolio"
owner: "RFP Program / Security"
approval_status: "Draft — requires designated owner approval"
effective_date: "2026-07-16"
review_date: "TBD"
confidentiality: "Customer shareable after approval"
supersedes: "None"
source_basis:
  - "Fluxora SE Copilot Demo — Design Spec"
  - "Fluxora SE Copilot Demo Implementation Plan"
---

# Usage rule

This library is a draft based on the demo implementation plan. It is not formally approved. Use a canonical answer only after its owner changes the approval status and confirms scope.

# Canonical answers from the demo source

## RFP-SEC-001 — Encryption at rest and in transit

**Category:** Security  
**Canonical question:** Does Fluxora encrypt data at rest and in transit?  
**Draft canonical answer:** Yes. Fluxora encrypts data at rest using AES-256 and data in transit using TLS 1.2 or later.  
**Scope/caveat:** Key ownership, key rotation, cipher suites, deployment exceptions, and internal service-to-service scope are not documented in the available source.  
**Owner:** Security Architecture  
**Approval status:** Draft  
**Allowed variants:** encryption, TLS, transport security, storage encryption

## RFP-COM-001 — SOC 2 Type II

**Category:** Compliance  
**Canonical question:** Does Fluxora maintain a SOC 2 Type II report?  
**Draft canonical answer:** Fluxora maintains a current SOC 2 Type II report, available under NDA upon request.  
**Scope/caveat:** Report period, system scope, bridge-letter availability, and request process must be confirmed.  
**Owner:** Compliance  
**Approval status:** Draft  
**Allowed variants:** SOC 2, independent audit, assurance report

## RFP-GOV-001 — Role-based access across business units

**Category:** Data Governance  
**Canonical question:** How does Fluxora support role-based access control across business units?  
**Draft canonical answer:** Governance Suite provides row- and column-level access policies that can be scoped by team, workspace, or business unit.  
**Scope/caveat:** Identity-provider integration, policy inheritance, masking, audit, and administrative roles are not documented.  
**Owner:** Governance Suite Product / Security  
**Approval status:** Draft  
**Allowed variants:** RBAC, fine-grained access, row-level security, column-level security

## RFP-ARC-001 — Customer-managed VPC

**Category:** Architecture  
**Canonical question:** Can Fluxora deploy in a customer's own cloud VPC?  
**Draft canonical answer:** Lakehouse Core supports customer-managed VPC deployment on AWS, GCP, and Azure.  
**Scope/caveat:** Regions, topology, networking features, operational ownership, and other product-line support are not documented.  
**Owner:** Product Architecture  
**Approval status:** Draft  
**Allowed variants:** customer cloud, private deployment, VPC, VNet

## RFP-PRI-001 — Pricing model

**Category:** Pricing and Licensing  
**Canonical question:** Is pricing based on compute usage or seat count?  
**Draft canonical answer:** The demo design describes Fluxora pricing as primarily consumption-based for compute and storage, with optional seat-based add-ons for Governance Suite.  
**Scope/caveat:** This is demo language, not a quote, SKU description, price, discount, or contractual term.  
**Owner:** Pricing / Finance / Legal  
**Approval status:** Draft  
**Allowed variants:** consumption, compute, storage, seats, licensing

# Answer rules

1. Preserve the canonical meaning; do not add unsupported details.
2. State relevant scope and caveats.
3. Never use a roadmap item to answer a current-capability question.
4. Never turn a security control into a certification or contractual guarantee.
5. If the question exceeds the canonical answer, route the gap to the owner.
6. Record customer-specific commitments separately and obtain approval.

# Standard unresolved-answer text

`Not verified — SME review required. The available approved sources do not establish this claim. Required owner: <team>.`
