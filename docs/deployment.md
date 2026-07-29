# Deployment

## Recommended Demo Deployment

Deploy the Streamlit review dashboard in fixture mode. This gives judges a stable public prototype without requiring Snowflake credentials in the hosting platform.

Render Blueprint:

```text
https://dashboard.render.com/blueprints/new?repo=https://github.com/meishuet16/ms-revenue-assurance-agent
```

The repository includes `render.yaml`, which configures:

- Python web service;
- `pip install -r requirements.txt`;
- `streamlit run app/app.py`;
- `SNOWFLAKE_DASHBOARD_MODE=fixture`.

## Expected Public URL

After the Render service is created, copy the generated service URL into the submission form. It will look similar to:

```text
https://ms-revenue-assurance-agent.onrender.com
```

## Why Fixture Mode Is Used For Deployment

Fixture mode is deterministic and safe for public review:

- no Snowflake password or secret is stored in the deployment platform;
- no live write-back action can happen from the public app;
- the dashboard always shows the validated Q3 demo cases;
- the live Snowflake core validation is documented separately in the demo script.

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
