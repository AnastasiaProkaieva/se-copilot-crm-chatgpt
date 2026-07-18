# Governance Suite — Technical FAQ

## Architecture & Deployment

### How does Governance Suite enforce policy consistently across the lakehouse, pipeline orchestration, and model-serving products?
Governance Suite is a single control plane, not three product-specific permission systems stitched together. Access policies — role-based and attribute-based — are defined once and enforced at query/execution time regardless of whether the request originates from a SQL query against lakehouse tables, a pipeline orchestration job reading/writing job inputs and outputs, or a model-serving inference request touching feature data. This replaced the pre-GA state where access control, lineage, and audit logging were fragmented across products with inconsistent logging granularity, and it's the reason security teams can get one answer to "who has access to this table and why" instead of reconciling three systems.

### What performance overhead should we expect from enabling row-level filtering and column-level masking?
Policy enforcement — row-level filters and static or dynamic column-level masking — is designed to add no more than low-single-digit-percent overhead to query and pipeline execution latency at customer-representative data volumes, and lineage capture is designed not to introduce observable latency to pipeline job execution. These targets are validated against Fluxora's current largest GA customer environments; policy engine horizontal scaling work is actively in progress (Q3 2026) to sustain thousands of concurrent policy evaluations per second as the largest accounts continue to grow, so SEs should frame this as a validated target under continuous engineering investment rather than a static, one-time benchmark.

### What happens to data access requests if the policy engine itself becomes unavailable or hits an internal error?
Governance enforcement sits on the critical path for data access, so it is held to the same availability SLOs as core lakehouse query serving, and the policy engine is architected with no single point of failure. Critically, it fails closed: on internal error, the system denies access rather than defaulting open. This is a deliberate design choice for regulated customers who need assurance that a governance-layer fault degrades to "no access" rather than "unchecked access."

## Security & Compliance

### Is the audit log genuinely immutable, and can we export it to our own SIEM or storage?
Yes. All data access, policy changes, and administrative actions are recorded in a centrally queryable, immutable audit log that is tamper-evident — write-once and cryptographically verifiable. Retention is customer-configurable, and audit log export to customer-owned SIEM or storage targets with configurable retention windows shipped in the most recent release cycle (Q1–Q2 2026), so this is a currently available capability, not a roadmap item.

### Which compliance frameworks and report templates does Governance Suite support today?
Governance Suite functionality is in scope for Fluxora's SOC 2 Type II audit, and the platform supports the customer-side configuration needed for HIPAA and GDPR compliance, including data residency-aware audit log storage and configurable retention. Pre-built, exportable report templates exist for SOC 2 access review, GDPR data subject access request (DSAR) support, and HIPAA access accounting, designed so compliance teams can generate them without engineering involvement. The GDPR DSAR template most recently reached self-service availability; HIPAA access accounting template enhancements and further SOC 2 self-service refinements are active areas of continued investment rather than one-time deliverables.

### How is tenant isolation guaranteed for audit and policy data in shared infrastructure deployments?
In shared infrastructure deployments, policy and audit data for one tenant is fully isolated from another at both the storage and query layer. This is a hard non-functional requirement: no cross-tenant leakage is permitted under any policy misconfiguration, which is a distinct guarantee from simple logical separation — isolation holds even in a misconfigured-policy scenario, not only under correct configuration.

## Integration & Interoperability

### Does Governance Suite integrate with our existing identity provider, and can we assign policy at the group level?
Yes. Governance Suite has native SCIM/SAML/OIDC integration for user and group sync, and policy can be assigned at the group level rather than requiring per-user policy configuration. SCIM group-based policy assignment reached general availability in the most recent release cycle, specifically to eliminate per-user policy sprawl for customers whose groups are synced from their IdP — this is a shipped capability evaluators can test directly in a POC.

### How complete is automated lineage capture, especially through custom Python/SQL transformation code?
Lineage is captured automatically from pipeline DAG execution and transformation logic for standard operators — no manual annotation required — and is queryable at table, column, and job level, extending through to model training datasets and served model versions. Where lineage is less complete today is arbitrary user-defined transformation code (custom Python/SQL UDFs); this is a known, acknowledged gap and a recurring POC objection in custom-code-heavy environments. The near-term mitigation is confidence-indicator tagging for lineage traversal through UDFs, which is planned for Q3 2026 rather than shipped today — SEs evaluating a UDF-heavy pipeline should scope this honestly during discovery rather than imply full automated coverage.

### Is Governance Suite a replacement for our data catalog or business glossary tooling?
No. Governance Suite is explicitly not a general-purpose data catalog or business glossary product — catalog and search UX are tracked separately under the Lakehouse Catalog roadmap. It's also worth noting Governance Suite does not perform DLP-style content scanning or automatic PII discovery; its classification framework covers manual and rule-based tagging (e.g., "PII," "financial," "restricted") that policy rules can reference, but deep content-based PII detection is out of scope for this product today.

## Competitive Differentiation

### How does Governance Suite compare to Databricks Unity Catalog?
Unity Catalog's governance model is strongest within the Databricks lakehouse and Spark-centric workloads; customers running heterogeneous pipeline orchestration and separate model-serving infrastructure alongside Databricks often need supplementary tooling to get consistent policy enforcement and lineage across those boundaries. Because Fluxora's lakehouse, orchestration, and model-serving products share a single governed metadata layer natively, Governance Suite gives customers one policy definition and one lineage graph across the full pipeline-to-serving lifecycle. In technical evaluations, this should translate into faster time-to-first-working-policy across a multi-product workload than a Unity Catalog-plus-separate-orchestration/serving-governance patchwork, since evaluators aren't reconciling two policy models.

### How does Governance Suite compare to Snowflake's native governance features (RBAC, dynamic masking, tagging, access history)?
Snowflake's native governance is well-regarded for SQL-layer access control and masking within Snowflake-resident data. The gap is enforcement scope beyond the warehouse: Fluxora customers increasingly run transformation pipelines and model-serving workloads outside a single SQL warehouse boundary, and that's precisely where Snowflake-native governance has less direct reach. Governance Suite extends the same row/column-level policy and audit rigor customers expect from a mature warehouse governance model into pipeline execution and model-serving inference — dynamic column-level masking was extended to model-serving inference requests touching feature data in the most recent release, closing what had been the last enforcement gap across the three surfaces. This is a good probe point for Staff/Senior Data Engineers running a technical evaluation who are used to Snowflake's warehouse-scoped model.

## Pricing & Licensing

### Is Governance Suite a separate SKU, and how is it licensed?
This FAQ covers technical and architectural questions; specific packaging, edition eligibility, and quote-level pricing are commercial terms that vary by deal and should be confirmed with your Fluxora account team or deal desk rather than assumed from this document. SEs should avoid committing to a specific packaging model in an RFP response without checking current commercial guidance.

### Does the price scale with table count, lineage graph size, or policy evaluation volume?
The engineering scale targets are documented and can be cited with confidence: the policy engine and lineage graph are built to scale to tens of thousands of tables, hundreds of millions of lineage edges, and thousands of concurrent policy evaluations per second at the largest GA customer environments without degradation. Whether and how commercial pricing maps to any of those scale dimensions is a licensing question, not an architecture question, and should be routed to the account team rather than answered from technical documentation.

## Roadmap

### What's coming next for lineage completeness on custom code and for delegated administration safety?
Two related gaps are actively being worked in the near-term roadmap. Confidence-indicator tagging for automated lineage traversal through custom Python/SQL UDFs is planned for Q3 2026, aimed at mitigating the recurring "incomplete lineage" POC objection with partial-lineage-plus-confidence-signal rather than requiring manual annotation. On delegated administration, business-unit-scoped policy guardrail templates are planned for Q3 2026, followed by policy-conflict detection across delegated admin domains and a dual-control approval workflow for changes to governance policy itself, both planned for Q4 2026. SEs should represent these as planned, not yet shipped, and avoid committing customers to specific delivery dates in an RFP.

### Are there plans to support governance for multi-region, global data access patterns?
Today, audit logs and lineage metadata already respect the data residency boundaries configured for a customer's underlying Fluxora deployment region. What's not yet fully solved is policy that itself needs to span multiple data-residency boundaries for global customers with cross-region access patterns — this is an open item flagged for follow-up scoping with Solutions Architecture. Cross-region policy scoping and data residency-aware audit log routing enhancements are on the roadmap for Q2 2027, alongside policy engine failover hardening for global-scale fail-closed behavior, but all are currently in Planned status. For active deals with genuinely global, multi-region governance requirements, SEs should loop in Solutions Architecture rather than represent this as solved today.
