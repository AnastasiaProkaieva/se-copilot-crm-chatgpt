# Deployment and Testing

## A. Personal or Pro deployment

1. Install the workflow skills you need (`fluxora-deal-brief`, `fluxora-poc-tracker`, `fluxora-discovery-prep`, `fluxora-rfp-drafting`).
2. Install `fluxora-product-knowledge`.
3. Install `fluxora-crm-capability-audit`.
4. Keep `fluxora-crm-writeback` uninstalled until write support is confirmed.
5. Connect or select **Salesforce CRM** in the conversation before a CRM-backed request.
6. Upload approved knowledge files or make them available through an approved document app.

Invoke a skill directly with `@`-mention (e.g. `@fluxora-deal-brief`); skill selection is model-driven and no skill programmatically calls another.

**Current plan note (2026-07-16):** OpenAI currently documents custom MCP connections on ChatGPT Pro as read/fetch-only. Full MCP write/modify support requires an eligible Business or Enterprise/Edu workspace. Treat this as time-sensitive and re-check before enabling writeback.

## B. Workspace Agent deployment

1. Create **Fluxora SE Copilot**.
2. Paste `agent/AGENT_INSTRUCTIONS.md` into the agent instructions.
3. Add **Salesforce CRM** under Tools.
4. Add the four core workflow skills and `fluxora-product-knowledge`.
5. Add approved knowledge files.
6. Set app writes to `Always ask` or a stricter custom approval policy.
7. Add `fluxora-crm-writeback` only after the capability audit and sandbox testing.
8. Pilot with a small SE group before workspace publication.

## C. Salesforce capability test

Run:

> Use `@fluxora-crm-capability-audit` to inspect Salesforce CRM. Do not create, update, or delete anything. Report the available actions and object-level access for the eight Fluxora objects.

Interpretation:

- `platform/sobject-reads` is read-only.
- `platform/sobject-mutations` supports create and update, not delete.
- `platform/sobject-all` supports full CRUD.
- `platform/sobject-deletes` supports delete only.

Even when Salesforce exposes mutation tools, ChatGPT plan, app action settings, published snapshots, confirmation policy, and user permissions can still prevent writes.

## D. Core regression tests

### Deal Brief — Barnett Group

Prompt:

> Use Salesforce CRM and the Deal Brief workflow. Brief me on OPP-0088. Separate CRM facts, contradictions, and recommendations.

Expected findings:

- Open Business Case Opportunity with a close date of `2026-04-07`, which is overdue on `2026-07-16`
- Two POCs for the same Opportunity
- Same sub-10-second latency criterion appears twice
- One POC is At Risk and one is Completed - Failed
- `environment stable` activity language conflicts with POC outcomes
- Snowflake TCO pressure
- Economic buyer and champions only when stakeholder relations support those roles

### POC Tracker

Prompt:

> Use Salesforce CRM. Show the POCs owned by SE-037, high risk first, and draft an internal update for the AE.

Pass criteria:

- Ownership resolved through OpportunityTeamMember or a direct POC owner field
- Sibling POCs grouped
- Evidence-backed risk reasons
- No CRM update performed

### RFP Drafting

Prompt:

> Draft answers for encryption at rest and in transit, SOC 2 Type II, and RBAC. Include source, confidence, and review status. Do not invent unsupported details.

Pass criteria:

- Approved sources or master answers used
- No unsupported security claims
- Gaps routed to an SME

### Discovery Prep

Prompt:

> Prep me for a first discovery call with an account. Separate known CRM facts from pain-point hypotheses.

Pass criteria:

- Account and contact context retrieved
- Hypotheses labeled
- Questions tailored to industry and stack
- No Account Contact treated as a confirmed opportunity stakeholder without evidence

## E. Write pilot

Run only in a sandbox after write support is confirmed.

1. Create a dedicated test record.
2. Request one low-impact field update.
3. Confirm the exact patch.
4. Verify read-after-write.
5. Inspect Salesforce audit history.
6. Test denied fields and insufficient permissions.
7. Test ambiguous record names and ensure the skill refuses to guess.

## F. Acceptance metrics

Suggested initial targets:

- 100% of live CRM claims traceable to Salesforce output
- 100% of RFP claims traceable to approved content
- Barnett regression test catches all material contradictions
- Less than 10% user correction rate during pilot
