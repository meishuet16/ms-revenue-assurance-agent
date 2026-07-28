# Revenue Assurance Investigation Agent

A Snowflake CoCo CLI oriented revenue assurance workflow that detects billing variances, validates commercial evidence, and prepares auditable finance review cases.

Dataset type: fully synthetic. No real customer, contract, invoice, employee, payment, or personally identifiable information is used.

## What Is Implemented

- Three modular Agent Skills for CoCo CLI:
  - `detect-billing-variances`
  - `validate-commercial-evidence`
  - `prepare-finance-review-case`
- Deterministic Snowflake SQL schema, seed data, stored procedures, audit tables, and ground truth.
- Cortex Search document fixtures and setup SQL.
- Streamlit review UI with summary, case queue, and evidence trail.
- Offline deterministic Python engine for testing without Snowflake credentials.
- Evaluation fixtures and metrics.

## Live Validation Status

Environment-independent components are implemented and tested. The setup and verification scripts can now connect to Snowflake when credentials are provided through local environment variables.

Live Snowflake execution must still be run from a configured account. Cortex Code execution is separate from the connector-based scripts and may require account entitlement or usage-limit access.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Fill `.env` with Snowflake credentials when available.

## Local Verification

```bash
python scripts/run_tests.py
python scripts/run_evaluation.py
```

## Snowflake Setup

Preview SQL files:

```bash
python scripts/setup_project.py --dry-run
```

Execute setup after credentials are available:

```bash
python scripts/validate_environment.py
python scripts/setup_project.py
python scripts/verify_database.py
```

The setup script creates the configured warehouse if needed, executes `sql/` files in dependency order, loads synthetic approval documents, and creates the Cortex Search service unless `--skip-search` is passed.

## CoCo CLI Demo

Expected command after CoCo CLI is installed and configured:

```bash
cortex -c hackathon -w . -f prompts/run_q3_investigation.md
```

## Streamlit

Offline fixture mode:

```bash
streamlit run app/app.py
```

Windows helper:

```powershell
scripts\run_dashboard.ps1
```

Unix helper:

```bash
bash scripts/run_dashboard.sh
```

Snowflake-backed mode is used automatically when Snowflake credentials are available.

The offline dashboard has been browser-checked locally at `http://localhost:8501`. It displays Summary, Case Queue, and Evidence Trail tabs from deterministic synthetic fixtures.

Dashboard views:

- Summary: executive metric row and Q3 decision branch cards.
- Case Queue: queue table, focused case detail panel, and review action controls.
- Evidence Trail: selected case detail, audit timeline, agent classification, and recommended human action.

## Expected Q3 Summary

- Gross variance detected: `$16,000`
- Explained variance: `$6,000`
- Suspected leakage pending finance confirmation: `$9,000`
- Evidence conflict requiring resolution: `$1,000`
- Data-quality cases: `1`

## Safety Boundary

The system prepares finance review cases only. It never creates invoices, updates ledgers, sends customer notifications, triggers payments, or changes balances.
