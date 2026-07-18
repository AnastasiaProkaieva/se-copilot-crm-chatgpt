---
title: "Fluxora Security and Compliance Overview"
document_id: "SEC-OVR-001"
content_type: "security_compliance_overview"
product_line: "Portfolio"
owner: "Security and Compliance"
approval_status: "Draft — requires designated owner approval"
effective_date: "2026-07-16"
review_date: "TBD"
confidentiality: "NDA required"
supersedes: "None"
source_basis:
  - "Fluxora SE Copilot Demo — Design Spec"
  - "Fluxora SE Copilot Demo Implementation Plan"
---

# Status and scope

This is an approval-ready **demo baseline**, not a signed security statement, contract, or certification representation. Security, Compliance, Privacy, Legal, and Product Architecture must validate scope and wording.

# Source-backed demo claims

| Domain | Canonical demo claim | Scope/caveat | Status |
|---|---|---|---|
| Encryption at rest | Data at rest is encrypted with AES-256. | Algorithm is source-backed; key ownership, rotation, scope, and exceptions are not documented. | Draft for approval |
| Encryption in transit | Data in transit uses TLS 1.2 or later. | Cipher suites, certificate management, internal service traffic, and exceptions are not documented. | Draft for approval |
| Compliance | Fluxora maintains a current SOC 2 Type II report, available under NDA upon request. | Report period, scope, bridge letter, and request process are not documented. | Draft for approval |
| Access control | Governance Suite provides row- and column-level access policies scoped by team, workspace, or business unit. | Identity provider, administration, inheritance, masking, and audit behavior are not documented. | Draft for approval |
| Deployment | Lakehouse Core supports customer-managed VPC deployment on AWS, GCP, and Azure. | Exact topology, regions, shared responsibility, and private-networking options are not documented. | Draft for approval |

# Explicit non-claims

Until approved evidence exists, the Agent must not claim:

- ISO 27001 certification
- HIPAA compliance or a BAA
- PCI DSS compliance
- FedRAMP authorization
- GDPR compliance as an absolute statement
- A 99.999% or any other availability SLA
- Customer-managed encryption keys in every deployment
- Specific RTO or RPO
- Specific data residency or sovereign-cloud coverage
- SAML, OIDC, SCIM, MFA, or specific identity-provider integrations
- Penetration-test frequency or report availability
- Vulnerability remediation timelines
- Backup, deletion, retention, or incident-notification commitments
- Any certification, control, or contractual term inferred from SOC 2

# Sharing rules

- SOC 2 reports: share only through the approved NDA/request process.
- Security answers: use the master RFP library; do not improvise.
- Architecture diagrams: verify confidentiality and version.
- Customer-specific commitments: require Security/Legal approval and should be recorded in the contract or approved exception process.

# Required approvers

| Content | Owner |
|---|---|
| Encryption and key management | Security Architecture |
| Identity and access | Product Security / IAM owner |
| Compliance reports and certifications | Compliance |
| Privacy and data processing | Privacy / Legal |
| Availability, backup, DR, RTO/RPO | Reliability Engineering / Legal |
| Deployment models and networking | Product Architecture |
| Contractual commitments | Legal |
