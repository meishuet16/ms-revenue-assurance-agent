# Revenue Assurance Investigation Agent

## Purpose

This repository implements the Snowflake CoCo CLI Hackathon revenue assurance workflow described in `docs/implementation-spec.md`.

## Authoritative Specification

`docs/implementation-spec.md` is the source of truth for architecture, behavior, data model, safety boundaries, and demo output.

## Repository Structure

- `.snowflake/cortex/skills/` contains the three modular Agent Skills.
- `sql/` contains deterministic Snowflake setup, seed data, procedures, audit, and ground truth SQL.
- `search/` contains synthetic approval document fixtures and Cortex Search setup.
- `app/` contains the Streamlit review interface and environment-independent local engine.
- `scripts/` contains setup, validation, demo, and evaluation helpers.
- `tests/` contains deterministic Python tests for expected billing, boundaries, classifications, upsert behavior, and evaluation metrics.

## Required Test Commands

```bash
python scripts/run_tests.py
python scripts/run_evaluation.py
```

`pytest tests` is also supported when pytest is installed.

## Snowflake Setup Commands

```bash
python scripts/validate_environment.py
python scripts/setup_project.py --dry-run
python scripts/setup_project.py
python scripts/verify_database.py
```

Live Snowflake validation is pending until account, warehouse, role, Cortex Search, and CoCo CLI access are available.

## CoCo CLI Demo Command

```bash
cortex -c hackathon -w . -f prompts/run_q3_investigation.md
```

The exact executable and flags must be verified against the installed CoCo CLI version before claiming live execution.

## Deterministic Financial Calculation Rule

Financial calculations, effective-date comparisons, and variance amounts must be produced by deterministic SQL or Python tests. LLM output may explain results but must not be treated as the source of truth for monetary values.

## Human Review Boundary

The system must never create invoices, send emails, update ledgers, trigger payments, alter customer balances, or contact customers automatically. Streamlit review actions only update investigation review state.

## No-Secret-Commit Rule

Do not commit credentials, private keys, `.env`, Streamlit secrets, Snowflake passwords, or real customer data.

## No Silent Replacement Rule

Do not silently replace deterministic SQL calculations with LLM arithmetic. If a Snowflake tool is unavailable, mark validation as pending and use local deterministic fixtures only for offline demonstration.

