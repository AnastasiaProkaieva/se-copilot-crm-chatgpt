# Salesforce → ChatGPT SE Copilot

Connect your **Salesforce CRM** to **ChatGPT** over the open Model Context
Protocol (MCP), then give it a set of **Skills** and an **Agent** that turn
raw CRM records into things a Sales Engineer actually needs: deal briefs,
POC risk reviews, discovery prep, and RFP drafts.

This repo is a working reference. It ships:

- a **step-by-step how-to** (this file) for wiring a real Salesforce org to
  ChatGPT, read-only, using a Hosted MCP Server + an External Client App;
- six **portable Skills** (`chatgpt-agent/skills/`) and a **Workspace Agent**
  instruction set (`chatgpt-agent/agent/`);
- the **Salesforce metadata** the demo depends on (`force-app/`) — custom
  objects, fields, and a permission set;
- a **synthetic-data generator** (`scripts/`) and a sample dataset
  (`output/`) so you can populate an empty org and follow the worked example.

The worked example uses a fictional company, **Fluxora** (a data/AI
infrastructure vendor). Everything is org-agnostic in shape — swap in your own
objects and knowledge and the same walkthrough holds.

> **This feature area is new and moves fast (2026).** Salesforce Hosted MCP
> Servers, ChatGPT Apps/Plugins, Skills, and Workspace Agents all change
> menu labels and capabilities between releases. Exact UI paths below were
> accurate against official docs at the time of writing; **re-verify each in
> your own tenant.** Where two official sources currently disagree, it's
> flagged inline.

---

## What you'll build

```
  Salesforce org                         ChatGPT
  ┌───────────────────────┐              ┌──────────────────────────────┐
  │ CRM data (per-user)   │              │  Agent: "SE Copilot"         │
  │  Account, Opportunity,│   OAuth 2.0  │   ├─ Skill: deal-brief        │
  │  Contact, POC__c, ... │◄────────────►│   ├─ Skill: poc-tracker       │
  │                       │  auth-code   │   ├─ Skill: discovery-prep    │
  │ Hosted MCP Server     │  + PKCE      │   ├─ Skill: rfp-drafting      │
  │  platform/            │              │   ├─ Skill: product-knowledge │
  │  sobject-reads        │   read-only  │   ├─ Skill: capability-audit  │
  │  (read tools only)    │   tools      │   └─ Skill: crm-writeback*    │
  │                       │              │                              │
  │ External Client App   │              │  Custom MCP App (connector)  │
  │  (OAuth client)       │              │   points at the MCP URL      │
  └───────────────────────┘              └──────────────────────────────┘
        * writeback is optional, mutating, and separately governed —
          it is described here but not shipped in this repo (see Part 3)
```

- **Read-only by design.** You connect the standard `platform/sobject-reads`
  MCP server, which exposes *only* read tools. No mutation is structurally
  possible on it, regardless of client.
- **Per-user permissions.** Every MCP call runs as the authenticating user,
  under their object/field-level security and sharing rules. There are no
  service accounts and no machine-to-machine flows.
- **Skills do the thinking.** The connector just fetches records; the Skills
  encode the SE judgment (risk rules, contradiction detection, source
  discipline). See the skill table in [Part 3](#part-3--skills--the-agent) for
  the catalog and [`chatgpt-agent/docs/DEMO_PROMPTS.md`](chatgpt-agent/docs/DEMO_PROMPTS.md)
  for copy-paste prompts.

---

## Prerequisites

| You need | Notes |
|---|---|
| A Salesforce org where you're **System Administrator** | Required to create an External Client App. Don't have one? See **[Appendix B](#appendix-b--get-a-free-salesforce-developer-org)**. |
| The target **standard MCP server enabled** | Standard servers are **OFF by default** — an admin must turn them on. See Step 1.1. |
| An **MCP-capable ChatGPT plan** with Developer mode | Developer mode is available on **Pro, Plus, Business, Enterprise, and Education** (web). **Workspace Agents and admin-published Apps require Business/Enterprise/Edu.** See [Part 3](#part-3--skills--the-agent). |
| Connecting users have the **CRM permissions** for what they'll read | Per-user enforcement means a user with no access to `POC__c` silently gets empty results even though the connection succeeds. |

> **Scratch orgs:** External Client Apps can't be created through the Setup UI
> in a scratch org — build in a Dev Hub, package, and install. A Developer
> Edition org (Appendix B) has no such restriction.

---

## Part 1 — Salesforce: expose CRM read-only over MCP

The goal of Part 1 is a working **read-only** connection point:

1. an **enabled** standard MCP server (`platform/sobject-reads`), and
2. an **External Client App** that ChatGPT can authenticate against with OAuth.

> **External Client App, not Connected App.** Connected Apps are **not
> supported** for MCP. You must use an External Client App (ECA), the modern
> successor. This trips people up constantly.

### 1.1 Enable the standard read-only MCP server

Standard MCP servers ship **disabled**. Enabling one is an explicit,
non-optional admin action — pointing a client at the URL is *not* enough.

1. In Setup, go to **Integration → Salesforce MCP Servers**.
2. Enable the standard **SObject Reads** server (`platform/sobject-reads`).
   This is the read-only server: it exposes query/search/schema/relationship
   tools and no mutation tools.
3. Note the server URL for your environment:
   - **Production:** `https://api.salesforce.com/platform/mcp/v1/platform/sobject-reads`
   - **Sandbox / scratch:** `https://api.salesforce.com/platform/mcp/v1/sandbox/platform/sobject-reads`

The read tools this server exposes are: `find` (SOSL search), `soqlQuery`,
`getObjectSchema`, `getRelatedRecords`, `getUserInfo`, and
`listRecentSobjectRecords`.

> The exact enablement toggle wording moves between releases; if you don't see
> a "SObject Reads" server to enable, confirm your org's edition/license
> includes Hosted MCP Servers (see [Caveats](#caveats)).

Other standard servers exist if you later need writes — `sobject-mutations`
(create + update), `sobject-deletes` (delete), `sobject-all` (full CRUD) — each
still bounded by the user's permissions. **This guide stays on `sobject-reads`.**

### 1.2 Create the External Client App (OAuth)

The ChatGPT callback URL is generated *by ChatGPT*, so it's cleanest to open
ChatGPT to the point where it shows the callback (Part 2, Step 2.3) first, or
create the ECA now with a placeholder and paste the real callback in afterward.

1. Setup → **External Client App Manager** → **New External Client App**.
2. Fill in **Basic Information** (name e.g. `ChatGPT MCP`, your contact email).
3. Expand **API (Enable OAuth Settings)** → check **Enable OAuth**.
4. **Callback URL:** paste the URL ChatGPT gives you
   (`https://chatgpt.com/connector/oauth/<generated-by-chatgpt>`).
5. **OAuth Scopes** — add exactly these two:
   - `Access MCP servers (mcp_api)`
   - `Perform requests at any time (refresh_token)`
6. Under **Security**, select **Issue JSON Web Token (JWT)-based access tokens
   for named users**. Deselect other options that don't require Salesforce
   Support to change. Click **Create**.
7. Wait. **The ECA can take up to ~30 minutes to propagate** (DNS-like) before
   it's operational.
8. Open **Settings → OAuth Settings → Consumer Key and Secret** and copy the
   **Consumer Key** (client ID). You'll paste it into ChatGPT. (A consumer
   secret is not required for this flow.)

Create the ECA in Setup as above. This repo does **not** publish an External
Client App — the ECA metadata carries org-specific values (callback URL, contact
email) and is intentionally git-ignored (`force-app/main/default/ext*`). If you
build one locally and want to version it, genericize those values first and see
the [pre-publish note](#before-you-publish-or-fork).

### 1.3 (Optional) tighten access

- **Pre-authorize with a Permission Set** (OAuth Policies) so only assigned
  users can connect — by default any org user can authenticate through the ECA.
- Set **Refresh Token Validity ≤ 30 days** + enable **Refresh Token Rotation**.
- Enable **Single Logout** (Session Settings).
- **IP allowlists — caution:** ChatGPT egresses from very large IP ranges that
  can exceed Salesforce's allowlist capacity. Confirm before enabling, or you
  may block the connector entirely.

---

## Part 2 — ChatGPT: connect the MCP server as an App

> **Menu labels are in flux.** As of late 2025, "connectors" became "Apps";
> in mid-2026 the app directory became the "Plugin" directory. Salesforce's
> docs say *Settings → Apps → Create App*; OpenAI's own docs describe enabling
> Developer mode under *Settings → Connectors / Apps & Connectors → Advanced*
> and creating the connector under Plugins. **These two official sources
> currently disagree — locate the live equivalent in your build.** The
> substance below is stable even as labels shift.

### 2.1 Turn on Developer mode

Developer mode is per-user (each admin/owner enables it for themselves).

- **Pro / Plus / individual:** Settings → **Connectors / Apps & Connectors →
  Advanced settings** → enable **Developer mode**.
- **Business / Enterprise / Edu:** an admin first grants developer-mode access
  by role (**Workspace Settings → Permissions & Roles → Connected Data**), then
  each granted user toggles it on in their settings.

### 2.2 Create the custom MCP App

1. Open **Settings → Apps → Create** (admins: **Workspace Settings → Apps →
   Create**).
2. **MCP Server URL:** the `sobject-reads` URL from Step 1.1.
3. **Authentication → Advanced settings:**
   - **Registration Method = "User-defined OAuth client"**
     (Salesforce does **not** support dynamic client registration).
   - **OAuth Client ID:** paste the ECA **Consumer Key** from Step 1.2.
4. Copy the **Callback URL** ChatGPT shows here **back into the ECA** (Step 1.2,
   item 4) if you didn't already.
5. Click **Scan Tools** → complete the OAuth consent → **Create**.

### 2.3 Authorize and smoke-test

On create, ChatGPT redirects to your Salesforce login (OAuth authorization-code
+ PKCE). Once authorized, in a chat click the **(+)** button and explicitly
**select Salesforce**, then try a read prompt:

> What are my top 10 open opportunities by amount?

> **Tip:** test the raw connection in Postman first (native OAuth2 + PKCE,
> returns raw JSON) to isolate auth issues before adding the model.

### 2.4 Publishing to a workspace (Business/Enterprise/Edu)

The App starts as a **Draft**. An admin publishes it (**Workspace Settings →
Apps → Drafts → Publish**), reviews safety warnings, and can restrict which
tools are enabled and who has access (RBAC). Write actions require confirmation
by default; tools carrying the MCP `readOnlyHint` annotation auto-execute — the
`sobject-reads` read tools are all annotated read-only.

---

## Part 3 — Skills + the Agent

Now attach the intelligence. A **Skill** is a folder with a `SKILL.md` (YAML
frontmatter + Markdown body) following the open [Agent Skills
standard](https://agentskills.io). This repo ships **six** under
`chatgpt-agent/skills/` (a seventh, `fluxora-crm-writeback`, is described below
but intentionally not included — see the note under the table):

| Skill | Does | CRM |
|---|---|---|
| `fluxora-deal-brief` | One-opportunity brief: health, stakeholders, POC/tech risk, competitor signals, **contradictions**, next step | read |
| `fluxora-poc-tracker` | Ranks POC risk; flags stale/failed/missing-criteria; drafts an AE status update | read |
| `fluxora-discovery-prep` | Pre-call briefing: verified facts vs. labeled pain-point hypotheses + discovery questions | read |
| `fluxora-rfp-drafting` | Drafts RFP/security answers from approved reusable responses; flags SME-review needs | read |
| `fluxora-product-knowledge` | Product/architecture/security/competitor Q&A from knowledge files — **no CRM record required** | optional |
| `fluxora-crm-capability-audit` | Non-mutating audit of what the connected app/MCP scope can actually do | read |
| `fluxora-crm-writeback`† | **The only mutating skill** — create/update after explicit confirmation, with preview + read-after-write | write |

> † `fluxora-crm-writeback` is described here for completeness but is **not
> included in this repo**. Writeback is optional, mutating, and separately
> governed; the six read-only skills above are the shipped set. Wherever the
> steps below reference `fluxora-crm-writeback`, treat it as something you author
> and add yourself after the capability audit and a sandbox test.

Purpose, inputs, and outputs for each skill live in its own `SKILL.md` under
`chatgpt-agent/skills/`; copy-paste trigger prompts are in
**[`chatgpt-agent/docs/DEMO_PROMPTS.md`](chatgpt-agent/docs/DEMO_PROMPTS.md)**.

### 3.1 Install the Skills

1. Profile icon → **Skills** (`chatgpt.com/skills`).
2. **Create → Upload from your computer**, and upload each skill folder (each
   contains a `SKILL.md`; some carry a `references/` directory). Uploads are
   safety-scanned.
3. Rename the connected app inside each `SKILL.md` if yours isn't named
   **Salesforce CRM** (the skills reference that app name).
4. Invoke a skill by **@-mentioning it** in the composer (e.g. `@fluxora-deal-brief`)
   or let ChatGPT auto-select. *(In ChatGPT the trigger is `@`; `$`/`/skills`
   are Codex conventions, not ChatGPT web.)*

> Skills are GA on Business/Enterprise/Healthcare/Edu. Enterprise/Edu admins
> gate Skills at `chatgpt.com/admin/permissions`; they're off by default today,
> with default-on planned for Enterprise on **2026-07-23** unless the workspace
> opts out.

### 3.2 Business/Enterprise: build the Workspace Agent

1. Left sidebar → **Agents → Create**.
2. Paste `chatgpt-agent/agent/AGENT_INSTRUCTIONS.md` as the agent's
   instructions (role, routing table, grounding rules, read/write policy).
3. **Tools → + Add tool:** add your **custom MCP App** (from Part 2), the four
   core workflow skills, and `fluxora-product-knowledge`.
4. Add approved **knowledge files** (battlecards, RFP master answers — the
   upload-ready set is in
   `chatgpt-agent/docs/fluxora_documentation/fluxora-agent-knowledge/`).
5. Set app writes to **Always ask** (or stricter). Add `fluxora-crm-writeback`
   **only** after running the capability audit and a sandbox test.
6. **Preview**, then **Create**, then manage distribution under **Channels →
   ChatGPT → Manage access**.

> Workspace Agents are Business/Enterprise/Edu-only and off by default at launch
> for Enterprise — an admin must enable them; RBAC governs who can run each.

### 3.3 Personal / Pro path (no Workspace Agent)

Pro/Plus don't have Workspace Agents. Use the Developer-mode connector from
Part 2 plus the Skills directly in chat. Install the read-only trio —
`fluxora-product-knowledge`, `fluxora-crm-capability-audit`, and whichever
workflow skills you need — and leave `fluxora-crm-writeback` uninstalled.

> **Plan-gating clarified:** a Pro user in Developer mode *can* add a custom
> MCP that exposes write tools and invoke them (each write is
> confirmation-gated). What Pro/Plus lack is the **admin publish + Company
> knowledge + RBAC governance layer** and **Workspace Agents** — not write
> capability itself. The "read/fetch-only" framing you'll see applies to the
> vetted **Company knowledge** surface on Business/Enterprise/Edu.

---

## Part 4 — Try it

Point the connector at the demo dataset (Appendix A) and run these. The hero
deal, **OPP-0088 (Barnett Group)**, is engineered to hide a contradiction: the
Lakehouse Core POC ran **twice** and missed the same sub-10s latency criterion
both times (one *At Risk*, one *Completed – Failed*), yet the check-in notes
say "environment stable" — while the deal advanced to Business Case at ~$592K.

```
@fluxora-deal-brief  Brief me on OPP-0088. Separate CRM facts, contradictions, and recommendations.
@fluxora-poc-tracker Show the POCs for SE-037, highest risk first, and draft an internal update for the AE.
@fluxora-rfp-drafting Draft answers for encryption at rest/in transit, SOC 2 Type II, and RBAC. Include source, confidence, and review status.
@fluxora-discovery-prep Prep me for a first discovery call with ACC-0009. Separate known CRM facts from pain-point hypotheses.
```

**The "wow":** deal-brief catches the two-failed-POCs-vs-"stable" contradiction
a human skimming the record would miss. Expected findings and pass criteria for
each are in `chatgpt-agent/docs/DEPLOYMENT_AND_TESTING.md`.

---

## Security & governance

- **Read-only two ways:** the `sobject-reads` server has no mutation tools, and
  every call is bounded by the user's own FLS/object/sharing permissions.
- **No service accounts.** Authorization-code + PKCE per named user only; DCR is
  not supported.
- **Audit:** MCP activity appears in standard Salesforce API event logs
  attributed to the named user. Filter `APICLIENTCATEGORY = SALESFORCE_HOSTED_MCP`.
- **Writeback is opt-in and gated:** `fluxora-crm-writeback` is the sole
  mutating skill, requires a preceding capability audit, an allowlist, explicit
  per-write confirmation, and read-after-write verification. Keep it uninstalled
  for read-only deployments.

---

## Repository layout

```
README.md                         ← you are here
chatgpt-agent/
  README.md                       ← skill-pack overview
  agent/AGENT_INSTRUCTIONS.md     ← Workspace Agent instruction base
  skills/fluxora-*/               ← the 6 Skills (SKILL.md + references/)
  docs/
    DEPLOYMENT_AND_TESTING.md          ← install, capability checks, regression tests
    DEMO_PROMPTS.md                    ← copy-paste demo prompt library
    DESIGN_RECOMMENDATIONS.md          ← design corrections & additions
    FLUXORA_STORY.md                   ← narrative walkthrough
    solution-architecture.drawio       ← architecture diagram
    fluxora_documentation/             ← knowledge pack (see below)
      fluxora-agent-knowledge/         ← canonical upload-ready set
      fluxora-knowledge-pack-draft/    ← draft/source material
      products_information/            ← per-product source docs
force-app/main/default/
  objects/                        ← custom objects + fields + External_Id__c keys
  permissionsets/Fluxora_Demo_Access
  (External Client App metadata is git-ignored — create it per Step 1.2)
scripts/
  generate_crm_data.py            ← synthetic data generator (seeded, reproducible)
  crm_data/, tests/
output/*.csv                      ← generated sample dataset (8 files)
```

---

## Appendix A — Deploy the demo schema + load synthetic data

The demo data does **not** fit stock Salesforce (however can be simply adapted by changes in skills) — it relies on custom objects
(`POC__c`, `SE_Activity__c`, `Competitor_Mention__c`, `RFP_Response__c`,
`Opp_Team_Member__c`), custom Account/Contact/Opportunity fields, and an
`External_Id__c` (Text, Unique, External ID) key on every object.

**1. Deploy the schema first** (nothing loads without it):

```bash
sf project deploy start --source-dir force-app --target-org <your-org-alias>
sf org assign permset --name Fluxora_Demo_Access --target-org <your-org-alias>
```

**2. (Re)generate the dataset** — reproducible, seeded:

```bash
pip3 install faker
cd scripts && python3 generate_crm_data.py        # writes 8 CSVs to ../output/
# python3 generate_crm_data.py --seed 7            # different corpus
cd tests && python3 -m pytest -v                   # optional: validate coherence
```

Row counts: accounts 200 · contacts 600 · opportunities 350 ·
opportunity_team_members 400 · pocs 120 · se_activities 900 ·
competitor_mentions 150 · rfp_responses 70.

**3. Load, parents before children.** The prefixed IDs (`ACC-0001`, `OPP-0001`,
…) are **external IDs**, not Salesforce record IDs — they load into
`External_Id__c` and are the upsert match key.

- **Data Loader (GUI):** Upsert → pick `External_Id__c` as the match field →
  map columns (snake_case CSV headers → API names) → run per object in load
  order. For child objects map the parent via `Opportunity__r:External_Id__c`.
- **`sf` CLI (Bulk API):** rename CSV headers to API field names and add a
  relationship column (`Account.External_Id__c` on Contact/Opportunity;
  `Opportunity__r.External_Id__c` on the child objects), then:

  ```bash
  sf data upsert bulk --target-org <alias> --sobject Account \
    --external-id External_Id__c --file output/accounts.csv --wait 10
  ```

  Load order: `accounts` → `opportunities` + `contacts` → `pocs`,
  `se_activities`, `competitor_mentions`, `rfp_responses`,
  `opportunity_team_members`. Upsert is idempotent — re-run children if a parent
  hadn't finished.

**4. Verify:**

```bash
sf data query --target-org <alias> --query "SELECT COUNT() FROM Account"        # 200
sf data query --target-org <alias> --query "SELECT COUNT() FROM Opportunity"    # 350
```

---

## Appendix B — Get a free Salesforce Developer org

No org? A **Developer Edition** org is free, non-expiring, and full-featured.

1. Go to <https://developer.salesforce.com/signup>.
2. Fill the form. The **Username** must be globally unique and in email format
   (e.g. `you+fluxora@example.dev`) but need not be a real mailbox; the
   **email** must be reachable (activation link).
3. Activate, set a password, and you have a full Lightning Platform org (Apex,
   custom objects, metadata deploys, API). Storage is small (~5 MB data / 20 MB
   files) — fine for this dataset.

Then follow Appendix A to deploy the schema and load data, and Part 1 to enable
MCP.

---

## Before you publish or fork

This repo is meant to be public. The exclusions below are **already applied**
via `.gitignore`; if you fork or copy the folder, keep them in place and re-check
before pushing:

- **`.gitignore`** already excludes `.sfdx/`, `.vscode/`, `.cursor/`, `.mvn/`,
  `.DS_Store`, `stage_phase/`, `docs/superpowers/` (local design spec + plan,
  which may contain `/Users/...` paths), and all External Client App metadata
  (`force-app/main/default/ext*`). A bare `git add .` will not pull in your org's
  schema cache, local editor config, or ECA.
- **External Client App** — the ECA is git-ignored, so it never publishes. If
  you deliberately un-ignore one to share it, first replace the real
  `contactEmail` and ChatGPT `callbackUrl` with placeholders, and **never commit
  a consumer secret, access token, or refresh token.**
- **No `.sfdx/` auth files** in history — verify with
  `git log --all --stat | grep -i sfdx`.


