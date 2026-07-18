---
name: fluxora-deal-brief
description: Produces an evidence-grounded Fluxora opportunity or account brief from Salesforce, including deal health, stakeholders, POC status, technical risks, competitor signals, contradictions, and prioritized next steps. Use for brief me on an opportunity, account review, deal inspection, or AE-SE handoff.
compatibility: Requires the connected Salesforce CRM app with read access to Opportunity, Account, OpportunityTeamMember, POC__c, SE_Activity__c, Competitor_Mention__c, and stakeholder data.
metadata:
  owner: Fluxora Sales Engineering
  version: "0.1.0"
---

# Fluxora Deal Brief

## Inputs

Accept Opportunity ID or name. Account name is allowed when the user wants an account-level view.

## Required workflow

1. Resolve the Opportunity and confirm the Account.
2. Retrieve:
   - Opportunity and Account
   - OpportunityTeamMember
   - POC__c
   - SE_Activity__c
   - Competitor_Mention__c
   - OpportunityContactRole or equivalent stakeholder records
   - Account Contacts as unconfirmed candidates only when no opportunity-level relation exists
3. Check stage, amount, close date, team, recent activity, POC outcomes, success criteria, and competitor trend.
4. Apply the [deal-health rules](references/deal-health-rules.md).
5. Compare records for contradictions.
6. Produce the [required output](references/output-template.md).

## Guardrails

- Do not infer that every Account Contact is involved in the Opportunity.
- Do not call a person a champion or economic buyer unless CRM explicitly identifies that role.
- Do not hide an overdue close date because another risk appears more interesting.
- Do not update the Opportunity or related records.

## Final checks

- Health rating is rule-based and explained.
- POC and stakeholder data are included, not omitted.
- Every contradiction identifies both supporting records.
- Recommendations are specific and limited to three priorities.
