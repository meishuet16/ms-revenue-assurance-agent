# Demo Script

## Demo Goal

Show a finance reviewer how the project separates recoverable suspected leakage from valid commercial variance, evidence conflict, and data-quality blockers without crossing the human review boundary.

Use offline fixture mode for a reproducible demo until live Snowflake and CoCo CLI validation are completed.

## Preflight

From the repository root:

```bash
python scripts/run_tests.py
python scripts/run_evaluation.py
```

Expected offline signals:

- deterministic tests pass;
- evaluation covers 12 synthetic cases;
- unsafe action rate is `0`;
- monetary calculation accuracy is `1.0`.

Do not claim live Snowflake execution unless `python scripts/validate_environment.py`, `python scripts/setup_project.py`, and `python scripts/verify_database.py` have passed in the configured account.

## Context

Revenue leakage is often not caused by one obvious billing error. It happens when pricing, usage, invoices, commercial exceptions, and approval documents disagree across systems.

## CLI Execution

Primary live command, pending local CoCo CLI and Snowflake validation:

```bash
cortex -c hackathon -w . -f prompts/run_q3_investigation.md
```

Show the three skills:

- `detect-billing-variances`
- `validate-commercial-evidence`
- `prepare-finance-review-case`

If live validation is not available, present the prompt and skills as the intended CoCo CLI workflow and use the offline dashboard walkthrough for the executed demo.

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

Keep fixture mode as the default. Set `SNOWFLAKE_DASHBOARD_MODE=live` only after live Snowflake validation passes.

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

## Closing Line

The implemented, verified demo is the offline deterministic finance review flow. The live Snowflake path is ready for credentialed validation, but remains pending until account, warehouse, role, Cortex Search, and CoCo CLI access are confirmed.
