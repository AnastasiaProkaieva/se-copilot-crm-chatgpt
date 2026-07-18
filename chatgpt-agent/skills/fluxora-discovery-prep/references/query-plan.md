# CRM Query Plan

1. Resolve Account by exact ID, then exact name, then fuzzy name.
2. If given an Opportunity, retrieve Opportunity first and follow AccountId.
3. Retrieve Contacts for the Account.
4. Prefer opportunity-level stakeholder relations when available.
5. Retrieve recent Opportunities for context, avoiding closed deals unless relevant.
6. Retrieve the most recent discovery calls, demos, and internal sync activities.
7. Record missing objects or inaccessible fields in the final `Data gaps` section.
