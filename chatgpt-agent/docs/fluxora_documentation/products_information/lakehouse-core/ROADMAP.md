# Lakehouse Core — Roadmap

Lakehouse Core has been GA since 2024 and is now the transactional system of record for customers consolidating BI and AI/ML workloads onto a single, open-format table layer. This roadmap covers incremental hardening, scale, and enterprise-readiness work — no GA milestone is in scope for this window — with emphasis on governance depth, multi-engine performance parity, CDC scale limits, and cross-region replication maturity.

## Recently Shipped (Q1–Q2 2026)

Theme: Strengthening the governance and concurrency foundations enterprise reviewers scrutinize first.

- Refreshed SOC 2 Type II control mapping across schema-change, access-grant, and row/column-policy audit logging (Shipped)
- Consistency fixes for row-level and column-level access policy enforcement across Spark, Trino, and Fluxora's native query layer (Shipped)
- Configurable time-travel retention window improvements, including tighter point-in-time query performance (Shipped)
- Initial hardening pass on CDC feed behavior under schema evolution, addressing a subset of previously identified high-cardinality edge cases (Shipped)

## Q3 2026

Theme: Deepening compliance and lineage capabilities to shorten enterprise security-review cycles.

- GDPR right-to-erasure workflow with automated vacuum confirmation for targeted row deletion (In Progress)
- Lineage tracking API for ingestion-through-consumption traceability, exposed for enterprise data catalog integration (Planned)
- Continued HIPAA-eligible configuration work ahead of independent third-party audit — not yet representable as a completed certification (In Progress)
- Concurrent writer conflict-rate monitoring and alerting to support the production conflict-rate success metric (Planned)

## Q4 2026

Theme: Closing the multi-engine performance gap and further hardening CDC under schema evolution.

- Expanded query-planning benchmark suite comparing Lakehouse Core against native cloud warehouse planners for time-to-first-query claims (In Progress)
- Trino and Presto read-path optimizations targeting parity with Fluxora's own query layer for the engine-agnostic positioning (In Progress)
- Continued CDC feed hardening for remaining high-cardinality schema-evolution edge cases (In Progress)
- Cross-region replication cost estimator to give enterprise DR evaluators granular pricing guidance for RFP responses (Planned)

## Q1 2027

Theme: Pushing scale ceilings on metadata and storage maintenance for petabyte-scale, multi-billion-row tables.

- Validated sub-second metadata resolution for table snapshot lookups beyond the current 100K-partition benchmark (Planned)
- Zero-copy, in-place format conversion path for tables already committed to Iceberg or Delta Lake, reducing migration friction (Planned)
- Expanded schema evolution support for additional type-widening scenarios without full table rewrites (Planned)
- Automated compaction and file-size optimization tuning improvements for petabyte-scale tables (In Progress)

## Q2 2027

Theme: Enterprise-grade concurrency and disaster-recovery readiness at scale.

- Increased supported concurrent-writer ceiling per table with refined optimistic concurrency backoff (Planned)
- Cross-region replication general availability for disaster recovery and data-residency requirements (Planned)
- Target completion of HIPAA-eligible configuration third-party audit (Planned)
- Cross-product lineage presentation alignment with pipeline orchestration and ML serving to deliver a single end-to-end lineage narrative (Planned)
