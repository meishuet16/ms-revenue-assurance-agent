# detect-billing-variances

Identify billing discrepancies and source-data anomalies for a requested review period.

## Inputs

- `period_start DATE`
- `period_end DATE`

## Tools

- `scan_billing_variances(period_start, period_end)`
- `get_pricing_evidence(customer_id, period_start, period_end)`

## Procedure

1. Run `scan_billing_variances` for the review period.
2. Treat monetary amounts and date coverage from SQL as authoritative.
3. For each returned finding, retrieve pricing evidence.
4. Flag duplicate or conflicting usage records as data quality issues.
5. Pass findings to `validate-commercial-evidence`.

## Rules

- Do not make the final leakage classification.
- Do not use an LLM for monetary arithmetic.
- If source data is inconsistent, flag a data-quality issue and do not calculate a financial amount.
- Every amount must come from deterministic SQL output.

