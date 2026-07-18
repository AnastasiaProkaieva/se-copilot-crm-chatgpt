# PipelineOps — PRD

**Status:** Approved | **Stage:** GA (since 2024) | **Owner:** Product Manager, PipelineOps

## Problem Statement

Data and ML teams building on modern lakehouse architectures need to orchestrate increasingly complex, interdependent workflows — ingestion jobs, transformation pipelines, feature engineering, model training, and batch inference — across heterogeneous compute engines. Today, most enterprise teams solve this with self-managed Apache Airflow clusters, which require dedicated platform engineering headcount to operate, upgrade, and scale, or with cloud-native schedulers (e.g., Databricks Workflows) that lock orchestration logic into a single vendor's compute layer and provide limited cross-platform lineage.

The result is fragmented ownership: pipeline reliability, dependency management, and failure recovery become a tax on data engineering velocity, and lineage/observability data is scattered across disconnected tools, undermining governance and audit readiness. Fluxora customers consistently cite "who broke the pipeline and what did it touch downstream" as a top-three operational pain point during platform migrations.

PipelineOps addresses this by providing fully managed, DAG-based orchestration natively integrated with Fluxora's lakehouse storage and Governance Suite — eliminating the operational burden of self-hosted schedulers while giving customers lineage-aware pipeline execution out of the box.

## Target Personas

- **Head of Data Engineering** — owns pipeline reliability and team velocity; evaluates whether PipelineOps reduces on-call burden and infrastructure maintenance relative to self-managed Airflow.
- **VP of Engineering** — cares about total cost of ownership, platform consolidation, and reducing the number of distinct systems engineering must operate and secure.
- **Chief Data Officer** — accountable for data governance, lineage, and audit readiness across the organization; evaluates PipelineOps as the control point connecting pipeline execution to Governance Suite.
- **Staff/Senior Data Engineer (technical evaluator)** — hands-on evaluator during POC; assesses DAG authoring ergonomics, backfill behavior, dependency semantics, and migration path from existing Airflow DAGs.

## Goals

1. Provide a managed orchestration layer that removes the operational burden of running and scaling a scheduler (no metastore/scheduler infrastructure for customers to patch, upgrade, or capacity-plan).
2. Capture pipeline-level and task-level lineage automatically and stream it into Governance Suite without requiring custom instrumentation.
3. Support DAG-based orchestration for both data pipelines (ELT/ETL) and ML workflows (training, batch inference, feature pipelines) in a single control plane.
4. Provide a credible, low-friction migration path for teams currently running Apache Airflow, including DAG-compatibility tooling.
5. Deliver enterprise-grade reliability (SLA-backed uptime, retries, alerting) so PipelineOps can serve as the orchestration system of record for regulated and mission-critical workloads.

## Non-Goals

- PipelineOps is not a general-purpose workflow engine for non-data use cases (e.g., business process automation, CI/CD orchestration); customers should use purpose-built tools for those.
- PipelineOps does not aim to replace customers' existing BI scheduling or reverse-ETL tools; it orchestrates pipelines feeding into and out of the lakehouse, not downstream BI refresh logic.
- This release does not include a visual, no-code DAG builder for business analysts — DAG authoring remains code-first (Python/YAML), targeted at data engineers.
- PipelineOps does not manage compute infrastructure provisioning outside of Fluxora's managed compute pools (e.g., it will not orchestrate arbitrary third-party Kubernetes clusters in this phase).

## Key Requirements

1. **DAG authoring SDK** — Python and YAML-based DAG definition supporting task dependencies, dynamic task generation, parameterization, and conditional branching, with a local CLI for validation before deployment.
2. **Managed scheduler control plane** — Fluxora-hosted, multi-tenant scheduler with no customer-managed infrastructure; supports cron, event-driven, and dependency-triggered execution.
3. **Native lineage capture** — automatic capture of task-level input/output dataset references, execution metadata, and run-level lineage graphs, streamed in real time into Governance Suite without requiring manual annotation.
4. **Cross-engine task execution** — ability to orchestrate tasks across Fluxora's lakehouse compute (SQL/Spark jobs), model serving endpoints, and external systems via connectors (e.g., dbt, REST APIs, webhook triggers).
5. **Airflow migration tooling** — a DAG conversion utility that parses existing Airflow DAG definitions and flags/auto-migrates common operators to PipelineOps equivalents, plus a compatibility mode for a defined subset of Airflow operators.
6. **Backfill and replay management** — self-service backfill of historical DAG runs with configurable concurrency limits, partition-aware backfills, and idempotent re-run semantics.
7. **Alerting and failure recovery** — configurable retry policies, task-level and DAG-level alerting (email, Slack, PagerDuty, webhook), and automatic failure isolation so downstream tasks do not execute on upstream failure unless explicitly configured.
8. **Role-based access control on DAGs** — namespace-level and DAG-level permissions integrated with Fluxora's centralized IAM, so pipeline ownership and edit/execute permissions map to team boundaries.
9. **Multi-environment promotion** — support for dev/staging/prod DAG promotion workflows with environment-scoped variables and secrets, integrated with standard CI/CD (Git-based deployment).
10. **Observability dashboard** — run history, SLA-miss tracking, task duration trends, and dependency graph visualization within the Fluxora console.

## Non-Functional Requirements

- **Availability:** 99.9% scheduler control-plane uptime SLA for GA customers; scheduler must tolerate single-AZ failure without dropping scheduled triggers.
- **Scale:** Support DAGs with up to 5,000 tasks and tenant-level concurrent execution of 10,000+ active task instances without control-plane degradation.
- **Latency:** Event-driven and dependency-triggered task starts within 30 seconds of trigger condition being met at P95.
- **Security:** All DAG definitions, parameters, and secrets encrypted at rest and in transit; secrets management integrated with customer-managed KMS keys (BYOK) for enterprise tier.
- **Access control:** Fine-grained RBAC enforced at DAG, task, and connection-credential level; full audit logging of DAG edits, permission changes, and manual run triggers.
- **Compliance:** SOC 2 Type II coverage inclusive of PipelineOps control plane; lineage and execution logs retained in a manner consistent with customer data-residency configuration (no cross-region data movement for logs/lineage without explicit customer opt-in).
- **Multi-tenancy isolation:** Strict logical isolation between customer tenants at the scheduler and metadata-store level; no shared execution state across tenants.
- **Disaster recovery:** Control-plane metadata (DAG definitions, run history, lineage events) backed up with RPO ≤ 15 minutes and RTO ≤ 4 hours.

## Competitive Positioning

**Vs. Databricks Workflows:** Databricks Workflows orchestrates well within the Databricks compute environment but is inherently tied to that platform's job clusters and notebooks — it is not designed to be a neutral orchestration layer across multiple engines or vendors. PipelineOps is positioned as engine-agnostic: it orchestrates lakehouse SQL/Spark jobs, model-serving tasks, and third-party connectors from a single control plane, and — because it's native to Fluxora's Governance Suite — it produces unified cross-pipeline lineage rather than lineage scoped only to jobs run inside one vendor's notebooks. For customers who are not fully committed to a single-vendor compute stack, this reduces long-term lock-in risk relative to Workflows.

**Vs. self-managed Apache Airflow:** Airflow is the de facto open-source standard and PipelineOps's DAG-authoring model is intentionally familiar to Airflow users to minimize migration friction. The differentiation is entirely operational: Airflow requires customers to run, patch, scale, and upgrade their own scheduler, metastore, and worker fleet — commonly a multi-person, ongoing platform-engineering commitment. PipelineOps removes that operational surface entirely as a managed service, while adding lineage capture, governance integration, and enterprise RBAC that self-managed Airflow does not provide out of the box (these typically require bolting on separate open-source or third-party tooling, such as OpenLineage integrations, which customers must then also maintain). The pitch to a Head of Data Engineering evaluating a migration is: keep the DAG mental model your team already knows, shed the infrastructure ownership, and get lineage/governance for free.

**General framing:** PipelineOps should be positioned as the orchestration layer that pairs naturally with Fluxora's broader platform story — customers adopting Fluxora for lakehouse storage or ML serving get materially faster time-to-value on orchestration and lineage than assembling Airflow plus a bolted-on lineage tool, and materially more platform flexibility than adopting Databricks Workflows as their orchestration standard.

## Success Metrics

- **Adoption:** % of Fluxora lakehouse customers with at least one production DAG running in PipelineOps within 90 days of platform onboarding (target: 60% by end of next fiscal year).
- **Migration conversion:** Number/percentage of POC deals where Airflow migration tooling is used and results in a signed multi-quarter commitment.
- **Reliability:** Scheduler control-plane uptime against the 99.9% SLA; task-start latency P95 against the 30-second target.
- **Lineage coverage:** % of production DAG task executions with complete lineage records successfully ingested into Governance Suite (target: 99%+).
- **Operational efficiency (customer-reported):** Reduction in customer-reported orchestration-related on-call incidents post-migration from self-managed Airflow (tracked via customer success check-ins and POC exit surveys).
- **Expansion:** Increase in average DAG count and task-execution volume per customer account quarter-over-quarter, as a leading indicator of platform stickiness.

## Risks & Open Questions

- **Airflow compatibility gaps:** The compatibility mode covers a defined operator subset; customers with heavily customized or plugin-dependent Airflow deployments may hit migration friction not fully captured in current tooling coverage. Open question: what is the minimum viable operator coverage to unblock the majority of enterprise POCs, and how do we message unsupported operators during Discovery?
- **Cross-engine lineage completeness:** Lineage capture is strongest for tasks running on Fluxora-native compute; tasks executed via external connectors (e.g., arbitrary REST APIs) may produce incomplete lineage unless the connector explicitly emits lineage metadata. This could undercut the core governance differentiation if not addressed.
- **Scale ceiling validation:** The 5,000-task DAG / 10,000 concurrent task-instance targets are based on internal load testing; they have not yet been stress-tested against the largest prospective enterprise accounts' real workloads. Recommend validating with at least one large POC before citing these numbers in competitive RFP responses.
- **Multi-cloud/data residency nuance:** Customers with strict data-residency requirements may require lineage and run-metadata storage to stay within a specific region; current DR design assumes standard regional backup topology, and edge cases for residency-constrained tenants need explicit review with Legal/Compliance.
- **Pricing/packaging ambiguity:** Whether Airflow migration tooling and BYOK secrets management are bundled into a single enterprise tier or sold as separate add-ons is not yet finalized; this affects how SEs should position cost during competitive displacement conversations and should be resolved before the next RFP cycle.
- **Competitive response risk:** If Databricks extends Workflows with broader cross-engine support or improved lineage in a future release, the "engine-agnostic" differentiation narrows; Product should monitor Databricks Workflows roadmap signals and revisit this positioning section accordingly.
