# ModelServe — PRD
Status: Approved (Active Development) | Stage: GA (since 2025) | Owner: Product Manager, ModelServe

## Problem Statement

Teams building AI/ML pipelines on Fluxora can already train, transform, and curate feature data in Lakehouse Core — but historically had to export models to a separate serving stack to put them into production. That hop introduces three recurring problems for our buyers: (1) feature-serving skew, where the features computed offline in the lakehouse don't match what's available at inference time; (2) operational overhead, since data engineering teams end up owning a second infrastructure surface (containers, autoscalers, load balancers) just to serve models; and (3) slow, risky rollouts, because promoting a new model version to production traffic is often a manual, all-or-nothing cutover.

ModelServe closes this gap by making low-latency model serving a native capability of the Fluxora platform, directly wired to Lakehouse Core feature data, so customers who have already standardized on Fluxora for storage and pipelines don't need to stand up or evaluate a separate serving product.

## Target Personas

- **Head of Data Engineering** — owns the team responsible for keeping feature pipelines and serving infrastructure reliable in production; cares about operational burden and on-call load.
- **VP of Engineering** — owns the multi-quarter platform decision and cross-team roadmap; cares about consolidating vendor surface area and reducing integration risk.
- **Chief Data Officer** — owns the business case for AI/ML initiatives; cares about time-to-value and defensible governance/compliance posture for models in production.
- **Staff/Senior Data Engineer** (technical evaluator) — runs the POC; cares about latency numbers, rollout controls, API ergonomics, and how much glue code is needed to integrate with existing feature pipelines.

## Goals

1. Let customers deploy a trained model to a low-latency serving endpoint without leaving the Fluxora platform or provisioning separate serving infrastructure.
2. Give Staff/Senior Data Engineers native access to Lakehouse Core feature tables at inference time, eliminating custom feature-fetching glue code.
3. Make canary and staged rollouts a first-class, low-risk operation so teams can promote new model versions with confidence and fast rollback.
4. Provide autoscaling that tracks real traffic patterns so Heads of Data Engineering aren't manually managing capacity for spiky inference workloads.
5. Give VPs of Engineering and CDOs the observability and governance controls needed to treat ModelServe as the system of record for production model traffic.

## Non-Goals

- ModelServe is not a model training or experiment-tracking product; training remains the responsibility of upstream tooling (including third-party frameworks) that feed into Fluxora.
- ModelServe does not aim to support arbitrary batch scoring workloads at large scale — that use case is addressed by Lakehouse Core pipeline jobs, not the low-latency serving path.
- ModelServe is not pursuing edge/on-device deployment in this roadmap window; scope is cloud-hosted serving within the customer's Fluxora deployment footprint.
- ModelServe does not include a built-in feature store authoring UI — feature definitions and transformations remain owned by Lakehouse Core.

## Key Requirements

1. **One-click model deployment**: Support deployment of models packaged in common formats (ONNX, PMML, and standard Python model artifacts) to a managed serving endpoint via CLI, API, or console, without requiring customers to write Dockerfiles or manage container orchestration directly.
2. **Native Lakehouse Core feature lookup**: Serving endpoints must be able to reference Lakehouse Core feature tables directly by name at inference time, with automatic point-in-time consistency so online features match what the model was trained against.
3. **Canary rollouts with automated rollback**: Support traffic-percentage-based canary releases (e.g., 5% → 25% → 100%) with configurable success criteria (latency, error rate, custom business metrics) and automatic rollback if thresholds are breached.
4. **Autoscaling with cold-start mitigation**: Endpoints must scale horizontally based on request volume and queue depth, with a configurable minimum warm-instance count to avoid cold-start latency spikes for latency-sensitive workloads.
5. **Multi-version endpoint support**: A single logical endpoint must support multiple concurrently deployed model versions, enabling A/B testing and shadow traffic in addition to canary rollout.
6. **Request/response logging and drift signals**: Every inference request/response pair must be optionally logged back into Lakehouse Core for downstream monitoring, with built-in feature and prediction drift detection surfaced to the customer's observability tooling.
7. **Role-based access control on endpoints**: Endpoint creation, promotion, and traffic-shifting actions must be gated by Fluxora's existing RBAC model, so that data engineering, ML, and platform teams can have distinct permission boundaries.
8. **Programmatic and low-code rollback**: Any deployed version must be revertible to the prior known-good version via a single API call or console action, with rollback completing within the platform's defined SLA (see Non-Functional Requirements).

## Non-Functional Requirements

- **Latency**: P99 inference latency overhead introduced by ModelServe's serving layer (excluding model compute time) must not exceed 10ms for feature-lookup-enabled endpoints under normal load.
- **Availability**: Serving endpoints must meet a 99.95% uptime SLA per region, consistent with Fluxora's platform-wide production SLA commitments.
- **Rollback speed**: Rollback to a prior model version must complete and begin serving 100% of traffic on the reverted version within 60 seconds of initiation.
- **Scalability**: Must support scaling a single endpoint from zero to at least 10,000 requests/second within defined autoscaling policy windows, without manual intervention.
- **Security**: All inference traffic must be encrypted in transit (TLS 1.2+); model artifacts and logged inference data at rest must be encrypted using the same key management infrastructure as Lakehouse Core, including support for customer-managed encryption keys (CMEK).
- **Data residency**: Serving endpoints and any logged inference data must respect the same regional data residency boundaries configured for the customer's Lakehouse Core deployment.
- **Compliance**: Audit logging of all deployment, rollout, and access-control actions must be retained and exportable to satisfy SOC 2 Type II control requirements; ModelServe inherits the platform's existing compliance certifications (SOC 2 Type II, ISO 27001) rather than requiring a separate attestation.
- **Multi-tenancy isolation**: Endpoint compute and traffic must be logically isolated per customer tenant, with no shared inference queues across tenants.

## Competitive Positioning

**Vs. Databricks Model Serving**: Databricks requires customers to move model artifacts and feature-serving logic into its own serving construct, which typically means duplicating feature engineering logic that already lives in the Databricks feature store or lakehouse layer. ModelServe's differentiation is that it is natively wired to the same Lakehouse Core feature tables customers already query for analytics and pipeline work — there is no separate feature-serving abstraction to configure or keep in sync. For customers already standardized on Fluxora for storage and pipelines, this means fewer moving parts and less risk of online/offline feature skew, rather than asking teams to learn and maintain a second feature-serving layer.

**Vs. Amazon SageMaker (Inference/Endpoints)**: SageMaker is a strong general-purpose serving product, but it is decoupled from any specific lakehouse or feature-store layer by design — customers bring their own feature pipeline integration, which is typically a custom-built bridge between S3/Redshift/whatever warehouse they use and SageMaker endpoints. ModelServe's positioning is faster time-to-first-deployment for customers who are already running Lakehouse Core, because there is no custom integration layer to build between storage and serving. We should not claim ModelServe is a general replacement for SageMaker's broader ecosystem (built-in algorithms, marketplace models, multi-cloud portability) — the win condition is specifically for customers consolidating their data + serving stack on Fluxora, not for customers who want a cloud-agnostic, storage-agnostic serving layer.

**General framing for SEs**: Lead with "one platform, one feature source of truth" rather than raw latency or scale claims, since Databricks and SageMaker are both credible at scale. The differentiated wedge is integration depth with Lakehouse Core and the operational simplicity of not running a second serving stack — this resonates most with Heads of Data Engineering and VPs of Engineering who are evaluating total platform surface area, not just serving performance.

## Success Metrics

- % of Lakehouse Core customers with an active ML workload who adopt ModelServe within 2 quarters of GA (adoption/attach rate).
- Median time from "model artifact ready" to "serving 100% production traffic" for new customer deployments (time-to-production).
- P99 serving latency and endpoint availability against SLA, tracked per customer tier.
- % of production model promotions that use canary rollout (vs. direct full-traffic deploy), as a proxy for safe-rollout adoption.
- Rollback frequency and mean-time-to-rollback, as a proxy for platform trust and safety-net effectiveness.
- Net-new competitive win rate in deals where ModelServe was cited as a differentiator against Databricks or SageMaker in the POC.

## Risks & Open Questions

- **Feature-lookup latency at scale**: Native Lakehouse Core feature lookups at inference time are a core differentiator, but they introduce a dependency on Lakehouse Core's own read latency under high concurrent load; we need continued hardening to ensure this doesn't erode the P99 latency budget as usage scales.
- **Multi-cloud/hybrid deployments**: Customers running Lakehouse Core across multiple regions or clouds may expect ModelServe endpoints to be deployable with similar flexibility; current scope assumes serving co-located with the customer's primary Fluxora deployment footprint, which may not satisfy all enterprise topologies.
- **Framework/format coverage**: Model packaging support (ONNX, PMML, standard Python artifacts) may not cover every framework a given customer's ML team uses (e.g., certain LLM-serving runtimes); gaps here could push technical evaluators back toward SageMaker or Databricks during POCs.
- **Drift detection maturity**: Built-in drift signals are a stated requirement, but the sophistication of out-of-the-box detection (vs. what customers may already have via third-party MLOps tooling) is still being validated with design partners; risk of being perceived as "checkbox" drift detection rather than a differentiator.
- **Pricing model clarity**: Autoscaling-based compute consumption for serving is priced differently from Lakehouse Core's storage/compute pricing; open question on how clearly this is communicated to CDOs evaluating total cost of ownership during multi-quarter deal cycles.
- **RBAC granularity**: Current RBAC integration covers endpoint-level actions; open question on whether finer-grained (e.g., per-model-version) permissions are needed for larger enterprise customers with strict segregation-of-duties requirements between ML and platform teams.
