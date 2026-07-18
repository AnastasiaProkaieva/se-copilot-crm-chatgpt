---
name: fluxora-crm-capability-audit
description: Safely audits the connected Salesforce CRM app and MCP scope, inventories available objects and actions, and reports whether read, create, update, or delete operations are available without changing CRM data. Use after connecting or updating Salesforce MCP, before enabling write workflows, or when a tool call fails.
compatibility: Requires the connected app named Salesforce CRM. This skill is deliberately non-mutating and must not execute create, update, or delete actions.
metadata:
  owner: Fluxora CRM Administration
  version: "0.1.0"
---

# Salesforce CRM Capability Audit

## Safety rule

This audit must not create, update, delete, convert, merge, or send anything.

## Required workflow

1. Inspect the Salesforce CRM app details or available action definitions when the client exposes them.
2. Record the MCP server or endpoint name if visible.
3. Inventory actions and classify each as:
   - Search
   - Fetch or read
   - Describe or metadata
   - Create
   - Update
   - Delete
   - Custom automation
4. Verify read access with low-risk queries against:
   - Account
   - Contact
   - Opportunity
   - OpportunityTeamMember
   - POC__c
   - SE_Activity__c
   - Competitor_Mention__c
   - RFP_Response__c
5. Do not attempt a mutation to prove write access. The presence of an approved mutation action is sufficient for this audit.
6. Report client-level constraints separately from Salesforce server capabilities.
7. Produce the [capability matrix](references/output-template.md).

## Interpretation rules

- A server or action labeled read-only does not support writes.
- The existence of a write-capable Salesforce server does not prove the ChatGPT client, workspace, app snapshot, user permissions, or approval policy permits the action.
- Salesforce object permissions, field-level security, and sharing rules may differ by user.
- Custom objects can be absent from the tool schema or inaccessible even when standard objects work.

## Final checks

- No data was changed.
- Server capability, ChatGPT capability, app action enablement, and user permission are reported as separate layers.
- Unknown capabilities are marked `Unknown`, not `No`.
- The recommendation states whether `fluxora-crm-writeback` should remain disabled.
