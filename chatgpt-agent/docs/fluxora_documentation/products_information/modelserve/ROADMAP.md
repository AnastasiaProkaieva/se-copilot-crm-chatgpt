# ModelServe — Roadmap

ModelServe has been generally available since 2025, giving customers native, low-latency model serving wired directly to Lakehouse Core feature data. This roadmap covers incremental hardening and scale work rather than a GA milestone: deepening feature-lookup performance at scale, closing framework/format gaps, maturing drift detection, and sharpening the governance and rollout controls enterprise buyers need to standardize on ModelServe as the system of record for production model traffic.

## Recently Shipped (Q1–Q2 2026)
Theme: Post-GA hardening of rollout and data-protection fundamentals.
- Shadow traffic support for multi-version endpoints, enabling pre-promotion validation alongside canary rollouts (Shipped)
- Customer-managed encryption key (CMEK) support for model artifacts and logged inference data (Shipped)
- Point-in-time feature lookup performance tuning under higher concurrency (Shipped)
- Drift detection beta: baseline feature and prediction drift signals surfaced to customer observability tooling (Shipped)

## Q3 2026
Theme: Protecting the latency budget and closing format gaps as usage scales.
- Feature-lookup latency hardening under high concurrent load to keep serving-layer overhead within the P99 10ms budget at scale (In Progress)
- Expanded model packaging support for additional LLM-serving runtimes alongside ONNX, PMML, and standard Python artifacts (In Progress)
- Validated autoscaling to 10,000+ requests/second with refined cold-start mitigation for latency-sensitive endpoints (In Progress)
- Per-model-version RBAC permissions design for segregation-of-duties between ML and platform teams (Planned)

## Q4 2026
Theme: Enterprise-grade governance and rollout confidence.
- General availability of per-model-version RBAC granularity (Planned)
- Expanded drift detection coverage with additional statistical and model-based detection methods (In Progress)
- Custom business-metric success-criteria library for canary rollouts, reducing manual threshold configuration (Planned)
- Serving cost and usage visibility dashboard giving CDOs clearer total-cost-of-ownership tracking for autoscaling-based compute consumption (Planned)

## Q1 2027
Theme: Resilience and deeper observability for multi-quarter production commitments.
- Cross-region failover hardening for serving endpoints within a customer's existing Fluxora deployment footprint (Planned)
- General availability of expanded drift detection (statistical + model-based signals) (Planned)
- Shadow traffic analytics enhancements to strengthen pre-promotion validation signal quality (Planned)
- Audit log export enhancements supporting continuous SOC 2 Type II compliance workflows (Planned)

## Q2 2027
Theme: Automating safe rollouts and cost transparency at enterprise scale.
- Automated canary success-criteria recommendations derived from historical rollout outcomes (Planned)
- Autoscaling policy improvements for sustained spiky, multi-tenant workloads at 10,000+ rps (Planned)
- General availability of the serving cost and usage dashboard with chargeback/showback reporting (Planned)
- Continued model-format and runtime coverage expansion based on POC and design-partner feedback (Planned)
