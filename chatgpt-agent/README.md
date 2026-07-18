# Fluxora SE Copilot Skill Pack

This package turns the Fluxora SE Copilot design into portable Agent Skills plus a Workspace Agent instruction set.

## Recommended architecture

Use one **Fluxora SE Copilot** agent or main skill as the entry point, backed by independently testable workflow skills:

1. `fluxora-discovery-prep`
2. `fluxora-poc-tracker`
3. `fluxora-rfp-drafting`
4. `fluxora-deal-brief`
5. `fluxora-product-knowledge` for non-CRM product, security, and competitive questions
6. `fluxora-crm-capability-audit` for safe read/write scope discovery

In environments where you cannot build a Workspace Agent (e.g. ChatGPT Pro or Plus), install the individual workflow skills and use them directly in chat via `@`-mention. Skill selection is model-driven; there is no composite router skill.

## Which files to use

### Personal or Pro workflow

Install the workflow skills you need, plus:

- `skills/fluxora-product-knowledge`
- `skills/fluxora-crm-capability-audit`

Connect or explicitly select the app named **Salesforce CRM** when the task needs CRM data, then invoke a skill with `@`-mention (e.g. `@fluxora-deal-brief`). Do not install `fluxora-crm-writeback` until the client and MCP server both expose approved mutation tools.

### Business or Enterprise Workspace Agent

Use `agent/AGENT_INSTRUCTIONS.md` as the agent's instruction base. Attach the Salesforce CRM app and the four core workflow skills. Add `fluxora-product-knowledge`.

### Plugin packaging

When your workspace supports publishing a plugin that bundles skills and apps, package these skills with **Salesforce CRM** as a required app for CRM-backed workflows. Keep `fluxora-product-knowledge` usable without Salesforce. Keep writeback optional and separately approved.

## Contents

- `agent/AGENT_INSTRUCTIONS.md` — main agent behavior and routing
- `skills/` — uploadable skill directories
- `docs/DESIGN_RECOMMENDATIONS.md` — proposed corrections and additions to the design
- `docs/DEPLOYMENT_AND_TESTING.md` — installation, capability checks, and evaluation plan
- `docs/KNOWLEDGE_FILE_INVENTORY_TEMPLATE.md` — inventory for product and RFP source files

## Naming assumptions

The connected app is assumed to be named **Salesforce CRM**. If your app has a different name, replace that name in all `SKILL.md` files before uploading.

The skills deliberately avoid hard-coding MCP tool names because the discovered tool set can differ by Salesforce server, org configuration, ChatGPT plan, and published app snapshot.
