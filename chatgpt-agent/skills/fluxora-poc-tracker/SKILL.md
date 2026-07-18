---
name: fluxora-poc-tracker
description: Finds and assesses Fluxora proofs of concept in Salesforce, ranks POC risk, detects missing criteria, stale check-ins, repeated failures, and contradictory notes, and drafts concise status updates. Use for my POCs, pod POCs, at-risk POCs, stalled validations, or POC portfolio reviews.
compatibility: Requires the connected Salesforce CRM app with read access to POC__c, Opportunity, OpportunityTeamMember, and SE_Activity__c.
metadata:
  owner: Fluxora Sales Engineering
  version: "0.1.0"
---

# Fluxora POC Tracker

## Inputs

Accept one or more of:

- `my POCs`
- SE name or ID
- pod
- Account or Opportunity
- status or date filter

## Required workflow

1. Resolve ownership.
   - For `my`, attempt to map the authenticated Salesforce user to the SE roster.
   - If no mapping is available, ask for the SE name or ID.
   - Traverse OpportunityTeamMember unless POC__c has a direct SE owner field.
2. Retrieve POC__c, related Opportunity fields, and recent SE_Activity__c.
3. Group sibling POCs by Opportunity and compare success criteria and outcomes.
4. Apply the [risk rules](references/risk-rules.md).
5. Rank high risk first.
6. Produce the [required output](references/output-template.md).

## Guardrails

- Do not infer ownership from a note author unless the relationship is explicit.
- Do not call a POC stalled solely because it is old; use status, dates, and activity evidence.
- Do not change POC status through this skill.
- Label contradictions as cross-record observations, not accusations.

## Final checks

- Every listed POC belongs to the requested user, pod, or opportunity scope.
- Every risk flag cites the fields or records that triggered it.
- Repeated criteria are compared exactly or with clearly stated normalization.
- Draft updates do not claim that an action has already occurred.
