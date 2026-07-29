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

Environment-independent components are implemented and tested. The setup and verification scripts have connected to Snowflake and validated the core live database path: tables, procedures, approval document fixtures, and Q3 ground truth.

Cortex Search service creation is pending in the current Snowflake trial account because Snowflake reports `AI function EMBED_TEXT_768 is not available for trial accounts`. Cortex Code execution is separate from the connector-based scripts and may require account entitlement or usage-limit access.

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

Expected offline result:

- tests pass through the deterministic Python engine;
- evaluation reports 12 synthetic cases;
- monetary calculation accuracy, classification accuracy, and evidence citation completeness report `1.0`;
- unsafe action rate reports `0`.

These commands do not require Snowflake credentials.

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

Snowflake trial accounts may report `AI function EMBED_TEXT_768 is not available for trial accounts` when creating Cortex Search. In that case, validate the core live database and mark Cortex Search as pending:

```bash
python scripts/setup_project.py --warehouse COMPUTE_WH --skip-search
python scripts/verify_database.py --allow-missing-search
```

## CoCo CLI Demo

Expected command after CoCo CLI is installed and configured:

```bash
cortex -c hackathon -w . -f prompts/run_q3_investigation.md
```

Use this as the primary live workflow demo only after the local CoCo CLI profile is available. If Cortex Code usage or entitlement blocks execution, use the implemented prompt and skills plus the validated Snowflake core database and Streamlit fixture dashboard.

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

Dashboard fixture mode is the default, even when Snowflake credentials are present. Keep fixture mode for the deterministic demo unless live dashboard reads are explicitly enabled and verified.

The offline dashboard has been browser-checked locally at `http://localhost:8501`. It displays Summary, Case Queue, and Evidence Trail tabs from deterministic synthetic fixtures.

Dashboard views:

- Summary: executive metric row and Q3 decision branch cards.
- Case Queue: queue table, focused case detail panel, and review action controls.
- Evidence Trail: selected case detail, audit timeline, agent classification, and recommended human action.
- Flow Map: visual investigation path from variance detection through evidence validation to finance review outcome.

## Deploy

The repo includes a Render Blueprint for a public fixture-mode dashboard:

```text
https://dashboard.render.com/blueprints/new?repo=https://github.com/meishuet16/ms-revenue-assurance-agent
```

After Render creates the service, use the generated `.onrender.com` URL as the prototype deployment link. See `docs/deployment.md` for deployment notes and the live Snowflake validation boundary.

## Expected Q3 Summary

- Gross variance detected: `$16,000`
- Explained variance: `$6,000`
- Suspected leakage pending finance confirmation: `$9,000`
- Evidence conflict requiring resolution: `$1,000`
- Data-quality cases: `1`

## Demo Runbook

Use `docs/demo-script.md` for the presenter sequence. The short path is:

1. Run `python scripts/run_tests.py`.
2. Run `python scripts/run_evaluation.py`.
3. Launch `streamlit run app/app.py`.
4. Walk through Summary, Case Queue, Evidence Trail, and Flow Map using offline fixtures.
5. State that Snowflake core validation passed, Cortex Search is pending on the trial account, and CoCo CLI execution depends on local account entitlement.

Supporting docs:

- `docs/architecture.md` explains the CoCo CLI, Snowflake SQL, Cortex Search, and Streamlit boundaries.
- `docs/evaluation-plan.md` describes the synthetic evaluation cases and metrics.
- `docs/evaluation-report.md` records the current offline deterministic evaluation result.
- `docs/known-limitations.md` lists MVP scope and live validation boundaries.
- `docs/dataset-declaration.md` confirms the dataset is fully synthetic.

## Safety Boundary

The system prepares finance review cases only. It never creates invoices, updates ledgers, sends customer notifications, triggers payments, or changes balances.
