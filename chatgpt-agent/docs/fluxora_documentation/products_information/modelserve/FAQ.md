# ModelServe — Technical FAQ

## Architecture & Deployment

### Do we need to manage our own containers, autoscalers, or load balancers to serve a model?
No. ModelServe supports one-click deployment of models packaged as ONNX, PMML, or standard Python model artifacts to a managed serving endpoint via CLI, API, or console — customers don't write Dockerfiles or manage container orchestration directly. This is a deliberate design goal: teams that have already standardized on Fluxora for storage and pipelines shouldn't need to stand up or operate a second infrastructure surface just to serve models.

### How do canary rollouts and rollback work in ModelServe?
ModelServe supports traffic-percentage-based canary releases (e.g., 5% → 25% → 100%) with configurable success criteria — latency, error rate, or custom business metrics — and automatic rollback if those thresholds are breached. A single logical endpoint can host multiple concurrently deployed model versions, which also enables A/B testing and shadow traffic (shadow traffic support for multi-version endpoints shipped in the Q1–Q2 2026 hardening cycle) alongside canary promotion. Any deployed version can be reverted to the prior known-good version via a single API call or console action, and rollback is designed to begin serving 100% of traffic on the reverted version within 60 seconds of initiation.

### How does autoscaling handle spiky or high-volume inference traffic?
Endpoints scale horizontally based on request volume and queue depth, with a configurable minimum warm-instance count so latency-sensitive workloads aren't exposed to cold-start spikes. The platform is designed to scale a single endpoint from zero to at least 10,000 requests/second within defined autoscaling policy windows without manual intervention, and the serving layer overhead itself is bounded — P99 latency added by ModelServe (excluding model compute time) should not exceed 10ms for feature-lookup-enabled endpoints under normal load. Validating autoscaling behavior at 10,000+ rps with refined cold-start mitigation is active, in-progress work for Q3 2026, so for very high-throughput POCs it's worth setting expectations that this is an area of continued hardening rather than a fully closed-out capability.

## Security & Compliance

### How is inference traffic and stored data encrypted, and can we use our own keys?
All inference traffic is encrypted in transit using TLS 1.2+. Model artifacts and any logged inference data at rest are encrypted using the same key management infrastructure as Lakehouse Core. Customer-managed encryption key (CMEK) support for model artifacts and logged inference data has shipped as part of the recent post-GA hardening cycle, so customers who require CMEK for Lakehouse Core can extend that same control to ModelServe.

### What compliance certifications and audit logging does ModelServe provide?
ModelServe inherits Fluxora's existing platform compliance certifications — SOC 2 Type II and ISO 27001 — rather than requiring a separate attestation. All deployment, rollout, and access-control actions are audit-logged, and those logs are retained and exportable to satisfy SOC 2 Type II control requirements. Serving endpoints and logged inference data also respect the same regional data residency boundaries already configured for the customer's Lakehouse Core deployment, so residency posture doesn't need to be reconfigured separately for the serving layer.

### How granular is RBAC on ModelServe endpoints today?
Today, endpoint creation, promotion, and traffic-shifting actions are gated by Fluxora's existing RBAC model, which lets data engineering, ML, and platform teams have distinct permission boundaries at the endpoint level. Finer-grained, per-model-version permissions — relevant for larger enterprises with strict segregation-of-duties requirements between ML and platform teams — are planned, with design work scheduled to begin in Q3 2026; that design work has not started yet and the capability is not yet generally available. See the Roadmap section below for timing.

## Integration & Interoperability

### Which model formats and frameworks does ModelServe support?
ModelServe supports deployment of models packaged in ONNX, PMML, and standard Python model artifact formats today. Expanded model packaging support for additional LLM-serving runtimes is in progress for Q3 2026. If a prospect's ML team is standardized on a framework or LLM-serving runtime outside these formats, that should be flagged and confirmed against current coverage before making any commitment in a POC or RFP.

### How does ModelServe access Lakehouse Core feature data at inference time, and how does it prevent online/offline skew?
Serving endpoints can reference Lakehouse Core feature tables directly by name at inference time, with automatic point-in-time consistency so the features available online match what the model was trained against. This is what eliminates the custom feature-fetching glue code teams typically have to write and maintain when serving is decoupled from the feature store. Because feature lookups depend on Lakehouse Core's own read latency under high concurrent load, continued performance hardening at scale is an active investment area (feature-lookup latency hardening under high concurrent load is in progress for Q3 2026) to keep the P99 10ms overhead budget intact as usage grows.

### Can we log inference requests/responses back into Lakehouse Core, and what drift detection is available?
Yes — every inference request/response pair can optionally be logged back into Lakehouse Core for downstream monitoring. Baseline feature and prediction drift detection, surfaced to the customer's existing observability tooling, shipped as a beta capability in the recent hardening cycle. Expanded drift detection coverage with additional statistical and model-based detection methods is in progress with planned GA in Q1 2027, so today's drift signals should be positioned as a solid starting point rather than a full replacement for a mature third-party MLOps drift solution a customer may already run.

## Competitive Differentiation

### How is ModelServe different from Databricks Model Serving?
Databricks requires customers to move model artifacts and feature-serving logic into its own serving construct, which typically means duplicating feature engineering logic that already lives in the Databricks feature store or lakehouse layer. ModelServe is natively wired to the same Lakehouse Core feature tables customers already query for analytics and pipeline work, so there's no separate feature-serving abstraction to configure or keep in sync. For customers already standardized on Fluxora for storage and pipelines, the win is fewer moving parts and lower risk of online/offline feature skew — not a claim that ModelServe is categorically faster or more scalable than Databricks. Lead with "one platform, one feature source of truth," not raw latency or scale claims, since Databricks is credible on both.

### How does ModelServe compare to Amazon SageMaker?
SageMaker is a strong, general-purpose serving product, but it's decoupled from any specific lakehouse or feature-store layer by design — customers typically build a custom bridge between S3/Redshift/whatever warehouse they use and SageMaker endpoints. ModelServe's edge is faster time-to-first-deployment specifically for customers already running Lakehouse Core, because there's no custom integration layer to build between storage and serving. Be careful not to position ModelServe as a general replacement for SageMaker's broader ecosystem — built-in algorithms, a model marketplace, and multi-cloud portability aren't things ModelServe is trying to match. The win condition is consolidating the data + serving stack on Fluxora, not offering a cloud-agnostic, storage-agnostic serving layer.

## Pricing & Licensing

### How is ModelServe priced relative to Lakehouse Core?
ModelServe's autoscaling-based compute consumption for serving is metered and priced separately from Lakehouse Core's storage/compute pricing — it is not simply bundled into existing Lakehouse Core spend. Because this is a distinct usage-based line item, SEs should loop in the pricing/deal desk for exact rate card and packaging details during a deal cycle rather than quoting specific figures, and should proactively flag to CDOs evaluating multi-quarter TCO that ModelServe compute is tracked and billed separately from storage/pipeline compute.

### Can customers get visibility into ModelServe compute spend for chargeback or showback?
Not yet in a dedicated, purpose-built form. A serving cost and usage visibility dashboard aimed at giving CDOs clearer total-cost-of-ownership tracking for autoscaling-based compute is planned for Q4 2026, with GA of that dashboard — including chargeback/showback reporting — planned for Q2 2027. Until then, this should be positioned as a near-term roadmap commitment rather than a shipped capability.

## Roadmap

### Is per-model-version RBAC available today, and when is it coming?
Not yet. Today, RBAC gates endpoint-level actions — creation, promotion, and traffic-shifting. Per-model-version RBAC design work, aimed at segregation of duties between ML and platform teams, is planned for Q3 2026 (design has not yet started), with general availability planned for Q4 2026. It's fair to tell prospects this is a committed near-term roadmap item, while being clear it isn't available today, design work hasn't kicked off yet, and "planned" timing can shift.

### What's the roadmap for closing model-format gaps and hardening feature-lookup performance at scale?
Q3 2026 is focused on exactly these two areas: feature-lookup latency hardening under high concurrent load (to protect the P99 10ms serving-overhead budget as usage scales) and expanded model packaging support for additional LLM-serving runtimes alongside the existing ONNX, PMML, and standard Python artifact support — both currently in progress. Validated autoscaling to 10,000+ rps with refined cold-start mitigation is also in progress in the same window. SEs should frame these as active engineering investments with a clear direction, and confirm any prospect-specific framework or scale requirement against current coverage before making a POC commitment.
