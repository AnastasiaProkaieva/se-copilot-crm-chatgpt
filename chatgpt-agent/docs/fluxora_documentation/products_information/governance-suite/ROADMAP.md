# Governance Suite — Roadmap

Governance Suite reached GA in 2024 and is now in a phase of incremental hardening, scale, and depth rather than net-new category expansion. This roadmap focuses on sustaining unified policy enforcement and lineage capture as GA customers grow into the largest, most regulated deployments — while closing the specific gaps flagged as open risks: policy sprawl under delegated administration, lineage completeness through custom code, audit retention economics, and cross-region governance for global accounts.

## Recently Shipped (Q1–Q2 2026)
Extending consistent enforcement and self-service compliance reporting across all three product surfaces.
- Dynamic column-level masking extended to model-serving inference requests touching feature data, closing the last enforcement gap across lakehouse/orchestration/serving (Shipped)
- SCIM group-based policy assignment reached general availability, eliminating per-user policy sprawl for IdP-synced groups (Shipped)
- Self-service GDPR data subject access request (DSAR) report template shipped for compliance teams (Shipped)
- Audit log export to customer-owned SIEM/storage targets shipped with configurable retention windows (Shipped)

## Q3 2026
Theme: Scaling the policy engine and lineage graph for the largest GA accounts.
- Policy engine horizontal scaling work to sustain thousands of concurrent policy evaluations per second at largest-customer data volumes (In Progress)
- Lineage graph query performance optimization validated against hundreds-of-millions-of-edges environments (In Progress)
- Confidence-indicator tagging for automated lineage traversal through custom Python/SQL UDFs, mitigating the recurring "incomplete lineage" POC objection (Planned)
- Business-unit-scoped policy guardrail templates for delegated governance admins (Planned)

## Q4 2026
Theme: Making delegated administration safe at scale.
- Policy-conflict detection across delegated admin domains to catch inconsistent or contradictory business-unit policies before enforcement (Planned)
- Dual-control approval workflow for changes to governance policy itself, extending tamper-evident audit coverage to administrative actions (Planned)
- Rule-based classification tagging that auto-applies as schemas evolve, reducing manual re-tagging on new tables/columns (Planned)
- HIPAA access accounting report template enhancements for expanded self-service compliance coverage (In Progress)

## Q1 2027
Theme: Audit log economics and enforcement performance at extreme scale.
- Customer-configurable tiered/archival storage for long-retention audit logs, addressing multi-year regulated-customer retention cost (Planned)
- Cryptographic verifiability (write-once, tamper-evident) extended to archival-tier audit storage (Planned)
- Row/column-level policy enforcement latency tuning for pipeline job inputs/outputs to hold low-single-digit-percent overhead as lineage graph size grows (Planned)
- SOC 2 access review report generation refinements aimed at full self-service, engineering-free completion (Planned)

## Q2 2027
Theme: Governance that spans regions for global, multi-region customers.
- Cross-region policy scoping for customers whose data access patterns span multiple data-residency boundaries (Planned)
- Data residency-aware audit log routing enhancements for global deployments, in coordination with Solutions Architecture scoping (Planned)
- Policy engine failover hardening to reinforce fail-closed behavior with no single point of failure at global scale (Planned)
- Additional industry-specific compliance report templates beyond SOC 2/HIPAA/GDPR baseline (Planned)
