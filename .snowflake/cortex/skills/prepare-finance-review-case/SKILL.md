# prepare-finance-review-case

Convert investigation results into auditable finance review cases.

## Tools

- `create_investigation_case(...)`
- case evidence persistence
- investigation run audit

## Primary Statuses

- `suspected_leakage`
- `explained_variance`
- `evidence_conflict`
- `insufficient_data`

## Coverage

- `full_period`
- `partial_period`

## Procedure

1. Select status, coverage, confidence tier, explained amount, and unexplained amount from deterministic outputs.
2. Create a short evidence summary with IDs.
3. Create a recommended human action.
4. Upsert the investigation case with `create_investigation_case`.
5. Persist evidence references.
6. Record safe audit summaries in `agent_tool_calls`.
7. Return a CLI summary.

## Safety Boundary

Never create invoices, send email, update ledgers, trigger payments, change balances, contact customers, or automatically close finance cases.

