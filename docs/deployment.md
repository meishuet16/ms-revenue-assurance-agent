# Deployment

## Recommended Demo Deployment

Deploy the Streamlit review dashboard on Render. The Blueprint is configured for live mode when Snowflake environment variables are provided.

Render Blueprint:

```text
https://dashboard.render.com/blueprints/new?repo=https://github.com/meishuet16/ms-revenue-assurance-agent
```

The repository includes `render.yaml`, which configures:

- Python web service;
- `pip install -r requirements.txt`;
- `streamlit run app/app.py`;
- `SNOWFLAKE_DASHBOARD_MODE=live`;
- Snowflake account, user, and password as private Render environment variables;
- `COMPUTE_WH`, `REVENUE_ASSURANCE`, and `PUBLIC` defaults.

## Expected Public URL

After the Render service is created, copy the generated service URL into the submission form. It will look similar to:

```text
https://ms-revenue-assurance-agent.onrender.com
```

## Live Mode

Live mode reads from Snowflake and writes only human review state:

```text
SNOWFLAKE_DASHBOARD_MODE=live
SNOWFLAKE_ACCOUNT=<your Snowflake account identifier>
SNOWFLAKE_USER=<your Snowflake login name>
SNOWFLAKE_PASSWORD=<Render secret>
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=REVENUE_ASSURANCE
SNOWFLAKE_SCHEMA=PUBLIC
```

Before switching Render to live mode, run locally:

```powershell
python scripts\setup_project.py --warehouse COMPUTE_WH --skip-search
python scripts\verify_database.py --allow-missing-search
```

The setup script materializes demo rows into `investigation_cases` and `case_evidence`, so the deployed dashboard can read live Snowflake case data.

## Fixture Mode

Fixture mode is useful as a fallback if Render should not hold Snowflake secrets:

```text
SNOWFLAKE_DASHBOARD_MODE=fixture
```

Fixture mode is deterministic and safe for public review:

- no Snowflake password or secret is stored in the deployment platform;
- no live write-back action can happen from the public app;
- the dashboard always shows the validated Q3 demo cases;
- the live Snowflake core validation is documented separately in the demo script.

## Switching An Existing Render Deployment

In Render:

1. Open the deployed `ms-revenue-assurance-agent` service.
2. Go to `Environment`.
3. Set `SNOWFLAKE_DASHBOARD_MODE` to `live` or `fixture`.
4. For live mode, add the Snowflake variables above.
5. Click `Manual Deploy` / `Deploy latest commit`.

The public `.onrender.com` URL stays the same after switching modes.

## Local Demo Command

```powershell
python -m streamlit run app/app.py --server.port 8501
```

## Live Snowflake Core Verification

Run locally from PowerShell after setting Snowflake environment variables:

```powershell
python scripts\validate_environment.py
python scripts\setup_project.py --warehouse COMPUTE_WH --skip-search
python scripts\verify_database.py --allow-missing-search
```

Expected final line:

```text
Live Snowflake core database verification passed; Cortex Search validation is pending.
```

## Pending Trial Limitation

The current Snowflake trial account reports:

```text
AI function EMBED_TEXT_768 is not available for trial accounts
```

Therefore Cortex Search should be described as implemented but pending account feature availability.
