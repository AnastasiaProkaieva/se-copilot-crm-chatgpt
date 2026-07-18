# Lakehouse Core — Technical FAQ

## Architecture & Deployment

### What is Lakehouse Core, architecturally?
Lakehouse Core is an object-storage-backed, ACID-compliant table format and transaction layer that sits directly on customer-owned cloud object storage (S3, GCS, or Azure Blob). It is composed of a metadata/control plane that manages table snapshots, schema, and transaction coordination, and a data plane that stores the actual table files in the customer's own storage account. There is no proprietary storage engine underneath — Fluxora manages the transactional metadata; the customer's cloud provider owns the underlying bytes and their durability guarantees.

### Does Lakehouse Core require a proprietary storage engine or data format the customer can't leave?
No. Table data is written in an open, interoperable metadata format designed to be readable by third-party query engines (e.g., Spark, Trino, Presto) without proprietary connectors. This is a deliberate design principle, not a compatibility afterthought — it's central to how Lakehouse Core differentiates against both Delta Lake and Snowflake's storage layer (see Competitive Differentiation below).

### What deployment models does Lakehouse Core support — can it run on-premises or air-gapped?
Lakehouse Core targets customer cloud accounts on major public cloud object storage (AWS, GCP, Azure). There is currently no committed support for on-premises or air-gapped deployments in the active roadmap — if a prospect requires that, flag it early as a gap rather than implying a workaround exists.

### What scale and concurrency can Lakehouse Core actually support per table?
Individual tables are designed to scale to tens of billions of rows and petabyte-scale storage without manual repartitioning or degraded write throughput. Concurrency-wise, Lakehouse Core supports hundreds of concurrent readers and dozens of concurrent writers per table using optimistic concurrency control with bounded retry/backoff on write conflicts. Metadata resolution for table snapshot lookups is sub-second at 100K+ partition scale; validating that performance beyond the current 100K-partition benchmark is active roadmap work for Q1 2027, so if a POC pushes meaningfully past that scale, set expectations that we're actively hardening (not yet fully validated) at that ceiling.

## Security & Compliance

### How is data encrypted and how does identity/access management integrate with our existing stack?
Encryption at rest (with customer-managed key support) and in transit is on by default. Identity federation integrates with customer identity providers via SAML/OIDC, so access control rides on the customer's existing IdP rather than a Fluxora-specific identity silo.

### How granular is access control, and is it consistent across query engines?
Lakehouse Core supports row-level and column-level security policies enforced at the table layer, meaning the same policy applies regardless of whether the table is queried through Spark, Trino, or Fluxora's native query layer. Consistency fixes to that cross-engine enforcement behavior shipped in the Q1–Q2 2026 hardening cycle, specifically closing gaps where policy enforcement could diverge by engine.

### What compliance certifications does Lakehouse Core currently hold, and what's in progress?
SOC 2 Type II control mapping across schema-change, access-grant, and row/column-policy audit logging was refreshed and shipped in the Q1–Q2 2026 cycle. A GDPR right-to-erasure workflow — including automated vacuum confirmation for targeted row deletion — is in progress and targeted for Q3 2026. HIPAA-eligible configuration work is also in progress, but it has not yet gone through independent third-party audit; do not represent HIPAA as a completed certification in any customer-facing conversation or RFP response until that audit formally closes (currently targeted for Q2 2027).

## Integration & Interoperability

### Can we point our existing Spark/Trino/Presto tooling directly at Lakehouse Core tables without a Fluxora-specific connector?
Yes — table metadata is exposed in an open format that conformant third-party engines can read natively, without requiring proprietary Fluxora connectors. This is a core requirement of the product, not a bolt-on: the goal is that customers can multi-tool across engines against the same physical tables. Note that engine-level performance can vary; see the Competitive Differentiation section for how we frame multi-engine parity honestly.

### Does Lakehouse Core support change data capture (CDC) for downstream pipelines and feature stores?
Yes. Each table emits a consumable change feed (inserts/updates/deletes) so downstream pipelines and ML feature stores can subscribe incrementally rather than re-scanning full tables. An initial hardening pass addressing a subset of previously identified CDC edge cases under high-cardinality schema evolution shipped in Q1–Q2 2026, with continued hardening for the remaining edge cases in progress for Q4 2026. If a prospect has a CDC-heavy use case with frequent schema changes, it's fair to say this is an actively-hardened area rather than a fully closed one.

## Competitive Differentiation

### How does Lakehouse Core differ from Databricks and Delta Lake?
Delta Lake pioneered ACID transactions on object storage and remains the incumbent there, but it performs best — and gets its most advanced features like liquid clustering and deep optimization — when run through the Databricks compute runtime. Lakehouse Core's differentiation is that engine-agnosticism is a first-class design principle: customers can point Spark, Trino, or Fluxora's own query layer at the same tables without routing through a single vendor's compute to get full feature parity. In practice, this shows up in POCs as faster time-to-first-query in multi-engine environments and lower operational overhead for customers who don't want their transactional table layer coupled to one company's compute pricing. Being candid with technical evaluators: we are still closing performance gaps on non-Fluxora engines (Trino/Presto read-path optimization work is in progress for Q4 2026), so frame this as "architecturally engine-agnostic, with active investment in closing the last-mile performance gap" rather than "already at parity everywhere."

### How does Lakehouse Core differ from Snowflake's storage layer?
Snowflake's storage layer is proprietary and is only fully accessible through Snowflake compute — even "external tables" don't fully escape that constraint, so data effectively lives inside Snowflake's format. That's a durable lock-in vector that tends to surface at renewal time. Lakehouse Core's core pitch is openness: data lives in the customer's own object storage, in an open table format, readable by any conformant engine, so a future switch or multi-tooling decision doesn't require a re-platforming project. For CDOs and VPs of Engineering weighing a multi-quarter commitment, the framing is platform risk reduction — Fluxora doesn't need to be "the last vendor standing" for the customer's data to stay usable.

## Pricing & Licensing

### How is Lakehouse Core priced relative to running a warehouse and a lake separately?
The commercial pitch is built around eliminating the "two-copy tax": today, many customers pay for duplicated storage and duplicated compute to maintain a warehouse copy (for BI) and a lake copy (for ML/ELT) of the same data, plus the reconciliation overhead of keeping them in sync. Lakehouse Core consolidates that into a single object-storage-backed copy that serves both BI-grade and ML workloads, so the pricing conversation should center on storage consolidation ratio and total infrastructure spend versus the incumbent warehouse-plus-lake setup, not a like-for-like feature-for-feature price comparison.

### What should I tell a prospect who wants precise cross-region replication cost estimates for an RFP?
Be transparent that current pricing guidance for cross-region replication is not yet granular enough to produce a confident, itemized cost model for RFP purposes — this is a known internal gap, not something to paper over with an estimate. A dedicated cross-region replication cost estimator is planned for Q4 2026 specifically to give enterprise DR evaluators more precise guidance. Until that ships, loop in Product Marketing and Finance for a custom estimate rather than quoting standardized figures.

## Roadmap

### Is there a zero-copy migration path for customers already committed to Iceberg or Delta Lake?
Not yet — this is a known gap. Customers already standardized on a competing open table format currently face real conversion cost, which is an open risk area for deal velocity even when long-term TCO favors Lakehouse Core. A zero-copy, in-place format conversion path is planned for Q1 2027 to reduce that migration friction, but it should be discussed as a roadmap item, not something available to POC against today.

### Can I tell a customer HIPAA-eligible configuration is fully certified?
No — be precise here. HIPAA-eligible configuration support is actively being built and is roadmapped toward a third-party audit targeted for completion in Q2 2027, but it has not been independently audited yet. It's accurate to say Fluxora is actively investing in HIPAA-eligible configuration ahead of that audit; it is not accurate to represent it as a completed certification in any customer-facing or RFP context until the audit formally closes.
