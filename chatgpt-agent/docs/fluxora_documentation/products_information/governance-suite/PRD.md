# Governance Suite — PRD

**Status:** Active (Post-GA) | **Stage:** GA (since 2024) | **Owner:** Product Manager, Governance Suite

## Problem Statement

As customers consolidate ingestion, transformation, and model-serving workloads onto Fluxora, governance has moved from a checkbox feature to a deal-blocking requirement. Enterprise data platform buyers — particularly regulated-industry customers evaluating a multi-quarter migration off legacy warehouses — will not commit to Fluxora as a system of record without demonstrable, fine-grained control over who can access what data, verifiable lineage from raw source to ML feature to served model, and audit trails that satisfy internal security review and external compliance obligations (SOC 2, HIPAA, GDPR, industry-specific frameworks).

Prior to Governance Suite, access control, lineage, and audit logging were fragmented across Fluxora's lakehouse, pipeline orchestration, and model serving products, each with its own permission model and inconsistent logging granularity. This created three concrete failures in the field: (1) security teams could not get a single answer to "who has access to this table and why," (2) data engineers could not trace a serving-time model input back to its source tables without manual cross-referencing, and (3) compliance teams could not produce audit evidence without stitching together logs from multiple subsystems. Governance Suite consolidates these into a single control plane so that governance is no longer the long pole in a Fluxora deal cycle or a recurring point of churn risk post-signature.

## Target Personas

- **Chief Data Officer** — owns organizational accountability for data risk, regulatory exposure, and cross-functional data policy; needs assurance that platform-wide governance posture is auditable and reportable to the board/regulators without custom tooling.
- **VP of Engineering** — evaluates Governance Suite as part of the broader platform commitment; cares about how governance overhead affects developer velocity, onboarding time for new teams, and the operational burden on the platform team that will own it long-term.
- **Head of Data Engineering** — the primary day-to-day owner of access policies, lineage accuracy, and audit readiness; needs governance controls that integrate with existing identity providers and don't require a parallel policy system to maintain.
- **Staff/Senior Data Engineer** (technical evaluator) — runs the POC; stress-tests policy enforcement correctness, lineage completeness across transformation logic, and whether governance controls introduce measurable query or pipeline latency.

## Goals

- Provide a single, consistent access-control model across lakehouse storage, pipeline orchestration, and model serving, enforced at query/execution time regardless of which Fluxora product initiates the request.
- Deliver automated, column- and row-level lineage that spans raw ingestion through transformation pipelines to features and served model outputs, without requiring engineers to manually annotate lineage.
- Give compliance and security teams self-service access to audit-ready reports (access history, policy change history, data classification coverage) without depending on the platform team to hand-build queries.
- Reduce the governance-related portion of enterprise deal cycles by giving SEs and technical evaluators a fast, credible way to validate fine-grained controls during POC.
- Maintain governance enforcement with negligible performance overhead so that customers do not have to trade off security posture against query/pipeline performance.

## Non-Goals

- Governance Suite is not a general-purpose data catalog or business glossary product; catalog/search UX improvements are tracked separately in the Lakehouse Catalog roadmap.
- Governance Suite does not provide data loss prevention (DLP) content scanning or automatic PII discovery beyond the classification tagging framework described below — deep content-based PII detection is a candidate for a future dedicated product, not this suite.
- Governance Suite does not manage identity lifecycle (provisioning/deprovisioning of users); it integrates with external identity providers (SCIM/SAML/OIDC) rather than replacing them.
- Governance Suite does not extend governance controls to data or systems outside Fluxora (e.g., a customer's separate on-prem warehouse); federated cross-platform governance is out of scope for this PRD.
- This is a GA-stage PRD covering incremental hardening and scale; it does not introduce net-new product categories or a new GA milestone.

## Key Requirements

1. **Unified policy model.** Access policies (role-based and attribute-based) are defined once in Governance Suite and enforced consistently across lakehouse tables, pipeline orchestration job inputs/outputs, and model-serving endpoints — no per-product policy duplication.
2. **Fine-grained, dynamic masking and row/column-level security.** Support row-level filters and column-level masking (static and dynamic, e.g., role-aware redaction) evaluated at query time, applied consistently whether the query originates from SQL, a pipeline job, or a model-serving inference request touching feature data.
3. **End-to-end automated lineage capture.** Lineage is captured automatically from pipeline DAG execution and transformation logic (no manual annotation required for standard operators) and is queryable at table, column, and job level, extending through to model training datasets and served model versions.
4. **Immutable, queryable audit log.** All data access, policy changes, and administrative actions are recorded in an immutable, centrally queryable audit log, retained per customer-configured retention policy and exportable to customer-owned SIEM/storage targets.
5. **Data classification and tagging framework.** Support manual and rule-based tagging of tables/columns (e.g., "PII," "financial," "restricted") with policy rules that reference tags rather than requiring per-object configuration, so classification-driven policy scales with schema growth.
6. **Identity provider integration.** Native SCIM/SAML/OIDC integration for user and group sync, with policy assignment supportable at the group level to avoid per-user policy sprawl.
7. **Compliance reporting templates.** Pre-built, exportable reports for common frameworks (SOC 2 access review, GDPR data subject access request support, HIPAA access accounting) that compliance teams can generate without engineering involvement.
8. **Delegated administration.** Support scoped governance admin roles so that individual business units or data domains can manage their own policies within guardrails set centrally, rather than requiring a single central admin team as a bottleneck.

## Non-Functional Requirements

- **Performance.** Policy enforcement (masking, row filtering) must add no more than low-single-digit-percent overhead to query and pipeline execution latency at customer-representative data volumes; lineage capture must not introduce observable latency to pipeline job execution.
- **Scale.** Policy engine and lineage graph must scale to the largest GA customer environments (tens of thousands of tables, hundreds of millions of lineage edges, thousands of concurrent policy evaluations per second) without degradation.
- **Availability.** Governance enforcement is on the critical path for data access and must meet the same availability SLOs as core lakehouse query serving; the policy engine has no single point of failure and fails closed (denies access) rather than open on internal error.
- **Security.** All audit log data is tamper-evident (write-once, cryptographically verifiable); administrative actions on governance policy itself are subject to the same audit and, optionally, dual-control approval workflows.
- **Compliance.** Governance Suite functionality is in scope for and covered by Fluxora's SOC 2 Type II audit; supports customer configurations needed for HIPAA and GDPR compliance (data residency-aware audit log storage, configurable retention, DSAR reporting support).
- **Data residency.** Audit logs and lineage metadata respect the same data residency boundaries configured for the customer's underlying Fluxora deployment region.
- **Multi-tenancy isolation.** In shared infrastructure deployments, policy and audit data for one tenant must be fully isolated from another at the storage and query layer, with no cross-tenant leakage under any policy misconfiguration.

## Competitive Positioning

Governance Suite's core differentiation against **Databricks Unity Catalog** is breadth of consistent enforcement: Unity Catalog's governance model is strongest within the Databricks lakehouse and Spark-centric workloads, but customers running heterogeneous pipeline orchestration and separate model-serving infrastructure often report needing supplementary tooling to get consistent policy enforcement and lineage across those boundaries. Because Fluxora's lakehouse, orchestration, and model-serving products share a single governed metadata layer natively, Governance Suite is positioned to give customers one policy definition and one lineage graph across the full pipeline-to-serving lifecycle, rather than governance that is strongest at the storage layer and thinner elsewhere. In technical evaluations, this should translate into faster time-to-first-working-policy across a multi-product workload than a comparable Unity Catalog + separate orchestration/serving governance patchwork, since evaluators aren't reconciling two policy models.

Against **Snowflake's native governance features** (RBAC, dynamic data masking, object tagging, access history), the contrast is enforcement scope beyond the warehouse. Snowflake's governance is well-regarded for SQL-layer access control and masking within Snowflake-resident data, but Fluxora customers increasingly run transformation pipelines and model-serving workloads outside a single SQL warehouse boundary — and that's precisely where Snowflake-native governance has less direct reach. Governance Suite is positioned to extend the same row/column-level policy and audit rigor customers expect from a mature warehouse governance model into pipeline execution and model-serving inference, which is a common gap SEs should probe for during discovery with Staff/Senior Data Engineers running technical evaluations.

In both cases, the positioning is "governance that follows the data across the full lifecycle, not just at rest in one system" — this should be the anchor talk track in POCs where the buyer is actively migrating from, or running alongside, Databricks or Snowflake.

## Success Metrics

- Reduction in governance-related deal cycle time (time from technical evaluation start to governance sign-off) for opportunities where Governance Suite is a named POC criterion.
- POC pass rate on governance-specific evaluation criteria (fine-grained access control, lineage completeness, audit export) as tracked by SEs in POC Tracking records.
- Percentage of GA customers with Governance Suite actively enforcing policy (not just enabled) across at least two of the three product surfaces (lakehouse, orchestration, model serving).
- Reduction in support escalations categorized as governance/compliance-blocking within 90 days of GA customer onboarding.
- Net retention delta for accounts with Governance Suite adopted versus accounts without, isolating governance as a stickiness driver.
- Time-to-produce for a standard compliance report (SOC 2 access review equivalent) as measured in customer-reported usage, targeting self-service completion without platform-team involvement.

## Risks & Open Questions

- **Policy sprawl risk.** Delegated administration (Key Requirement 8) reduces central bottlenecks but introduces risk of inconsistent or conflicting policies across business units; open question on whether centrally enforced guardrails are sufficient or whether a policy-conflict detection feature is needed sooner than currently roadmapped.
- **Lineage completeness for custom code.** Automated lineage capture is strong for standard pipeline operators but lineage through arbitrary user-defined transformation code (custom Python/SQL UDFs) is harder to capture completely; incomplete lineage in custom-code-heavy environments is a recurring POC objection that needs a clearer mitigation story (partial lineage with confidence indicators vs. requiring annotation).
- **Performance overhead at extreme scale.** Non-functional targets for policy enforcement overhead are validated against current largest GA customers; it's an open question whether the policy engine architecture holds those overhead targets as the largest accounts continue to grow lineage graph size and concurrent policy evaluation load.
- **Competitive response risk.** Both Databricks and Snowflake are actively investing in cross-boundary governance (e.g., broader catalog federation efforts); the "governance follows data across the full lifecycle" positioning window may narrow over time and should be revisited each roadmap cycle rather than treated as a durable moat.
- **Audit log retention cost.** Long retention periods requested by regulated customers (multi-year) have real storage cost implications; open question on whether tiered/archival storage for audit logs should be a customer-configurable default rather than a custom arrangement.
- **Cross-region governance for global customers.** Data residency-aware audit storage is a stated non-functional requirement, but multi-region customers with global data access patterns may need governance policy that itself spans regions in ways not yet fully specified; needs follow-up scoping with Solutions Architecture before being treated as fully solved.
