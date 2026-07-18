# StreamSync — Roadmap

StreamSync is in private beta with design partners, delivering native CDC ingestion from operational databases directly into Lakehouse Core tables. The roadmap below tracks the path from private beta to General Availability, targeted for Q1 2027, and the hardening work that follows.

## Q3 2026
**Theme: Private beta feature completeness across core connectors and POC experience.**
- PostgreSQL, MySQL, and SQL Server log-based CDC connectors (WAL/binlog/CDC tables) reach private beta feature completeness (In Progress)
- Initial full-table snapshot with seamless, no-downtime transition to incremental streaming CDC (In Progress)
- Self-serve, time-boxed POC mode enabling technical evaluators to stand up a source connection within a single session (In Progress)
- Baseline pipeline observability (replication lag, throughput, connector health) surfaced in the private beta monitoring UI (In Progress)

## Q4 2026
**Theme: Reliability and failure-handling hardening ahead of GA scope lock.**
- Schema drift detection and propagation with configurable auto-evolve vs. quarantine-and-alert policies (In Progress)
- Dead-letter queue with inspectable payloads and replay mechanism for malformed change events (In Progress)
- Exactly-once delivery hardening, including adversarial testing of connector restart storms and source failover scenarios (In Progress)
- Oracle CDC connector go/no-go checkpoint, 90 days ahead of GA (Planned)

## Q1 2027
**Theme: General Availability — StreamSync becomes Lakehouse Core's native CDC ingestion path.**
- **General Availability (GA) launch** of StreamSync with native CDC connectors for PostgreSQL, MySQL, and SQL Server (Planned)
- Unified catalog and lineage integration so every StreamSync pipeline and target table is discoverable and auditable identically to batch tables (Planned)
- Backpressure-aware autoscaling of ingestion compute, with p50 ≤10s / p99 ≤60s latency validated under design-partner production load (Planned)
- GA-grade security and compliance: private connectivity, managed secrets vault, and audit logging aligned to SOC 2 Type II and applicable HIPAA/GDPR commitments (Planned)
- Disaster recovery targets met at GA: checkpoint state and pipeline configuration durably persisted and recoverable, meeting RPO ≤5 minutes / RTO ≤30 minutes for a regional infrastructure failure (Planned)

## Q2 2027
**Theme: Post-GA expansion — closing the connector gap and proving consolidation economics at scale.**
- Oracle CDC connector GA as the committed fast-follow to the initial connector set (Planned)
- Multi-tenant isolation hardening for high-density, high-scale production deployments, building on the RPO ≤5 min / RTO ≤30 min disaster-recovery targets already met at GA (Planned)
- Finalized StreamSync pricing model and Confluent coexistence-vs-displacement enablement for field teams (Planned)
- Validated sustained throughput beyond 50,000 change events/sec per pipeline for high-volume production customers (Planned)
