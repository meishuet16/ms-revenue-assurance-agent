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

## Pending Live Validation

The user does not yet have a Snowflake contest trial account. All environment-independent components are implemented. Live Snowflake validation, Cortex Search creation, and CoCo CLI execution are pending.

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
