# PipelineOps — Roadmap

PipelineOps has been generally available since 2024 as Fluxora's managed, lineage-aware DAG orchestration layer. This roadmap covers incremental hardening, scale validation, and cross-engine/governance depth rather than a GA milestone — the focus is on proving out enterprise-scale reliability targets, closing Airflow compatibility gaps, and extending lineage completeness across every execution surface PipelineOps orchestrates.

## Recently Shipped (Q1–Q2 2026)

**Theme: Deepening enterprise readiness for existing GA capabilities.**

- Expanded Airflow compatibility mode covering additional operator mappings, including common sensor and custom-operator patterns surfaced during enterprise migrations (Shipped)
- BYOK secrets management generally available for enterprise-tier customers, integrated with customer-managed KMS keys (Shipped)
- Dependency graph visualization improvements in the observability dashboard, including task-level drill-down (Shipped)
- Partition-aware backfill concurrency controls refined based on POC feedback from large-account backfills (Shipped)

## Q3 2026

**Theme: Validating scale ceilings and control-plane resilience for the largest accounts.**

- Large-account stress testing program to validate the 5,000-task DAG and 10,000+ concurrent task-instance targets against real enterprise workload profiles (In Progress)
- Multi-AZ control-plane failover hardening to reinforce the 99.9% uptime SLA under single-AZ failure conditions (In Progress)
- Airflow compatibility mode coverage expansion for plugin-dependent and custom-operator DAGs flagged in recent POCs (Planned)
- Connector-level lineage emission SDK for third-party REST/webhook connectors, enabling connectors to emit lineage metadata explicitly (Planned)

## Q4 2026

**Theme: Closing lineage and governance gaps across every execution engine.**

- Cross-engine lineage completeness push, extending automatic lineage capture to external-connector task types toward the 99%+ lineage coverage target (In Progress)
- Data-residency-aware storage controls for lineage and run-metadata, supporting regionally-constrained tenants without cross-region movement (Planned)
- DAG- and task-level RBAC granularity enhancements, including finer-grained connection-credential scoping (Planned)
- Airflow DAG conversion utility v2, increasing the share of DAGs that auto-migrate without manual operator remediation (Planned)

## Q1 2027

**Theme: Reliability and scale readiness for regulated, mission-critical workloads.**

- Publication of validated 5,000-task DAG / 10,000+ concurrent task-instance scale benchmarks for use in competitive RFP responses (Planned)
- Expanded failure-isolation and retry-policy templates tailored to regulated-industry SLA and audit requirements (Planned)
- Cross-region disaster recovery runbook automation to reinforce the RPO ≤15-minute / RTO ≤4-hour targets (Planned)
- Event-driven and dependency-triggered task-start latency optimization to sustain the P95 <30-second target under higher tenant concurrency (Planned)

## Q2 2027

**Theme: Broadening cross-engine orchestration reach and migration conversion tooling.**

- Expanded cross-engine connector catalog, adding integrations for additional model-serving endpoints and external systems (Planned)
- Migration conversion analytics dashboard tracking Airflow migration tooling usage through to signed multi-quarter commitments (Planned)
- Multi-environment promotion enhancements, including environment-scoped variable diffing and promotion approval workflows (Planned)
- Predictive SLA-miss alerting added to the observability dashboard, building on existing run-history and duration-trend tracking (Planned)
