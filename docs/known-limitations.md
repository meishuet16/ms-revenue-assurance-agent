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

Live Snowflake validation is pending configured account access. That includes warehouse and role validation, SQL setup execution, Cortex Search service creation, and CoCo CLI end-to-end execution.

The offline deterministic engine, tests, evaluation script, and Streamlit fixture-mode dashboard are available without Snowflake credentials.
