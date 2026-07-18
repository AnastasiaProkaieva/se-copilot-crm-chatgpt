---
name: fluxora-discovery-prep
description: Prepares Fluxora Sales Engineers for discovery and first meetings using Salesforce account, contact, opportunity, and activity context plus approved product and battlecard files. Use for account research, discovery-call preparation, stakeholder mapping, pain-point hypotheses, and discovery-question generation.
compatibility: Requires the connected Salesforce CRM app for live CRM facts. Uses approved Fluxora product, industry, competitor, and security knowledge files when available.
metadata:
  owner: Fluxora Sales Engineering
  version: "0.1.0"
---

# Fluxora Discovery Prep

## Inputs

Accept an Account name or ID, an Opportunity name or ID, and optional meeting purpose or attendee names.

## Required workflow

1. Resolve the Account.
   - If the input is an Opportunity, retrieve its Account.
   - When multiple records match, show candidates and do not guess.
2. Use **Salesforce CRM** to retrieve:
   - Account: industry, employee count, region, technology tags, and other relevant fields
   - Contacts: name, title, role, and contact details the user may access
   - Relevant open or recent Opportunities
   - Recent SE_Activity__c, especially discovery calls and technical demos
3. Retrieve relevant knowledge:
   - Product-line one-pager
   - Industry guidance
   - Competitor battlecard when a competitor is known
   - Security or architecture guidance when the meeting topic requires it
4. Treat likely pain points as hypotheses, not facts.
5. If current public company background is requested and web search is available, research it separately and cite it. Do not present CRM fields as a complete public-company profile.

See [query plan](references/query-plan.md) and [required output](references/output-template.md).

## Guardrails

- Do not invent company initiatives, budgets, systems, or priorities.
- Do not treat every Account Contact as a confirmed opportunity stakeholder.
- Do not expose contact details unless they are relevant to the user's request.
- Do not update CRM records.

## Final checks

- Every known fact is sourced from CRM, approved knowledge, or cited external research.
- Every pain point is labeled as a hypothesis.
- Questions are specific to the account's industry, stack, product line, and stage.
- The output contains a short list of information gaps to confirm during discovery.
