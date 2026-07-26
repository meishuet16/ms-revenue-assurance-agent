# Demo Script

## Problem

Revenue leakage is often not caused by one obvious billing error. It happens when pricing, usage, invoices, commercial exceptions, and approval documents disagree across systems.

## CLI Execution

```bash
cortex -c hackathon -w . -f prompts/run_q3_investigation.md
```

Show the three skills:

- `detect-billing-variances`
- `validate-commercial-evidence`
- `prepare-finance-review-case`

## Decision Branches

- Nova Retail: no valid exception.
- Kensington Labs: exception and document agree.
- BrightFarm Co: exception and document conflict.
- Summit Manufacturing: source-data conflict causes refusal to calculate.

## Output

- Suspected leakage: `$9,000`
- Explained variance: `$6,000`
- Evidence conflict: `$1,000`
- Data-quality cases: `1`

## Streamlit

```bash
streamlit run app/app.py
```

Open Summary, Case Queue, and Evidence Trail.

In Summary:

- point to the executive metric row;
- show the Q3 2026 decision branch cards;
- explain that suspected leakage, explained variance, evidence conflict, and data quality remain separate categories.

In Case Queue:

- select Nova Retail;
- point to the focused case detail panel;
- show the review action safety panel;
- use Accept finding, Dismiss, and Assign.

In Evidence Trail:

- show the audit timeline;
- point to pricing terms, invoice lines, approval documents, classification, and recommended human action.

Explain that no actual financial action is triggered.
