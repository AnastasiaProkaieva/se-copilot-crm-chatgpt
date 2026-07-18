# StreamSync — PRD

Status: Draft v0.9 (Private Beta) | Stage: Private Beta, targeting GA Q1 2027 | Owner: Product Manager, StreamSync

## Problem Statement

Fluxora's Lakehouse Core has historically been strongest for batch and micro-batch ingestion. In competitive evaluations, we consistently lose or stall streaming-first deals to Confluent, which owns the mental model of "real-time data" for many engineering leaders and offers a mature Kafka-native ecosystem with well-established CDC connectors (via Kafka Connect and Confluent's managed connector catalog). Prospects tell us directly that they don't want to run a separate streaming platform (Confluent) alongside their lakehouse (Fluxora) and reconcile two systems of record, two security models, and two operational surfaces — so when streaming is a top-3 requirement, they standardize on Confluent's broader platform instead of evaluating Fluxora at all.

Design partner feedback during early private beta confirms the core pain: teams need low-latency change-data-capture (CDC) from operational databases (Postgres, MySQL, SQL Server, Oracle) directly into Lakehouse Core tables, without hand-rolling Debezium-to-Kafka-to-object-storage pipelines and without paying the operational tax of running and securing a separate event-streaming cluster. StreamSync closes this gap by making CDC and streaming ingestion a native, first-class capability of Lakehouse Core rather than a bolt-on integration.

## Target Personas

- **Head of Data Engineering** — owns the ingestion architecture and is accountable for pipeline reliability, freshness SLAs, and the total system count the team must operate. Primary economic and technical decision-maker for platform consolidation.
- **VP of Engineering** — evaluates StreamSync against build-vs-buy and platform-consolidation tradeoffs; cares about reducing the number of production systems (Kafka clusters, connector fleets) engineering must run and staff for.
- **Chief Data Officer** — sponsors multi-quarter platform commitments; cares about whether real-time data unifies with governed, auditable lakehouse data rather than creating a parallel, ungoverned "fast path."
- **Staff/Senior Data Engineer** (technical evaluator) — runs the proof-of-concept, tests CDC connector coverage, schema drift handling, exactly-once semantics, and lag/latency under production-like load; their sign-off is typically the gating factor before the deal proceeds to commercial negotiation.

## Goals

1. Deliver native, low-latency CDC ingestion from major operational databases directly into Lakehouse Core tables, eliminating the need for a separate streaming/event platform for the CDC-to-lakehouse use case.
2. Achieve sub-minute, and eventually single-digit-second, end-to-end latency from source commit to query-able lakehouse table for supported connectors.
3. Provide a unified governance, security, and lineage model so streamed data inherits the same access controls, audit trails, and catalog presence as batch-ingested data.
4. Give technical evaluators a frictionless, self-serve POC path so streaming-first deals can be won on product merit within a standard 90–180 day deal cycle.
5. Establish StreamSync as the reason a prospect can say "we don't need Confluent" for the CDC-to-analytics use case, without requiring us to match Confluent's full general-purpose event-streaming feature set.

## Non-Goals

- StreamSync is not a general-purpose event-streaming/message-broker platform. We are not building a Kafka-API-compatible pub/sub system, arbitrary topic-based messaging, or support for high-fanout event distribution to many independent consumer applications.
- StreamSync will not initially support application-level event ingestion (e.g., clickstream, IoT telemetry, custom producer SDKs). GA scope is scoped to database CDC and a small set of high-value log/event sources (see Key Requirements).
- We are not committing to feature-for-feature parity with Confluent's connector marketplace (120+ connectors) at GA; we are committing to depth and reliability on the highest-demand operational database sources.
- StreamSync will not replace Fluxora's existing batch ingestion tooling; it is additive, targeting a workload class batch ingestion serves poorly today.
- No commitment at GA to multi-region active-active streaming topologies; single-region with cross-region replication of resulting lakehouse tables is out of scope for v1.

## Key Requirements

1. **Native CDC connectors** for PostgreSQL, MySQL, and SQL Server at GA (Oracle as a fast-follow), using log-based capture (WAL/binlog/CDC tables) rather than polling, to minimize source-database load and capture latency.
2. **Direct-to-lakehouse write path**: captured changes land as append/merge operations directly into Lakehouse Core tables (via the existing table format's transaction log), with no intermediate broker or object-storage staging step exposed to the user.
3. **Schema drift handling**: automatic detection and propagation of source schema changes (column add/drop/rename, type widening) into the target table schema, with configurable policies (auto-evolve vs. quarantine-and-alert) rather than silent pipeline failure.
4. **Exactly-once delivery semantics** end-to-end, with idempotent apply and checkpointing, so replays or connector restarts never produce duplicate or lost rows in the target table.
5. **Initial snapshot + incremental CDC**: a StreamSync pipeline must be able to perform a consistent initial full-table snapshot and then seamlessly transition to streaming incremental changes without manual coordination or downtime on the source.
6. **Unified catalog and lineage integration**: every StreamSync pipeline and target table is automatically registered in Fluxora's data catalog with source-to-target lineage, so streamed tables are discoverable and auditable identically to batch tables.
7. **Pipeline observability**: built-in dashboards and alerting for replication lag (source-commit-to-lakehouse-visible), throughput, error/dead-letter rates, and connector health, exposed via the same monitoring surface used for batch pipelines.
8. **Self-serve POC mode**: a scoped, time-boxed private-beta deployment mode that lets a technical evaluator stand up a source connection and validate latency/throughput against their own data within a single working session, without SE-assisted backend configuration.
9. **Dead-letter and error handling**: malformed or unprocessable change events are routed to a dead-letter queue with inspectable payloads and a replay mechanism, rather than blocking the pipeline or being silently dropped.
10. **Backpressure-aware autoscaling**: ingestion compute scales with source change volume within configured bounds, and applies backpressure toward the source connector (not silent buffering-until-OOM) when downstream write capacity is constrained.

## Non-Functional Requirements

- **Latency**: p50 source-commit-to-queryable latency ≤ 60 seconds at private beta; target p50 ≤ 10 seconds and p99 ≤ 60 seconds at GA for supported connectors, under design-partner-representative load.
- **Throughput & scale**: support sustained CDC volumes of at least 50,000 change events/sec per pipeline at GA, with horizontal scaling of ingestion workers independent of Lakehouse Core compute.
- **Availability**: StreamSync ingestion control plane targets 99.9% availability; a connector or worker failure must trigger automatic restart from last checkpoint with no manual intervention and no data loss.
- **Security**: all data in transit (source-to-StreamSync, StreamSync-to-lakehouse) encrypted via TLS 1.2+; credentials for source database connections stored in Fluxora's managed secrets vault, never persisted in pipeline configuration; support for private connectivity (VPC peering / PrivateLink-equivalent) so source databases are never exposed to the public internet.
- **Access control**: CDC pipelines and target tables are subject to Fluxora's existing role-based access control and column-level masking policies; no bypass path that exposes raw change events outside governed access.
- **Auditability & compliance**: full audit log of pipeline configuration changes, connector credential rotations, and schema-evolution decisions, retained per Fluxora's standard compliance retention policy; supports customer needs under SOC 2 Type II and, where applicable, HIPAA/GDPR data-handling commitments already covered by Fluxora's platform-level certifications.
- **Multi-tenancy & isolation**: per-customer pipeline compute and network isolation consistent with Lakehouse Core's existing tenant isolation model; no shared connector infrastructure across customer boundaries.
- **Disaster recovery**: checkpoint state and pipeline configuration are durably persisted and recoverable such that a regional infrastructure failure results in bounded data loss (RPO ≤ 5 minutes) and defined recovery time (RTO ≤ 30 minutes) at GA.

## Competitive Positioning

Confluent's core value proposition is a general-purpose, Kafka-native event-streaming platform: broad connector marketplace, topic-based pub/sub for many downstream consumers, and deep support for application-level event architectures. That breadth is real, but it comes with a cost most of our target buyers explicitly want to avoid: running and securing a second production system, staffing Kafka operational expertise, and building a separate pipeline to land streaming data into an analytics-ready lakehouse table.

StreamSync's positioning is not "Kafka, but from Fluxora." It is: *if your primary goal is getting change data from operational databases into governed, query-ready lakehouse tables in near real time, StreamSync gets you there with one system, one security model, and one catalog — instead of two.* Where Confluent requires stitching a broker, a set of Kafka Connect connectors, and a separate sink/ETL step into the lakehouse, StreamSync collapses that into a single managed pipeline with direct-to-table writes, native schema evolution, and lineage that's already integrated with the rest of Fluxora.

We should expect Confluent to be positioned as more mature and broader in connector catalog breadth and general-purpose event-streaming use cases (arbitrary pub/sub, high-fanout consumers, application event backbones) — we do not contest that at GA. Our contest is narrower and sharper: for the CDC-to-lakehouse workload specifically, StreamSync should deliver faster time-to-first-query than a comparable Confluent-plus-sink-connector-plus-lakehouse-load architecture, with materially less operational surface area for the customer's platform team to run. Where prospects need both governed analytics and general event streaming, we should be honest that a Confluent-plus-Fluxora coexistence pattern remains viable — but StreamSync should win the CDC-to-analytics slice of that architecture outright, and in accounts where CDC-to-lakehouse is the whole use case, StreamSync should let us win the deal without Confluent in the stack at all.

SEs should avoid claiming specific Confluent benchmark numbers (throughput, latency, pricing) since we do not have verified, current figures from Confluent's own materials; keep comparisons directional and architecture-based rather than stat-for-stat.

## Success Metrics

- **Private beta → GA conversion**: number and % of design partners who move from private beta usage to a paid production StreamSync commitment at GA.
- **Win rate on streaming-flagged deals**: change in win rate for opportunities where the prospect explicitly named streaming/CDC as a top-3 requirement, pre- vs. post-GA.
- **Confluent displacement/coexistence rate**: % of closed-won StreamSync deals where Confluent was a named incumbent or competing bid, and of those, % won as an outright displacement vs. a coexistence architecture.
- **POC-to-close cycle time**: median days from POC kickoff to closed-won for opportunities where StreamSync was evaluated, target materially shorter than the current 90–180 day baseline for streaming-flagged deals.
- **Pipeline reliability in production**: post-GA customer pipelines meeting the p50/p99 latency SLOs defined in Non-Functional Requirements, measured monthly across the install base.
- **Design partner NPS/CSAT**: qualitative and quantitative satisfaction score from private beta design partners, tracked through GA transition.
- **Attach rate**: % of new Lakehouse Core logos that adopt StreamSync within their first two quarters, as a proxy for platform-consolidation value realized.

## Risks & Open Questions

- **Connector coverage gap at GA**: if Oracle and other high-demand sources slip past GA, we risk losing deals where the operational database mix doesn't match our launch connector set. Need a firm go/no-go checkpoint on Oracle CDC scope 90 days before GA.
- **Latency target credibility**: our public-facing latency claims (p50 ≤ 10s) must be validated under design-partner production load, not synthetic benchmarks, before we let field/marketing use them in competitive comparisons — premature claims that don't hold up in a POC will damage credibility more than having no claim at all.
- **"CDC-only" scope may not be enough for some evaluators**: some Staff/Senior Data Engineer evaluators running POCs may test general event-streaming use cases (not just CDC) because that's what they assume "streaming" means; we need clear POC scoping conversations up front so evaluations aren't graded against non-goals.
- **Coexistence vs. displacement messaging risk**: over-claiming full Confluent replacement in accounts with broad event-streaming needs could set up an unwinnable technical evaluation; SE enablement needs clear guidance on when to pitch displacement vs. coexistence.
- **Operational load on source databases**: log-based CDC is lower-impact than polling, but design partners with high-write-volume production databases have raised concerns about WAL/binlog retention pressure and source-side resource consumption; needs explicit guidance and guardrails before GA.
- **Exactly-once guarantee under connector restart storms**: edge cases during rapid, repeated connector restarts (e.g., during a source failover) need more adversarial testing to confirm the exactly-once guarantee holds, not just single-restart scenarios.
- **Pricing model undecided**: whether StreamSync is priced as a StreamSync-specific throughput/volume metric, bundled into existing Lakehouse Core compute pricing, or some hybrid, is still open and has direct implications for the "consolidation saves money" pitch versus Confluent's pricing model.
- **GA date risk**: Q1 2027 is the headline roadmap commitment communicated to prospects in active deal cycles; any slip has direct pipeline impact on deals currently being held open pending GA, and needs early, proactive tracking against the connector-coverage and latency-validation risks above.
