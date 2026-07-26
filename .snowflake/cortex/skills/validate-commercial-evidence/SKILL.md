# validate-commercial-evidence

Validate whether a billing variance is explained by a commercial exception and whether the structured exception agrees with source documents.

## Inputs

- `customer_id`
- `period_start`
- `period_end`
- `gross_variance`

## Tools

- `get_commercial_exceptions(customer_id, period_start, period_end)`
- `search_approval_documents`

## Decision Branches

- No exception: run negative-evidence document search for material variance, then pass candidate `suspected_leakage`.
- Valid exception and matching document: classify as `explained_variance`.
- Partial coverage: split covered and uncovered periods.
- Structured record approved but source document conditional: classify as `evidence_conflict`.
- Conflicting source data: classify as `insufficient_data`.

## Required Wording

Use: `No contradictory evidence retrieved from indexed sources.`

Never use: `confirmed recoverable amount`.

## Rules

- A failed document search does not prove that no real-world approval exists.
- When an exception is marked approved, inspect the linked source document before finalizing.
- If Cortex Search is unavailable, mark document validation as pending.

