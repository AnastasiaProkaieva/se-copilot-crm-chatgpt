# Fluxora SE Copilot — Demo Prompt Library

Sample prompts for demonstrating the Fluxora SE Copilot against the
Salesforce org. Every prompt below was **ground-verified against the live org**:
its supporting query was executed and confirmed to return a *tight, legible*
result — never zero rows, never a 300+ row firehose. The specific record names,
IDs, and dollar figures cited are real as of the verification date and chosen so
each prompt lands cleanly in a live demo.

---

## How to read this file

Each prompt lists:

- **Skills** it exercises (see `chatgpt-agent/skills/`).
- **Tools** beyond the CRM (web search, memory, taxonomy) where relevant.
- **Lands on** — the verified real result, so you know what to expect on stage.
- **Demo note** — any caveat to steer around during a live run.

Skills referenced:

| Skill | Purpose |
|---|---|
| `fluxora-discovery-prep` | Discovery-call prep, account research, pain hypotheses, questions |
| `fluxora-deal-brief` | Live-deal posture, stakeholders, stage/close review, risk, next moves |
| `fluxora-poc-tracker` | POC health, success criteria, contradictions, portfolio views |
| `fluxora-rfp-drafting` | RFP/security-questionnaire answer reuse, source + confidence, SME gaps |
| `fluxora-product-knowledge` | Capabilities, architecture, GA/preview status, battlecards, terminology |
| `fluxora-crm-capability-audit` | Object/field access, read-vs-write scope, mutation diagnostics |

---

## Section 0 — Baseline

These are the established demo prompts. The new prompts in Sections A–C extend
these without duplicating them.

**0.1 — Discovery brief (discovery-prep)**
> "Give me a discovery brief for **Meridian Payments**. Summarize the account
> (industry, region, size, tech stack), the open opportunity and its stage, who's
> on the deal team, and the primary competitor. Then infer 3 likely technical pain
> points and draft 5 discovery questions I should ask. Read-only."

**0.2 — No-AE coverage gap (deal-brief / hygiene)**
> "List my open opportunities that have **no AE (Deal Owner)** on the team, sorted
> by amount. For each, show the account, stage, product line, and value. Total up
> the pipeline with no AE coverage, and flag the top 5 by dollar risk."
>
> *Lands on: 99 open opps, $60.9M with no AE; top-5 ≈ $5.82M.*

**0.3 — Snowflake bake-off (deal-brief + competitor)**
> "I'm walking into a bake-off against **Snowflake**. Show my open opportunities
> where Snowflake is the primary competitor, total the pipeline at stake, and for
> the largest one draft a one-page competitive brief: deal health, where we're
> strong vs Snowflake on that product line, and 3 next steps. Read-only."

**0.4 — POC triage (poc-tracker)**
> "Show me my **at-risk or recently failed POCs**. For each: the POC ID,
> opportunity, status, dates, environment, and success criteria. Flag any
> opportunity where the **same success criterion was retried and failed again**,
> and identify the AE to notify. Do not update Salesforce."

**0.5 — Product + lead-to-pipeline (product-knowledge + CRM)**
> "Two parts, read-only: (a) Summarize my **StreamSync** opportunity — our new CDC
> product competing with Confluent — including account context and stage. (b) Then
> review my open **leads** and tell me which one is the best fit to become a
> StreamSync opportunity, with reasoning."

---

## Section A — Single-skill prompts (fill the coverage gaps)

### A1 — RFP drafting with source, confidence, and SME gaps
**Skills:** `fluxora-rfp-drafting`

> "Martinez-Banks (OPP-0247) sent us a full RFP covering security, architecture,
> data governance, compliance, and pricing. Draft a response by reusing our
> strongest existing answers from past deals. For every question, cite which prior
> opportunity the answer came from and give it a confidence rating, and flag any
> category where we have no reusable answer so I can route it to an SME."

**Lands on:** 3 real RFP answers on OPP-0247 (Data Governance, Architecture);
genuine SME gaps in Compliance and Pricing for this opp.

### A2 — Reuse-as-confidence on a security questionnaire
**Skills:** `fluxora-rfp-drafting`

> "A new prospect just sent a security questionnaire. Pull our standard approved
> answer on data encryption at rest and in transit from the RFP library, tell me
> how many past opportunities we've reused it on and how confident I should be
> quoting it verbatim, and flag any security topics where we don't have a reusable
> answer yet."

**Lands on:** the AES-256 / TLS-1.2+ answer, reused across 10 named opportunities
— a strong reuse-volume confidence signal.

### A3 — StreamSync availability / status check
**Skills:** `fluxora-product-knowledge` · **no CRM**

> "Before I get on a call with Northwind Logistics on our StreamSync CDC pilot: is
> StreamSync GA yet or is it still private beta? Give me the approved status (GA /
> preview / private beta / roadmap), a plain-English rundown of its CDC and
> change-streaming capabilities and core architecture, the right terminology to
> use, and what I can and can't promise a customer while it's in this stage.
> Product knowledge only, grounded in approved claims — don't touch the CRM."

**Lands on:** the GA-vs-beta status discipline and terminology guidance no other
prompt exercises.

### A4 — Lakehouse Core vs Databricks battlecard
**Skills:** `fluxora-product-knowledge` · **no CRM**

> "Build me a one-page product battlecard for Lakehouse Core vs Databricks: our
> top capability differentiators, the architecture story, GA vs roadmap status of
> the features I'd lean on, the terminology to use, and 3–4 'where we win' talking
> points — strictly from approved product claims, no speculation or made-up
> benchmarks. Read-only, product knowledge only."

### A5 — Read/write capability matrix
**Skills:** `fluxora-crm-capability-audit`

> "Before I trust you with my pipeline, give me a capability audit: for each object
> you touch — Account, Contact, Opportunity, POC__c, SE_Activity__c,
> Competitor_Mention__c, RFP_Response__c, and Opp_Team_Member__c — tell me which
> ones you can READ and which fields, and which ones you can WRITE. Lay it out as a
> read/write matrix and call out anything that's read-only versus mutable. Don't
> change any records — this is just an inventory."

**Lands on:** all 8 objects reachable (Account 241, Contact 2651, Opportunity 355,
POC__c 120, SE_Activity__c 942, Competitor_Mention__c 150, RFP_Response__c 70,
Opp_Team_Member__c 420). Doubles as a **security-review artifact** for the customer.

### A6 — Diagnose a failed write and list gated mutations
**Skills:** `fluxora-crm-capability-audit`

> "I just tried to flip a POC__c record from 'At Risk' to 'In Progress' and it
> didn't seem to save. Diagnose it: do you actually have write access to
> POC__c.Status__c, or is every mutation gated behind a confirmation step? While
> you're at it, tell me exactly which write operations you're capable of and which
> are blocked, so I know what needs human confirmation. To be clear — don't perform
> the write, just audit the permissions and explain the gating."

---

## Section B — Portfolio views (poc-tracker as a management rollup)

### B1 — POC health by pod
**Skills:** `fluxora-poc-tracker`

> "Give me a portfolio health rollup of all our POCs grouped by pod (Enterprise,
> Strategic, Mid-Market). For each pod show the count of POCs by status, the
> success rate vs failure rate, and the total opportunity dollars tied up in At
> Risk or Completed-Failed POCs. Rank the pods so I can see which one is bleeding
> the most, and tell me where I should focus SE coverage this week."

**Lands on:** Enterprise is worst — 26 troubled POCs, ≈ $17.9M at risk.

### B2 — POC failure rate by environment type
**Skills:** `fluxora-poc-tracker`

> "Break down our whole POC portfolio by environment type — Customer Cloud, Fluxora
> Sandbox, and Hybrid. For each environment show how many POCs completed
> successfully vs failed vs are currently at risk, and compute the failure rate. I
> want to know if POCs run in the customer's own cloud fail more often than ones in
> our Fluxora sandbox, so I can decide where to steer new proofs-of-concept."

**Lands on:** a real operational signal — Customer Cloud ≈ 68% failure rate vs
Fluxora Sandbox ≈ 31%.

---

## Section C — Combination prompts (multi-skill + web / memory / taxonomy)

### C1 — Taxonomy over failed POCs
**Skills:** `fluxora-poc-tracker` + `fluxora-product-knowledge` · **Tools:** taxonomy

> "Pull every POC in Completed-Failed status and read each one's success criteria.
> Use the taxonomy to classify each failure into a standard theme (data
> migration/integrity, ingestion & scale/SLA, access control & governance,
> scheduled-pipeline reliability, query latency, ML-model deployment). Then give me
> a portfolio rollup: how many of the 22 failed POCs fall into each theme, which
> theme is costing us the most, and flag any whose success criteria don't map
> cleanly to a standard category. Read-only — don't change any records."

**Lands on:** access-control & governance is the dominant loss theme (≈ $6.29M / 8
POCs). The theme list includes query-latency and ML-deployment because the data
clusters into ~6 themes, not 4.

### C2 — RFP library coverage audit
**Skills:** `fluxora-rfp-drafting` + `fluxora-product-knowledge` · **Tools:** taxonomy

> "Take all 70 RFP responses in the library and give me a coverage rollup by
> standard category (Compliance, Architecture, Security, Data Governance, Pricing &
> Licensing). Tell me which categories are thinnest so I know where our answer
> library is weakest, and run a consistency check confirming each stored category
> still matches where the taxonomy would place the question."

**Lands on:** rollup Compliance 19 / Architecture 18 / Security 13 / Data
Governance 11 / Pricing & Licensing 9 = 70; thinnest = Pricing (9) and Data
Governance (11).

> **Demo note:** phrased as a coverage rollup + *consistency check*, not a
> "find mis-tagged records" hunt. The library holds only 5 distinct questions, all
> correctly tagged, so a mis-tag hunt would surface false positives on stage. Keep
> the scope at all 70 (library-wide) — an owner-scoped run returns only 51 and the
> rollup numbers won't match.

### C3 — Web recon + CRM merge + memory (discovery)
**Skills:** `fluxora-discovery-prep` + `fluxora-product-knowledge` · **Tools:** web search, memory

> "Research Northwind Logistics online — recent news on their data/streaming or
> change-data-capture (CDC) initiatives, funding, and current data stack — then
> merge that with our CRM opp, the StreamSync CDC Pilot ($720K, Technical
> Validation). Give me a discovery-prep brief for my next technical call and flag
> where they'd likely lean toward Confluent. Save the 3 most important external
> facts to memory so I have them for the follow-up."

> **Demo note:** Northwind Logistics is a **fictional** account — a live web search
> may return nothing (or collide with Microsoft's "Northwind" sample database).
> For a live run, either point the web half at a real comparable company or prefer
> **C4**, which searches for real regulatory trends rather than a fabricated
> company.

### C4 — Web regulatory signal → business case + memory
**Skills:** `fluxora-discovery-prep` + `fluxora-product-knowledge` · **Tools:** web search, memory

> "I'm at the Business Case stage on the Meridian Payments Governance Suite deal
> ($960K). Search the web for recent APAC payments and financial-services
> data-governance or regulatory developments that would strengthen our business
> case, merge that with what's already on the opp in CRM, and prep exec-readout
> talking points that connect each regulatory driver to a Governance Suite
> capability. Remember the single strongest regulatory driver to memory for the
> follow-up meeting."

**Lands on:** OPP-ASYA-04, Business Case, $960K. Safer web demo — it queries real
regulatory trends (which exist) rather than a fictional company.

### C5 — Live Databricks battlecard, ranked over pipeline
**Skills:** `fluxora-product-knowledge` + `fluxora-deal-brief` · **Tools:** web search

> "Build me a live Databricks competitive battlecard I can use in deals this week.
> Pull Fluxora's approved positioning and objection-handling for Lakehouse Core and
> PipelineOps versus Databricks, blend in any fresh Databricks news from the web
> over the last quarter (pricing moves, new product launches, earnings/analyst
> takes), and then rank it against the high-threat Databricks deals still open in
> the pipeline. Lead with the biggest one, Ward, Rivera and Burns (OPP-0274), and
> give me a per-deal 'so what' for the top few. Keep this read-only, just a
> briefing."

**Lands on:** 12 open high-threat Databricks deals, ≈ $7.68M; top-3 are OPP-0274
($1.10M), OPP-0275 ($1.04M), OPP-0092 ($868K).

### C6 — Confluent / StreamSync battlecard with web intel
**Skills:** `fluxora-product-knowledge` + `fluxora-deal-brief` · **Tools:** web search

> "Put together a Confluent competitive battlecard for me. Combine our approved
> StreamSync and PipelineOps positioning against Confluent with the latest Confluent
> news you can find on the web (recent releases, pricing, funding/earnings), then
> map it onto the high-threat Confluent deals we still have open. Anchor it on the
> largest, Andrews, Thompson and Taylor (OPP-0006), and flag which talking points
> matter most for the top handful. Read-only, no changes to any records."

**Lands on:** 11 open high-threat Confluent deals, ≈ $6.28M.

### C7 — Full deal posture (deal-brief + POC + competitor)
**Skills:** `fluxora-deal-brief` + `fluxora-poc-tracker` + `fluxora-product-knowledge`

> "Give me the full deal posture on Shah-Burgess (OPP-0082, Governance Suite). Pull
> the opportunity basics (amount, stage, close date, whether it has an AE), the
> current POC status and its success criteria, and any logged competitor threats.
> There's a Databricks mention flagged High — summarize what the risk is and give
> me 3 talking points to counter it heading into Technical Validation."

**Lands on:** OPP-0082, $154K, Technical Validation; POC At Risk (column-level
masking); exactly one competitor mention (Databricks / High).

> **Demo note:** this opp **does** have an AE (team member OTM-00162) and exactly
> one competitor mention. The prompt correctly asks *whether* it has an AE — don't
> pre-narrate "it has no AE."

### C8 — Double-jeopardy scan
**Skills:** `fluxora-poc-tracker` + `fluxora-deal-brief`

> "Scan my open opportunities and show me the ones that are double-jeopardy: a
> competitor mention flagged High AND a POC that's either At Risk or
> Completed-Failed. For each, list the account, amount, stage, the competitor and
> threat level, and the POC status, sorted by amount so I know where the biggest
> exposure is."

**Lands on:** exactly 2 deals — Kim-Adkins (OPP-0081, Snowflake High + failed POC,
$538K) and Shah-Burgess (OPP-0082, Databricks High + at-risk POC, $154K).

### C9 / C10 — RFP answer reality-checked against the deal's own POC
**Skills:** `fluxora-rfp-drafting` + `fluxora-product-knowledge` + `fluxora-poc-tracker`

> **C9:** "I'm finishing the RFP for Gill LLC (OPP-0154, PipelineOps). Draft a
> polished answer to their Security question 'Does Fluxora encrypt data at rest and
> in transit?' using our PipelineOps product knowledge, then cross-check it against
> that deal's live POC: pull the POC status and success criteria and flag anything
> I'm about to claim in the RFP that the POC hasn't actually proven out yet, so I
> don't over-promise. Read-only, don't write anything back."
>
> **C10:** "Help me answer the compliance question on the Garza, Sanchez and
> Mcbride RFP (OPP-0122, Lakehouse Core): 'Is Fluxora SOC 2 Type II certified?'.
> Write the answer grounded in our Lakehouse Core product knowledge, and while
> you're in the deal, look at their POC and tell me its status and success criteria
> so I can decide whether to reference POC progress as a trust proof point in the
> RFP narrative. Prep only — keep it read-only."

**Lands on:** C9 → OPP-0154 with a Security RFP answer + At-Risk PipelineOps POC;
C10 → OPP-0122 with a Compliance RFP question + In-Progress latency POC. This pair
is the strongest "grounded, not guessing" story — it catches an RFP claim the POC
hasn't de-risked.

---

## Recommended headline sequence

For maximum breadth in one session — hits all 6 skills + web,
every record name and dollar figure verified live:

1. **A1** — RFP drafting with source + confidence + SME gaps
2. **A5** — Read/write capability matrix (establishes trust)
3. **B1** or **B2** — Portfolio POC health rollup
4. **C5** — Live Databricks battlecard (product + web + pipeline)
5. **C9** — RFP answer reality-checked against the deal's POC

---

## Maintenance

The record names, IDs, and figures cited here are a live snapshot
(2026-07-18). If the org data changes, re-verify each prompt's supporting query
before a demo — the design intent is that **no prompt returns an empty set or a
300+ row firehose**. The `fluxora-crm-capability-audit` prompts (A5, A6) are a
quick way to re-confirm object counts and access before a run.
