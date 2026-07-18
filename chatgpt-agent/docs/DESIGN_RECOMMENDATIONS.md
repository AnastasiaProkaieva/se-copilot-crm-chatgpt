# Design Review and Recommendations

## 1. Use an agent as the orchestrator, not skill-to-skill calls

For a Workspace Agent, attach the Salesforce CRM app and the independent workflow skills. Put routing, shared grounding rules, and write policy in the agent instructions. Do not rely on one skill programmatically calling another; skill selection is model-driven.

For a personal or Pro environment without Workspace Agents, install the individual workflow skills and invoke them directly via `@`-mention; skill selection is model-driven and no composite router skill is needed.

## 2. Correct the object scope for Deal Brief

Deal Brief needs more than the objects listed in the original table. It must retrieve:

- POC__c to detect failed or repeated validation criteria
- Contact or, preferably, OpportunityContactRole for buyer and champion context
- Account for company context

Without POC__c, the featured Barnett Group contradiction cannot be discovered. Without opportunity-level stakeholder relations, a Contact's role is ambiguous.

## 3. Correct the ownership path for POC Tracker

`my POCs` cannot be answered reliably from POC__c and Opportunity alone because the current POC model has no SE owner field. Traverse:

`POC__c -> Opportunity -> OpportunityTeamMember -> SE`

A better production model adds `Primary_SE__c` directly to POC__c while retaining the OpportunityTeamMember relationship for validation.

## 4. Add an opportunity-level stakeholder object

Account-level Contacts are not automatically involved in every deal. Add standard `OpportunityContactRole` or a custom `Opportunity_Stakeholder__c` with:

- opportunity_id
- contact_id
- role
- influence_level
- champion_status
- technical_evaluator flag
- last_verified_date

## 5. Make POC success measurable and structured

A single free-text success criterion is difficult to score. Add:

- criterion_id
- metric
- target
- unit
- actual_result
- pass_fail
- evidence_link
- owner
- blocker
- next_step
- latest_checkin_date
- outcome_reason

Allow multiple criteria per POC through a child object such as `POC_Criterion__c`.

## 6. Add RFP governance metadata

RFP answers need provenance and freshness. Add:

- approval_status
- approved_by
- source_document
- source_section
- effective_date
- review_date
- product_version
- confidentiality
- allowed_customer_scope

Approved policy documents should override historical deal-specific answers.

## 7. Add explicit deal-readiness fields

For production use, consider:

- next_step
- next_step_due_date
- technical_risk
- decision_criteria
- decision_process
- security_review_status
- procurement_status
- last_meaningful_activity_date
- technical_validation_status

These fields reduce reliance on interpreting prose notes.

## 8. Treat company background as a separate source

The CRM model supports an account snapshot, not a complete current company background. Enable web search or a business-intelligence source for current external research. Keep external facts separate from CRM facts and internal hypotheses.

## 9. Make the Barnett demo flag the overdue close date

The hero Opportunity is in Business Case with a close date of `2026-04-07`. On the design date `2026-07-16`, that date is already overdue. The Deal Brief should flag this as a Red timeline risk in addition to the repeated POC failure and contradictory activity note. Either make the overdue date intentional and include it in the demo narration, or move the close date into the future.

## 10. Add identity mapping

`my POCs` and `my deals` require a dependable mapping from the authenticated Salesforce user to an SE roster record. Define the mapping explicitly rather than relying on display-name matching.

## 11. Add observability and evaluation

Track:

- skill activation accuracy
- Salesforce tool-call success rate
- missing-field rate
- contradiction detection rate
- unsupported-claim rate in RFP drafts
- user corrections
- write confirmation and failure rate

Use the Barnett scenario as a regression test, not only a demo script.
