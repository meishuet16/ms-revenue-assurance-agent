# Revenue Assurance Investigation Agent

A Snowflake CoCo CLI oriented revenue assurance workflow that detects billing variances, validates commercial evidence, and prepares auditable finance review cases.

Dataset type: fully synthetic. No real customer, contract, invoice, employee, payment, or personally identifiable information is used.

## Problem Statement

Finance teams can see invoice variance totals, but they often cannot tell quickly whether a variance is recoverable revenue leakage, an approved commercial concession, a data-quality blocker, or a conflict between structured system data and source approval documents. Acting too early can create false billing corrections; acting too late can leave real leakage unresolved.

This project targets **Problem Statement 1: Intelligent Workflow Automation Agent** by automating the investigation workflow around Q3 billing integrity while preserving a human finance review boundary.

## Solution

The Revenue Assurance Investigation Agent combines deterministic financial reconciliation with evidence-aware agent orchestration:

- Snowflake SQL calculates expected billing, actual invoice amounts, variances, and ground-truth demo outcomes.
- CoCo CLI prompt files and modular Agent Skills orchestrate the investigation workflow.
- Cortex Search-ready synthetic approval documents support evidence validation.
- The Streamlit dashboard presents prepared finance review cases, evidence trails, and safe review actions.

The agent does **not** create invoices, update ledgers, contact customers, trigger payments, or change balances. It prepares auditable cases for human review.

## Workflow

1. **Detect** billing variances across pricing terms, usage records, invoice lines, and Q3 review periods.
2. **Validate** commercial evidence by checking approved terms, concessions, exceptions, and supporting documents.
3. **Classify** each finding as suspected leakage, explained variance, evidence conflict, or insufficient data.
4. **Prepare** finance review cases with amounts, evidence citations, confidence tier, and recommended next action.
5. **Review** cases in Streamlit without crossing the automation safety boundary.

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

Dashboard fixture mode is the default, even when Snowflake credentials are present. Set `SNOWFLAKE_DASHBOARD_MODE=live` only after live Snowflake validation passes.

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
