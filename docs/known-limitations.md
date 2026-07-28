# Known Limitations

The MVP supports:

- flat monthly pricing;
- single-rate usage billing;
- one currency;
- synthetic cleaned text documents;
- manual CLI investigation trigger;
- human review.

The MVP does not support:

- tiered pricing;
- proration;
- multiple currencies;
- tax;
- OCR;
- ERP integration;
- invoice generation;
- customer notification;
- payment action;
- legal determination of recoverability.

Live Snowflake core validation has passed for warehouse access, role access, SQL setup execution, approval document fixture loading, stored procedures, and Q3 ground truth verification.

Cortex Search service creation remains pending in the current Snowflake trial account because the account reports `AI function EMBED_TEXT_768 is not available for trial accounts`.

CoCo CLI end-to-end execution remains dependent on local Cortex Code account entitlement and usage limits.

The offline deterministic engine, tests, evaluation script, and Streamlit fixture-mode dashboard are available without Snowflake credentials.
