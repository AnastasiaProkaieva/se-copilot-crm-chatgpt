# Lakehouse Core — PRD

Status: Active (Post-GA, Hardening & Scale) | Stage: GA (since 2024) | Owner: Product Manager, Lakehouse Core

## Problem Statement

Enterprises running analytics and AI/ML workloads on legacy data warehouses or hand-rolled data lakes face a persistent tradeoff: warehouses offer transactional guarantees and governance but lock data into proprietary formats and charge a storage-and-compute premium, while raw object-storage lakes are cheap and open but lack ACID semantics, schema enforcement, and reliable concurrent read/write behavior. Teams end up duplicating data across a warehouse for BI and a lake for ML/ELT, creating reconciliation overhead, staleness, and duplicated storage cost. As organizations consolidate onto fewer platforms to support both traditional analytics and growing AI/ML pipelines, they need a single system of record that is open-format, transactionally consistent, and performant enough to serve as the foundation for both BI and ML workloads without a second copy of the data.

Lakehouse Core exists to be that system of record: object-storage-backed, ACID-compliant, and interoperable with the broader data ecosystem, so customers stop paying the "two-copy tax" of running a warehouse and a lake side by side.

## Target Personas

- **Head of Data Engineering** — owns the platform migration decision, evaluates total cost of ownership versus the incumbent warehouse, and is accountable for pipeline reliability and data quality SLAs.
- **VP of Engineering** — sponsors the multi-quarter platform commitment, weighs build-vs-buy tradeoffs, and cares about how Lakehouse Core reduces long-term infrastructure sprawl and vendor lock-in.
- **Chief Data Officer** — accountable for enterprise data governance, compliance posture, and the strategic narrative of "one source of truth" across BI and AI initiatives.
- **Staff/Senior Data Engineer** (technical evaluator) — runs the proof-of-concept, validates ACID correctness under concurrent writes, benchmarks query performance, and tests format interoperability with existing tools.

## Goals

1. Provide a single, object-storage-backed table format that supports full ACID transactions for both structured and semi-structured data.
2. Eliminate the need for a separate warehouse copy of data by delivering BI-grade query performance directly on lakehouse tables.
3. Maintain open, interoperable table metadata so customers are not locked into a single query engine or vendor.
4. Reduce total storage cost by consolidating redundant copies of data currently split across warehouse and lake systems.
5. Give enterprise data leadership confidence in governance, lineage, and access control sufficient to pass security and compliance review during 90–180 day evaluation cycles.

## Non-Goals

- Lakehouse Core is not a BI visualization or dashboarding product; it is the storage and transaction layer beneath Fluxora's and third-party query/BI tools.
- Lakehouse Core does not manage pipeline orchestration or scheduling logic — that responsibility lives with Fluxora's pipeline orchestration product line, which reads from and writes to Lakehouse Core.
- Lakehouse Core does not provide model training or serving infrastructure — that is owned by Fluxora's ML model serving product, which consumes Lakehouse Core tables as a data source.
- This roadmap window does not include a GA milestone (already GA since 2024); it is scoped to incremental hardening, scale limits, and enterprise-readiness features, not net-new product categories.
- No commitment in this PRD to support on-premises or air-gapped deployments; Lakehouse Core targets customer cloud accounts on major public cloud object storage.

## Key Requirements

1. **ACID transactions on object storage.** Support atomic, consistent, isolated, and durable multi-statement writes (including concurrent writer conflict resolution) directly against customer-owned object storage (S3, GCS, Azure Blob), with no proprietary storage engine required.
2. **Schema evolution and enforcement.** Support additive and backward-compatible schema changes (column add/drop/rename, type widening) without requiring full table rewrites, with enforcement rules configurable per table to reject non-conforming writes.
3. **Time travel and rollback.** Retain historical table versions for a configurable retention window, allowing point-in-time queries and rollback to a prior snapshot for audit, debugging, and recovery scenarios.
4. **Open, interoperable table format.** Expose table metadata in a format readable by third-party query engines (e.g., Spark, Trino, Presto) without requiring proprietary connectors, so customers avoid engine-level lock-in.
5. **Fine-grained access control.** Support row-level and column-level security policies enforced consistently regardless of which query engine or Fluxora product accesses the table.
6. **Automated table maintenance.** Provide background compaction, file size optimization, and stale-snapshot cleanup (vacuuming) without requiring customer-managed cron jobs or manual intervention.
7. **Semi-structured data support.** Natively ingest and query nested/semi-structured formats (JSON, Avro, Parquet with nested types) alongside structured tabular data within the same table abstraction.
8. **Change data capture (CDC) feed.** Emit a consumable change stream (inserts/updates/deletes) per table so downstream pipelines and ML feature stores can subscribe incrementally rather than re-scanning full tables.
9. **Cross-region replication.** Support asynchronous replication of tables across cloud regions for disaster recovery and data residency requirements common in enterprise RFPs.

## Non-Functional Requirements

- **Performance.** Sub-second metadata resolution for table snapshot lookups at 100K+ partition scale; query planning overhead must not materially exceed that of native cloud data warehouse query planners for equivalent workloads, to support credible time-to-first-query comparisons during POCs.
- **Scalability.** Individual tables must scale to tens of billions of rows and petabyte-scale storage without degrading write throughput or requiring manual partitioning redesign.
- **Concurrency.** Support hundreds of concurrent readers and dozens of concurrent writers per table with optimistic concurrency control and bounded retry/backoff on write conflicts.
- **Availability.** Control plane (metadata service) SLA of 99.95% uptime; data plane availability inherits the durability guarantees of underlying object storage (typically eleven nines durability as published by cloud providers).
- **Security.** Encryption at rest (customer-managed key support) and in transit by default; integration with customer identity providers via SAML/OIDC; audit logging of all schema changes, access grants, and data access at the row/column-policy level.
- **Compliance.** Support for SOC 2 Type II control mapping, GDPR data residency and right-to-erasure workflows (including targeted row deletion with vacuum confirmation), and HIPAA-eligible configurations for regulated-industry customers.
- **Data governance.** Full lineage tracking from raw ingestion through transformation to consumption, exposed via API for integration with enterprise data catalogs.
- **Interoperability.** No degradation of read/write compatibility when tables are accessed by non-Fluxora engines conforming to the open table format spec.

## Competitive Positioning

**Vs. Databricks (Delta Lake):** Delta Lake pioneered ACID-on-object-storage and remains deeply tied to the Databricks compute runtime for its best performance characteristics and advanced features (e.g., liquid clustering, deep optimization). Lakehouse Core differentiates by treating engine-agnosticism as a first-class design principle rather than a compatibility afterthought: customers can point Spark, Trino, or Fluxora's own query layer at the same tables without needing to route through a single vendor's compute for full feature parity. Our positioning to technical evaluators emphasizes faster time-to-first-query in multi-engine environments and lower operational overhead for customers who do not want their transactional table layer coupled to one company's compute pricing model.

**Vs. Snowflake's storage layer:** Snowflake's storage layer is proprietary and only fully accessible through Snowflake compute; data effectively lives inside Snowflake's format even when "external tables" are used, which limits portability and creates a durable lock-in vector that shows up in renewal negotiations. Lakehouse Core's core pitch is openness: the data lives in the customer's own object storage, in an open table format, readable by any conformant engine — so switching or multi-tooling later doesn't require a re-platforming project. For CDOs and VPs of Engineering evaluating multi-quarter commitments, this is framed as reducing platform risk: Fluxora does not need to be the last vendor standing for the customer's data to remain usable.

**Shared narrative across both:** Fluxora's differentiation is not "we do transactions on object storage too" — both competitors already do. It is "you don't have to choose your compute vendor and your storage format at the same time," which shortens POC cycles for customers already running heterogeneous tooling and reduces the perceived risk of a multi-year platform bet.

## Success Metrics

- **POC-to-close conversion rate** for deals where Lakehouse Core is the primary evaluated component, tracked against the 90–180 day deal cycle benchmark.
- **Storage consolidation ratio**: average reduction in duplicate data copies (warehouse + lake) reported by customers within 6 months of migration.
- **Query performance parity**: percentage of benchmarked BI workloads that meet or exceed prior warehouse query latency post-migration.
- **Time-to-first-query** in technical POCs, measured from environment provisioning to first successful query against a migrated dataset.
- **Concurrent writer conflict rate**: production incidence of write conflicts requiring manual resolution, targeted to stay below defined threshold at scale.
- **Net Revenue Retention** contribution from Lakehouse Core-attached accounts, as a proxy for platform stickiness once tables are established as system of record.
- **Compliance review pass rate**: percentage of enterprise security/compliance reviews passed without a blocking finding on Lakehouse Core's governance or audit controls.

## Risks & Open Questions

- **Multi-engine performance parity risk**: if non-Fluxora engines reading our open table format lag meaningfully behind Fluxora's own query layer in benchmarks, the "engine-agnostic" positioning weakens during competitive POCs. Needs ongoing benchmark investment.
- **Migration friction from Delta Lake/Iceberg-committed shops**: customers already standardized on a competing open table format may face nontrivial conversion cost, which could slow deal cycles despite favorable long-term TCO. Open question: invest in a zero-copy/in-place format conversion path, or accept longer migration timelines as a cost of entry?
- **CDC feed scale limits under high-cardinality schema evolution**: early hardening work has surfaced edge cases where frequent schema changes interact poorly with downstream CDC consumers; requires further engineering investigation before broad GA claims in CDC-heavy use cases.
- **Cross-region replication cost transparency**: enterprise buyers evaluating DR requirements will ask for predictable replication cost modeling; current pricing guidance may not be granular enough for accurate RFP responses. Needs Product Marketing and Finance alignment.
- **Compliance certification timing**: HIPAA-eligible configuration support is roadmapped but not yet independently audited; sales teams should avoid representing this as a completed certification until audit closes.
- **Open question on governance ownership boundary**: as Fluxora's pipeline orchestration and ML serving products increasingly write directly to Lakehouse Core tables, it's unresolved which product owns end-to-end lineage presentation to the customer — needs a cross-product decision to avoid conflicting sales narratives.
