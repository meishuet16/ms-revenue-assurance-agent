# Architecture

The primary workflow runs through Snowflake CoCo CLI and three modular Agent Skills.

```text
Finance analyst
  -> CoCo CLI
  -> detect-billing-variances
  -> deterministic Snowflake procedures
  -> validate-commercial-evidence
  -> Cortex Search approval documents
  -> prepare-finance-review-case
  -> investigation tables
  -> Streamlit review UI
```

Financial arithmetic, effective-date checks, duplicate usage detection, and case upsert behavior are deterministic. The LLM may orchestrate and summarize, but it is not the monetary source of truth.

## Implemented Components

- Snowflake DDL and stored procedures in `sql/`.
- Synthetic approval documents and Cortex Search setup in `search/`.
- CoCo CLI prompt files in `prompts/`.
- Agent Skills in `.snowflake/cortex/skills/`.
- Streamlit UI in `app/`.
- Offline deterministic test engine in `app/services/local_engine.py`.

## Pending Live Validation

Snowflake trial account, CoCo CLI connection, warehouse, and Cortex Search service creation are pending.

