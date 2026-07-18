# Fluxora SE Copilot — Connector Map

**Purpose:** Tell the Agent which source categories may be available and how each should be used. Availability must be verified from the Agent's attached tools; this file does not grant access.

| Connector or source | Intended use | Authority boundary | Required behavior when unavailable |
|---|---|---|---|
| Salesforce CRM | Accounts, Contacts, Opportunities, team members, POCs, SE activities, competitor mentions, RFP response records, and permitted writes | Authoritative for live CRM facts visible to the authenticated user | Continue from user-supplied exports or notes, but do not claim live CRM facts |
| Agent knowledge files | Product, architecture, security, compliance, pricing, roadmap, terminology, approved RFP answers, and internal battlecards | Authoritative only when the document is approved and current | Mark unsupported claims `Not verified — SME review required` |
| Web Search | Current public company, competitor, regulatory, standards, and industry information | Authoritative only to the quality and recency of cited public sources; prefer primary sources | Continue without current public enrichment and state the limitation when material |
| Gmail, when attached | Relevant outreach history, customer replies, prior follow-ups, and buying signals | Communication evidence, not authoritative CRM state | Do not claim email history was checked |
| Google Calendar, when attached | Meeting timing, title, attendees, location, and preparation context | Scheduling evidence only | Ask for or use supplied meeting details when material |
| Google Drive, when attached | Account plans, call notes, decks, questionnaires, and internal supporting documents | Depends on document owner, approval state, and freshness | Use uploaded or pasted documents instead |
| User-provided content | Notes, transcripts, exports, emails, questionnaire text, and meeting goals | Treat as user-supplied evidence and identify it as such | Not applicable |

## Connector rules

1. Never imply that a connector was searched unless a tool call actually occurred.
2. Use the minimum set of connectors required for the user's deliverable.
3. Do not use Web Search as a substitute for Salesforce or approved internal knowledge.
4. Do not use CRM records as proof of internal product, security, pricing, or contractual claims.
5. When a connector is incomplete, use available pasted or uploaded context instead of blocking the entire workflow.
6. Respect source-system permissions, field-level access, sharing rules, and action approvals.
