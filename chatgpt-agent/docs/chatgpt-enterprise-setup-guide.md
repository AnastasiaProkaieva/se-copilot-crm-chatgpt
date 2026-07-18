# Setting Up "Fluxora SE Copilot" in ChatGPT Enterprise

> **Caveat:** ChatGPT Enterprise's Agent/Skill/Connector feature set is new
> and actively evolving as of this writing (mid-2026). Menu names, exact
> steps, and capability boundaries described below may have shifted by the
> time you read this — treat this as directionally accurate, not a pinned
> reference. Where a claim is time-sensitive, it's flagged explicitly.
>
> This guide is documentation only. No agent, skill, or connector described
> here has been created in a live workspace, and no CRM system is actually
> connected — see the design spec's "Out of Scope" section.

## 1. Create the Workspace Agent

1. In ChatGPT Enterprise, open the workspace admin's **Agents** area
   (sidebar → Agents, or Settings → Agents depending on your workspace's
   rollout). Agent creation/building/publishing are gated by workspace
   RBAC toggles — a workspace admin must enable "allow building agents"
   for your role before you'll see a create option.
2. Create a new agent named **"Fluxora SE Copilot"**.
3. Set the agent's **instructions** to describe its role: a Sales
   Engineering assistant for Fluxora, a data/AI infrastructure company,
   that helps SEs with discovery prep, POC tracking, RFP drafting, and
   deal briefs, always grounding answers in the connected CRM data and
   uploaded knowledge files rather than invented facts.
4. Pick a model appropriate for reasoning over structured CRM data and
   drafting long-form text (a mid-to-high-reasoning-tier model, not the
   fastest/cheapest tier).

## 2. Define the Four Skills

Configure each of the following as a distinct Skill under the agent, so a
user can invoke them explicitly (e.g. via a slash command or a labeled
button) rather than relying on the agent to infer intent every time:

| Skill | What it should do | Primary CRM objects it reads |
|---|---|---|
| **Discovery Prep** | Given an Account name or Opportunity ID, summarize company background, infer likely pain points, and draft discovery questions. | Account, Contact, SE_Activity__c |
| **POC Tracker** | Given an SE name or pod, list active POCs, flag ones that are stalled or missing success criteria, and draft a status update. | POC__c, Opportunity |
| **RFP Drafting** | Given a pasted question or uploaded questionnaire, draft answers reusing past RFP_Response__c records and flag gaps needing SME input. | RFP_Response__c, knowledge files |
| **Deal Brief** | Given an Opportunity ID, produce an AE-facing brief covering deal health, competitive landscape, and next steps. | Opportunity, OpportunityTeamMember, SE_Activity__c, Competitor_Mention__c |

Each Skill's own instructions should specify its expected input, which CRM
objects/fields it's allowed to read, and the output format (e.g. Deal
Brief should always produce the same section headers so AEs can skim it
quickly).

## 3. Upload Knowledge Files

Upload reference material the agent should retrieve from but never
treat as instructions:

- Product battlecards (one per product line: Lakehouse Core, PipelineOps,
  ModelServe, Governance Suite)
- Competitor comparison sheets (Databricks, Snowflake, Confluent)
- A master RFP answer document (a superset of the `rfp_responses.csv`
  rows where `opportunity_id` is blank)

As of this writing, ChatGPT's knowledge file limits are on the order of a
few dozen files and several hundred MB per file — check your workspace's
current documented limits before uploading, since these numbers move
between releases.

## 4. Configure the CRM Connector (Conceptual)

This demo does not connect a live CRM. If you were to wire this up for
real, the current recommended pattern is:

1. The CRM (e.g. Salesforce) exposes its data via a **hosted MCP server**
   rather than a hand-written OpenAPI Action — this is the direction
   OpenAI and major CRM vendors have been moving, and it typically
   supports finer-grained, per-user permission enforcement than a shared
   API key.
2. In the ChatGPT Enterprise workspace, an admin registers the CRM's MCP
   server as a **Connector** under Workspace Settings → Apps/Connectors,
   authenticating via OAuth (the CRM side is typically an OAuth client
   registration distinct from a legacy "Connected App" — check your CRM's
   current terminology).
3. Scope the connector to **read-only** access across the 8 objects in
   this dataset (Account, Contact, Opportunity, OpportunityTeamMember,
   POC__c, SE_Activity__c, Competitor_Mention__c, RFP_Response__c) for the
   Discovery Prep, POC Tracker, and Deal Brief skills.
4. If you later want the RFP Drafting skill (or any skill) to *write*
   back to the CRM — e.g., saving a drafted RFP answer as a new
   RFP_Response__c row — gate that specific write action behind an
   explicit per-action approval step, so no CRM record changes without a
   human confirming it first.

## 5. Workspace Admin Controls to Review

Before publishing this agent org-wide, a workspace admin should check:

- **Who can create/edit/publish agents** — RBAC toggles for "enable
  agents," "enable building," and "enable publishing" (and, separately,
  "enable publishing with personal connections," which controls whether a
  published agent can carry over an individual's personal connector
  authorizations to other users — you do NOT want this enabled for a
  shared CRM connector).
- **Connector/domain allowlisting** — whether the workspace restricts
  which external domains or MCP servers an agent is allowed to connect
  to. If the CRM's MCP server domain isn't allowlisted, the connector
  won't be selectable when configuring the agent.
- **Sharing scope** — whether "Fluxora SE Copilot" is shared with the
  whole workspace, just the SE org, or a smaller pilot group first.

## 6. Fallback: Custom GPT + Actions

If your workspace doesn't yet have Agents/Skills enabled, the same
narrative can be approximated with a classic **Custom GPT**:

- Build one Custom GPT ("Fluxora SE Copilot") via the GPT Builder/Editor
  (chatgpt.com/gpts → Create).
- Use the GPT's **Instructions** field to describe all four workflows
  (Discovery Prep, POC Tracker, RFP Drafting, Deal Brief) as sections,
  since Custom GPTs have no first-class Skill concept — the GPT infers
  which "mode" to use from the user's request or from **Conversation
  Starters** you define per workflow.
- Connect the CRM via a custom **Action** (OpenAPI schema + API key or
  OAuth), instead of a Connector. Note the platform constraint: a GPT can
  use *either* Actions *or* Apps/Connectors, not both — so if you need
  both a CRM Action and a separate pre-built App/Connector, this fallback
  path won't support that combination and you'd need the full Agent
  path instead.
- Upload the same knowledge files as described in Section 3.

This fallback is simpler to set up but is a strictly smaller feature set
than the Agent + Skills + Connector path — use it only if Agents aren't
available in your workspace yet.
