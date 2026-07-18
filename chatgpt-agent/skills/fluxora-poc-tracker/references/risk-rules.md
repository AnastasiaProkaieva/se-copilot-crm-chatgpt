# POC Risk Rules

## High risk

- Status is `At Risk`.
- Status is `Completed - Failed` and the Opportunity remains open.
- End date is past and status is not `Completed - Success`.
- Success criteria are blank, generic, or not measurable.
- A sibling POC for the same Opportunity failed the same normalized success criterion.
- POC status or result conflicts with recent SE activity notes.

## Medium risk

- Active POC has no POC check-in in the last 14 days.
- End date is within seven days and no current progress evidence is available.
- The Opportunity is in Business Case or Negotiation while technical success criteria remain unresolved.
- The close date is past while the Opportunity remains open.

## Low risk

- Active POC has measurable criteria, recent activity, and no contradictory or failed sibling record.
- Completed POC succeeded and no unresolved blocker is documented.

## Normalizing success criteria

When comparing criteria:

1. Lowercase text.
2. Remove punctuation and extra whitespace.
3. Normalize equivalent latency, throughput, migration, deployment, and governance phrases.
4. Do not treat different numeric thresholds as identical without stating the difference.
