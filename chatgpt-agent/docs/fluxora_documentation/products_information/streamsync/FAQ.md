# StreamSync — Technical FAQ

## Architecture & Deployment

### What is StreamSync, and how does it fit into Lakehouse Core?
StreamSync is Fluxora's native change-data-capture (CDC) and streaming ingestion capability, built directly into Lakehouse Core rather than delivered as a bolt-on integration. It uses log-based capture (WAL, binlog, or CDC tables, depending on source) to read changes from operational databases and writes them directly into Lakehouse Core tables via the existing table format's transaction log — there is no intermediate broker or object-storage staging step exposed to the user. StreamSync is currently in private beta with design partners, targeting General Availability in Q1 2027.

### Does StreamSync require running a separate streaming cluster or broker infrastructure?
No. That's the core architectural difference from a Kafka-based approach: StreamSync's ingestion workers read directly from the source database's change log and apply changes straight into the target lakehouse table. Customers do not provision, operate, or secure a separate event-streaming cluster or connector fleet for the CDC-to-lakehouse use case. Ingestion compute scales independently of Lakehouse Core query compute, and autoscaling responds to source change volume within configured bounds.

### How does StreamSync handle initial data load versus ongoing incremental changes?
A single StreamSync pipeline performs a consistent initial full-table snapshot and then transitions seamlessly into streaming incremental CDC, without manual coordination steps or downtime on the source database. This is a first-class requirement of the product, not a two-tool handoff — the same pipeline definition covers both phases.

### What happens if a connector or worker fails mid-pipeline?
StreamSync's ingestion control plane targets 99.9% availability. A connector or worker failure triggers automatic restart from the last durable checkpoint, with no manual intervention required and no data loss expected. Exactly-once delivery semantics are enforced end-to-end via idempotent apply and checkpointing, so replays or restarts should not produce duplicate or lost rows in the target table — this includes hardening work planned against restart-storm and source-failover edge cases ahead of GA.

### How does StreamSync handle malformed or unprocessable change events?
Malformed or unprocessable events are routed to a dead-letter queue with inspectable payloads, rather than blocking the pipeline or being silently dropped. A replay mechanism lets teams reprocess dead-lettered events once the underlying issue is resolved. Dead-letter handling is part of the Q4 2026 reliability-hardening milestone on the roadmap.

## Security & Compliance

### How is data secured in transit for StreamSync pipelines?
All data in transit — both source-to-StreamSync and StreamSync-to-lakehouse — is encrypted via TLS 1.2 or higher. Source database credentials are stored in Fluxora's managed secrets vault and are never persisted in pipeline configuration.

### Can StreamSync connect to a source database without exposing it to the public internet?
Yes. StreamSync supports private connectivity (VPC peering / PrivateLink-equivalent), so source databases do not need to be exposed to the public internet for CDC ingestion to work.

### Do streamed tables follow the same access control and governance model as batch-ingested tables?
Yes — this is a deliberate design goal. StreamSync pipelines and their target tables are subject to Fluxora's existing role-based access control and column-level masking policies, with no bypass path that exposes raw change events outside governed access. Every StreamSync pipeline and target table is also automatically registered in Fluxora's data catalog with full source-to-target lineage, so streamed data is discoverable and auditable identically to batch-ingested data.

### What compliance certifications apply to StreamSync?
StreamSync inherits Fluxora's platform-level SOC 2 Type II certification, and, where applicable, HIPAA/GDPR data-handling commitments already covered at the platform level. A full audit log is maintained for pipeline configuration changes, connector credential rotations, and schema-evolution decisions, retained per Fluxora's standard compliance retention policy. Multi-tenant isolation for StreamSync compute and networking is consistent with Lakehouse Core's existing tenant isolation model — there is no shared connector infrastructure across customer boundaries.

### What are StreamSync's disaster recovery targets?
At GA, StreamSync targets a recovery point objective (RPO) of 5 minutes or less and a recovery time objective (RTO) of 30 minutes or less, meaning checkpoint state and pipeline configuration are durably persisted and recoverable in the event of a regional infrastructure failure. Multi-region active-active streaming topologies are explicitly out of scope for v1; the supported pattern is single-region ingestion with cross-region replication of the resulting lakehouse tables.

## Integration & Interoperability

### Which source databases does StreamSync support?
At GA, StreamSync will support native, log-based CDC connectors for PostgreSQL, MySQL, and SQL Server. Oracle CDC is planned as a fast-follow, with a go/no-go checkpoint scheduled 90 days ahead of GA to confirm scope. All connectors use log-based capture (WAL, binlog, or CDC tables) rather than polling, to minimize load on the source database and reduce capture latency.

### How does StreamSync handle schema changes on the source database?
StreamSync automatically detects and propagates source schema changes — column adds, drops, renames, and type widening — into the target table schema. Teams can configure policy per pipeline: auto-evolve the target schema automatically, or quarantine-and-alert so a human reviews the change before it's applied. Either way, schema drift is handled explicitly rather than causing silent pipeline failure.

### Is StreamSync a general-purpose event-streaming or pub/sub platform I can point other applications at?
No, and we're direct about that scope. StreamSync is purpose-built for the CDC-to-lakehouse workload — it is not a Kafka-API-compatible pub/sub system and doesn't support arbitrary topic-based messaging or high-fanout distribution to many independent consumer applications. GA scope is database CDC plus a small set of high-value log/event sources. If a prospect's requirement is general-purpose application event streaming (clickstream, IoT telemetry, custom producer SDKs) rather than CDC-to-analytics, that's outside StreamSync's current scope and worth surfacing early in a POC scoping conversation.

## Competitive Differentiation

### How does StreamSync compare to Confluent for CDC-to-analytics use cases?
Confluent's strength is a broad, general-purpose Kafka-native event-streaming platform: a large connector marketplace (120+ connectors), topic-based pub/sub, and support for high-fanout application event architectures. We don't contest that breadth at GA. StreamSync's contest is narrower and sharper: for getting change data from operational databases into governed, query-ready lakehouse tables, StreamSync collapses what would otherwise be a broker plus Kafka Connect connectors plus a separate sink/ETL step into a single managed pipeline with direct-to-table writes, native schema evolution, and lineage already integrated with the rest of Fluxora — one system, one security model, one catalog, instead of two. We should expect StreamSync to deliver faster time-to-first-query than a comparable Confluent-plus-sink-connector-plus-lakehouse-load architecture, with materially less operational surface area for the customer's platform team to run and staff. Avoid citing specific Confluent benchmark numbers (throughput, latency, pricing) in these comparisons — we don't have verified, current figures from Confluent's own materials, so keep the comparison directional and architecture-based.

### If a prospect needs both real-time analytics and general event streaming, does that mean we lose the deal to Confluent?
Not necessarily — it depends on how the requirement is scoped. Where a prospect's need is exclusively CDC-to-lakehouse, StreamSync should let us win the deal without Confluent in the stack at all. Where a prospect genuinely needs both governed analytics and general-purpose event streaming (arbitrary pub/sub, high-fanout consumers, application event backbones), a Confluent-plus-Fluxora coexistence architecture remains a viable and honest recommendation — but StreamSync should still win the CDC-to-analytics slice of that architecture outright. SEs should scope which pattern applies early in discovery rather than defaulting to a displacement pitch in accounts with broad event-streaming needs, since over-claiming full Confluent replacement there can set up an unwinnable technical evaluation.

## Pricing & Licensing

### How is StreamSync priced?
StreamSync's pricing model is not yet finalized. Options under evaluation include a StreamSync-specific throughput/volume metric, bundling into existing Lakehouse Core compute pricing, or a hybrid of the two — with finalization targeted for Q2 2027, after GA. SEs should not commit to a specific pricing structure in active deal cycles; frame the consolidation value (one system instead of two) qualitatively until the model is locked, and flag pricing-sensitive opportunities to product/deal desk for guidance.

## Roadmap

### Is StreamSync available for production use today, and when is GA?
StreamSync is currently in private beta with design partners. GA is targeted for Q1 2027, with connector feature-completeness (PostgreSQL, MySQL, SQL Server) and POC-mode hardening as the Q3 2026 focus, followed by reliability and failure-handling hardening — schema drift, dead-letter handling, exactly-once restart-storm testing, and the Oracle go/no-go checkpoint — in Q4 2026. Prospects evaluating StreamSync today should be treated as design partners under private-beta terms, not as GA customers; SEs should confirm current beta status and any applicable design-partner agreement before setting deal-cycle expectations.

### Will StreamSync support Oracle CDC and higher sustained throughput at GA?
Oracle CDC is planned as a fast-follow after the initial GA connector set (PostgreSQL, MySQL, SQL Server), targeted for Q2 2027, contingent on a go/no-go checkpoint 90 days before GA. GA throughput commitment is sustained CDC volume of at least 50,000 change events per second per pipeline; validated support for sustained throughput beyond that threshold for high-volume customers is planned as Q2 2027 post-GA hardening work. SEs should represent Oracle support and above-50k throughput as near-term roadmap items rather than GA-day capabilities, and should validate current status before a POC that depends on either.
