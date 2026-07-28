# Demo Script

## Current Demo Status

Use this wording exactly:

> The project has connected successfully to Snowflake and the core live database setup is validated: tables, stored procedures, approval document fixtures, and ground truth are present. Cortex Search is marked pending because this Snowflake trial account reports `AI function EMBED_TEXT_768 is not available for trial accounts`. The dashboard remains safe fixture mode by default for a deterministic demo.

Do not claim that Cortex Search was created in the trial account. Do not claim CoCo CLI end-to-end execution if the local Cortex Code usage limit blocks it.

## One-Minute Pitch

Finance teams can see invoice variances, but they usually cannot tell quickly whether a variance is true revenue leakage, an approved concession, a conflicting approval, or a data-quality blocker.

This agent automates the investigation workflow around Q3 billing integrity. Deterministic Snowflake SQL computes the money. Agent Skills organize the workflow. The Streamlit dashboard gives finance reviewers evidence-backed cases without allowing the system to create invoices, update ledgers, contact customers, or trigger payments.

## Preflight Commands

Run from the repository root:

```powershell
python scripts\run_tests.py
python scripts\run_evaluation.py
python scripts\validate_environment.py
python scripts\setup_project.py --warehouse COMPUTE_WH --skip-search
python scripts\verify_database.py --allow-missing-search
```

Expected signals:

- tests pass;
- evaluation reports 12 synthetic cases;
- classification accuracy is `1.0`;
- monetary calculation accuracy is `1.0`;
- unsafe action rate is `0`;
- Snowflake core verification passes;
- Cortex Search is reported as pending, not failed, for the trial account.

## Snowflake Validation Talk Track

Say:

> I am using a Snowflake trial account, so I validated the core database path separately from Cortex Search. The setup script connected to Snowflake, created the `REVENUE_ASSURANCE` database objects, loaded synthetic data, created procedures, loaded approval documents, and verified Q3 ground truth. The only unavailable feature is Cortex Search embedding, which Snowflake reports as unavailable for trial accounts.

Show or quote this verification result:

```text
PASS table contracts
PASS table pricing_terms
PASS table usage_records
PASS table invoices
PASS table invoice_lines
PASS table commercial_exceptions
PASS table investigation_runs
PASS table investigation_cases
PASS table case_evidence
PASS table agent_tool_calls
PASS table approval_documents
PASS procedure scan_billing_variances
PASS procedure get_pricing_evidence
PASS procedure get_commercial_exceptions
PASS procedure create_investigation_case
PASS procedure add_case_evidence
PASS procedure update_case_review_status
PASS procedure start_investigation_run
PASS procedure log_agent_tool_call
PASS view q3_2026_ground_truth
PASS ground truth row count: 4 rows
PASS ground truth total variance: 16000.00 total
PASS cortex search search_approval_documents: pending for trial account
```

## CoCo CLI Segment

Show the intended command:

```powershell
cortex -c hackathon -w . -f prompts/run_q3_investigation.md
```

Say:

> The CoCo CLI workflow is implemented through three modular skills: detect billing variances, validate commercial evidence, and prepare finance review cases. My current account hit a Cortex Code usage or entitlement limit, so I am showing the implemented prompt and skill structure plus the validated Snowflake procedures and dashboard output.

Skill names to point to:

- `detect-billing-variances`
- `validate-commercial-evidence`
- `prepare-finance-review-case`

## Dashboard Startup

Use fixture mode for the dashboard unless live dashboard reads have been explicitly implemented and validated:

```powershell
python -m streamlit run app/app.py --server.port 8501
```

Open:

```text
http://localhost:8501/
```

Say:

> The dashboard is intentionally a finance review interface, not a billing execution interface. It presents prepared cases and review actions but does not trigger external financial changes.

## Summary Tab

Point to the top metrics:

- Gross variance detected: `$16,000`
- Suspected leakage: `$9,000`
- Explained variance: `$6,000`
- Evidence conflict: `$1,000`
- Data-quality cases: `1`

Say:

> The important design choice is that the system does not collapse every variance into leakage. It separates four outcomes so finance can act safely.

## Case Queue Tab

Walk through each case:

- Nova Retail: suspected leakage because approved pricing was active but invoices stayed lower.
- Kensington Labs: explained variance because concession evidence supports the lower billing.
- BrightFarm Co: evidence conflict because the registry and source approval document disagree.
- Summit Manufacturing: insufficient data because duplicate usage records conflict.

Say:

> This protects finance from false positives. A concession is not leakage, and a data-quality conflict is not a number the model is allowed to invent.

## Evidence Trail Tab

Select Nova Retail first.

Say:

> Every case has cited evidence: pricing terms, invoice lines, commercial exceptions, approval documents, or usage records. Monetary values come from deterministic SQL or deterministic Python fixtures, not from LLM arithmetic.

Then select BrightFarm Co.

Say:

> This case is deliberately not auto-resolved. The structured exception says approved, but the supporting document says final approval is still conditional. The safe output is finance review, not a billing correction.

## Flow Map Tab

Say:

> The Flow Map is the visual audit path. It shows how each customer moves from detection, to evidence validation, to a prepared finance review outcome.

Use it to reinforce the workflow:

1. Detect variance and data-quality issues.
2. Validate pricing, exceptions, and documents.
3. Prepare the finance review case.

## Safety Boundary

Say:

> The agent never creates invoices, sends emails, updates ledgers, changes balances, or contacts customers. It prepares evidence-backed cases for human review only.

## Closing Line

Say:

> This is a Snowflake-native revenue assurance investigation workflow. The core database path is live-validated in Snowflake, the financial logic is deterministic, the review boundary is explicit, and Cortex Search is the only pending piece because this trial account does not expose the required embedding function.

## If Asked About Deployment

Answer:

> Deployment is not required for judging the core workflow. The local Streamlit dashboard is enough for the demo. Deploy only if a public link or mobile viewing is required.

## If Asked About Cortex Search

Answer:

> The project includes Cortex Search setup SQL and synthetic approval documents. The live trial account rejects the embedding function with `EMBED_TEXT_768 is not available for trial accounts`, so I validated the core database and marked Cortex Search pending instead of falsely claiming it passed.

## If Asked Whether Snowflake Is Connected

Answer:

> Yes. Password authentication succeeded, the setup script executed in Snowflake, and verification passed for core tables, procedures, approval documents, and ground truth. The failed item is only the Cortex Search service creation in the trial account.
