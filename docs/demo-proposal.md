# Fluxora SE Copilot Demo Proposal

**Thesis:** An SE-facing ChatGPT Enterprise agent that surfaces cross-record deal risks and automates prep work — turning 30 minutes of CRM archaeology into 30-second prompts.

---

## Slide Outline (4 slides, ~5 minutes total)

### Slide 1: The Problem
**Title:** "SE Bandwidth Is the Bottleneck"

- Fluxora SE org tripled to 42 SEs in <2 years; 60–80 active POCs/month
- Deal context lives in Slack/heads, not the CRM; RFP volume outpaces headcount
- SEs toggle between 4–6 tabs (CRM, POC tracker, master RFP doc, Slack) to prep one call
- Knowledge silos between Enterprise/Strategic/Mid-Market pods
- Leadership's #1 blocker on sales velocity: SE capacity

**Speaker note:** "Our SEs are amazing — and overwhelmed. This isn't a people problem; it's a tooling gap."

---

### Slide 2: The Solution
**Title:** "Fluxora SE Copilot — A ChatGPT Workspace Agent"

- Built on ChatGPT Enterprise with 4 Skills + read-only CRM connector
- **Discovery Prep:** account → company background, pain points, questions
- **POC Tracker:** "my POCs" → at-risk flags, draft status updates
- **RFP Drafting:** paste questions → reuse master answers, flag gaps
- **Deal Brief:** opp ID → AE-facing brief (health, competitors, risks, next steps)

**Speaker note:** "We're not replacing SE judgment — we're giving them a copilot that remembers everything they don't have time to check."

---

### Slide 3: Live Demo — Barnett Group (OPP-0088)
**Title:** "Catching What a Busy SE Misses"

- $592K Lakehouse Core deal, Business Case stage, close April 2026
- Economic buyer: Ryan Miller (CDO); competitor: Snowflake (TCO angle)
- AE: Bill South (deal owner); SE: Asya Prokaev (Pre-Sales Consultant on the team)
- **Prompt 1:** `Brief me on OPP-0088` → surfaces buried contradiction: 2 POCs missed latency SLA, both failed/at-risk, but SE notes say "stable"
- **Prompt 2:** `Show me my at-risk POCs` → draft status update for AE in <10 sec
- **Prompt 3:** (paste CDO's 3 security questions) → RFP answers reused from master doc

**Speaker note:** "This is the 'wow' — cross-record analysis that takes a human 30 minutes, done in 3 prompts."

---

### Slide 4: Impact + Next Steps
**Title:** "From 30 Minutes to 30 Seconds"

- **Time savings:** 15–30 min/deal prep → <1 min; 20–40 min/RFP → 5 min review
- **Risk reduction:** POC contradictions, stale competitor intel surfaced automatically
- **Knowledge sharing:** Master RFP answers reused across all pods
- **Next:** Pilot with Strategic pod (10 SEs), iterate on Skills, add write-gated CRM updates

**Speaker note:** "We're not asking SEs to change how they work — we're meeting them in ChatGPT, where they already draft emails and brainstorm."

---

## 5-Minute Demo Walkthrough Script

| Time | Beat | Prompt / Action | What the Copilot Returns |
|------|------|----------------|-------------------------|
| 0:00–0:30 | **Setup** | Screen share: ChatGPT open, "Fluxora SE Copilot" skill visible. "I'm the SE on the Barnett Group deal, prepping for a sync with my AE Bill South." | *(No Copilot action yet; just context-setting for audience)* |
| 0:30–2:00 | **Deal Brief** | Type: `Brief me on OPP-0088` | **Returns:** Deal summary (Barnett Group, $592K Lakehouse Core, Business Case, close 2026-04-07). AE: Bill South (owner); SE: Asya Prokaev. Economic buyer: Ryan Miller (CDO). Competitor: Snowflake (TCO comparison, threat Medium). **KEY INSIGHT (highlight this):** "⚠️ POC-00046 At Risk + POC-00056 Completed–Failed — both missed sub-10s latency SLA. Your notes say 'environment stable' but neither POC hit the benchmark. Recommend: re-scope POC or address perf gap before Proposal." |
| 2:00–2:45 | **POC Tracker** | Type: `Show me my at-risk POCs` | **Returns:** Table: POC-00046 (Barnett Group, At Risk, benchmark latency issue). **Draft status update:** "Bill — POC-00046 flagged. Both POCs missed latency target; we advanced to Business Case but Snowflake is working TCO angle. Recommend call with Ryan Miller to reframe around cost + governance, not raw speed." |
| 2:45–3:45 | **RFP Drafting** | Paste (from a doc): "1. What encryption standards do you support? 2. Do you have SOC 2 Type II? 3. How does RBAC work for multi-tenant environments?" | **Returns:** "1. AES-256 at rest, TLS 1.2+ in transit. 2. Current SOC 2 Type II report available under NDA. 3. Governance Suite provides row/column-level access policies scoped by team, workspace, or business unit." *(Reused from master RFP answers in rfp_responses.csv)* |
| 3:45–4:45 | **Discovery Prep** | Type: `Prep me for ACC-0009` (Oconnor Group — a greenfield account with no open opportunity yet) | **Returns:** Company: Oconnor Group (Gaming, 3,686 employees, APAC). Stack: AWS, Snowflake, Azure. Likely pain points: (1) Snowflake cost/TCO as data volume grows, (2) multi-cloud governance across AWS+Azure, (3) analytics latency at gaming-event scale. Discovery questions: "How is your analytics spend trending on Snowflake as event volume grows?", "How are you governing data access across AWS and Azure today?", "Where do you feel latency pain — ingestion, query, or serving?" |
| 4:45–5:00 | **Wrap** | "That's four workflows — Deal Brief, POC Tracker, RFP, Discovery — each under 60 seconds. Questions?" | *(Pause for Q&A or transition to next section)* |

---

## Timing Table

| Section | Duration | Notes |
|---------|----------|-------|
| Setup + intro | 0:30 | Context-setting, no Copilot interaction yet |
| Deal Brief (OPP-0088) | 1:30 | The "wow" moment — surfaces POC contradiction |
| POC Tracker | 0:45 | Draft status update for AE |
| RFP Drafting | 1:00 | Reuse master answers, show speed |
| Discovery Prep | 1:00 | Top-of-funnel value (not just mid-deal) |
| Wrap / Q&A buffer | 0:15 | Transition or pause |
| **Total** | **5:00** | |

---

## Setup / Prerequisites

**Before the demo, have open:**
1. **ChatGPT (Pro)** — the `deal-brief` skill uploaded, with the **Salesforce CRM** plugin (MCP) connected to the `soma-moma` org.
2. **Data loaded** — the org holds the synthetic dataset. Verify OPP-0088 (Barnett Group), POC-00046 + POC-00056, and ACC-0009 (Oconnor Group) resolve via the connected plugin. Note: the org assigns its own POC record numbers (POC-00046/00056), which differ from the CSV IDs (POC-0047/0057) — the content is identical.
3. **Doc for RFP paste** — A scratch doc/notepad with the 3 security questions pre-typed, ready to copy-paste.
4. **Reference docs** (optional, don't need to show): `docs/superpowers/specs/2026-07-16-crm-agent-demo-design.md` (Section 7 is the scenario), `docs/chatgpt-enterprise-setup-guide.md`.

**Pro tip:** Do a dry-run 24 hours before. If any prompts return incomplete data, confirm the CSVs are current.

---

## What to Say If Asked "Is This Live?"

"Great question. This demo uses **synthetic data** and a documented agent design — the Skills, prompts, and workflows are real and reproducible, but the CRM connector isn't wired to a production Salesforce instance yet. The value is real: we validated these pain points with our SE leadership and two pilot SEs who manually prototyped the workflows. The next step is a live pilot with the Strategic pod, where we'll connect to our actual CRM (read-only to start) and iterate on the Skills based on real deal data. What you're seeing is the **designed experience** — think of it as a high-fidelity prototype that proves the concept before we invest in the integration work."

---

## Additional Notes

- **Why Barnett Group?** It's the perfect "messy real-world deal" — advancing despite red flags, exactly what a Copilot should catch.
- **Why these 4 Skills?** They map to the top 4 SE time-sinks per the leadership interviews: deal prep, POC status, RFP answers, discovery research.
- **Risks to address in Q&A:** (1) "Will SEs trust it?" → Pilot + feedback loop. (2) "What if it hallucinates?" → Master RFP answers are version-controlled; CRM reads are source-of-truth. (3) "Why ChatGPT Enterprise vs. custom UI?" → SEs already live in ChatGPT; no new tool to learn.

---

**For full detail:** See `docs/superpowers/specs/2026-07-16-crm-agent-demo-design.md` (Section 7, "Demo Scenario — A Day With the SE Copilot") and the setup guide at `docs/chatgpt-enterprise-setup-guide.md`. All record IDs in this proposal are real rows in `output/*.csv` and reproducible from the seeded generator.
