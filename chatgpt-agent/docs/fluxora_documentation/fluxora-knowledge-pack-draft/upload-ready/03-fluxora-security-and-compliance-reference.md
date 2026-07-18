---
title: "Fluxora Security and Compliance Reference"
document_id: "UPL-SEC-001"
content_type: "consolidated_security_reference"
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


---


# Control matrix

| ID | Domain | Question/control | Canonical answer | Verification status | Owner |
|---|---|---|---|---|---|
| SEC-001 | Encryption | Is data encrypted at rest? | Demo source states AES-256 at rest. Key scope and management are not documented. | Partial demo claim | Security Architecture |
| SEC-002 | Encryption | Is data encrypted in transit? | Demo source states TLS 1.2+ in transit. Cipher and certificate details are not documented. | Partial demo claim | Security Architecture |
| COM-001 | Assurance | Is a SOC 2 Type II report available? | Demo source states a current report is available under NDA. | Partial demo claim | Compliance |
| IAM-001 | Authorization | Is row-/column-level access available? | Demo source states Governance Suite supports row- and column-level policies by team, workspace, or business unit. | Partial demo claim | Governance Suite PM / Security |
| DEP-001 | Deployment | Can Lakehouse Core run in a customer-managed VPC? | Demo source states AWS, GCP, and Azure customer-managed VPC deployment. | Partial demo claim | Product Architecture |
| KEY-001 | Key management | Are customer-managed keys supported? | Not verified. | Gap | Security Architecture |
| IAM-002 | Authentication | Is SAML or OIDC SSO supported? | Not verified. | Gap | IAM owner |
| IAM-003 | Provisioning | Is SCIM supported? | Not verified. | Gap | IAM owner |
| IAM-004 | Authentication | Is MFA supported or enforced? | Not verified. | Gap | IAM owner |
| LOG-001 | Audit | What audit events are recorded and retained? | Not verified. | Gap | Product Security |
| DATA-001 | Residency | Which regions and residency controls are supported? | Not verified. | Gap | Product / Privacy |
| DATA-002 | Retention | How are retention and deletion handled? | Not verified. | Gap | Product / Privacy |
| BCDR-001 | Resilience | What are backup, RTO, and RPO commitments? | Not verified. | Gap | Reliability Engineering |
| BCDR-002 | Resilience | Is disaster recovery tested? | Not verified. | Gap | Reliability Engineering |
| AVAIL-001 | Availability | What SLA is offered? | Not verified. Do not infer an SLA. | Gap | Reliability / Legal |
| IR-001 | Incident response | What is the incident-notification process? | Not verified. | Gap | Security / Legal |
| VM-001 | Vulnerability management | What are scan and remediation practices? | Not verified. | Gap | Product Security |
| TEST-001 | Security testing | Are penetration-test reports available? | Not verified. | Gap | Product Security |
| SDLC-001 | Secure development | What secure-SDLC controls are used? | Not verified. | Gap | Engineering Security |
| PRIV-001 | Privacy | What privacy agreements and subprocessors apply? | Not verified. | Gap | Privacy / Legal |
| CERT-001 | Certifications | Is Fluxora ISO 27001 certified? | Not verified. | Gap | Compliance |
| REG-001 | Regulatory | Is Fluxora HIPAA compliant / is a BAA available? | Not verified. | Gap | Compliance / Legal |
| REG-002 | Regulatory | Is Fluxora PCI DSS compliant? | Not verified. | Gap | Compliance |
| GOV-001 | Governance | Are masking, classification, and lineage supported? | Not verified beyond row-/column-level policy claim. | Gap | Governance Suite PM |
| NET-001 | Networking | Are PrivateLink/private endpoints supported? | Not verified. | Gap | Product Architecture |

# Agent rule

A row marked `Gap` must return `Not verified — SME review required`, not a guessed answer. A `Partial demo claim` may be used only with its caveat until formally approved.
