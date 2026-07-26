CREATE OR REPLACE TABLE contracts (
    contract_id STRING,
    customer_id STRING,
    customer_name STRING,
    billing_model STRING,
    currency STRING DEFAULT 'USD',
    start_date DATE,
    status STRING
);

CREATE OR REPLACE TABLE pricing_terms (
    term_id STRING,
    contract_id STRING,
    term_type STRING,
    value NUMBER(18,6),
    value_type STRING,
    effective_start_date DATE,
    effective_end_date DATE,
    approval_status STRING,
    source_document_id STRING
);

CREATE OR REPLACE TABLE usage_records (
    usage_id STRING,
    customer_id STRING,
    billing_period_start DATE,
    billing_period_end DATE,
    units_used NUMBER(18,2)
);

CREATE OR REPLACE TABLE invoices (
    invoice_id STRING,
    customer_id STRING,
    billing_period_start DATE,
    billing_period_end DATE,
    total_amount NUMBER(18,2)
);

CREATE OR REPLACE TABLE invoice_lines (
    invoice_line_id STRING,
    invoice_id STRING,
    charge_type STRING,
    quantity NUMBER(18,2),
    unit_rate NUMBER(18,6),
    net_amount NUMBER(18,2)
);

CREATE OR REPLACE TABLE commercial_exceptions (
    exception_id STRING,
    customer_id STRING,
    exception_type STRING,
    approved_amount_or_rate NUMBER(18,6),
    effective_start_date DATE,
    effective_end_date DATE,
    approval_status STRING,
    approved_by STRING,
    source_document_id STRING
);

CREATE OR REPLACE TABLE investigation_runs (
    run_id STRING DEFAULT UUID_STRING(),
    review_period_start DATE,
    review_period_end DATE,
    run_status STRING,
    initiated_by STRING,
    started_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    completed_at TIMESTAMP_NTZ
);

CREATE OR REPLACE TABLE investigation_cases (
    case_id STRING,
    customer_id STRING,
    review_period_label STRING,
    review_period_start DATE,
    review_period_end DATE,
    status STRING,
    coverage STRING,
    affected_period_start DATE,
    affected_period_end DATE,
    gross_variance NUMBER(18,2),
    explained_amount NUMBER(18,2),
    unexplained_amount NUMBER(18,2),
    confidence_tier STRING,
    evidence_summary STRING,
    recommended_action STRING,
    review_status STRING DEFAULT 'pending',
    reviewed_by STRING,
    reviewed_at TIMESTAMP_NTZ,
    review_comment STRING,
    run_id STRING,
    finding_key STRING,
    updated_at TIMESTAMP_NTZ,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE case_evidence (
    case_id STRING,
    evidence_type STRING,
    evidence_id STRING,
    evidence_excerpt STRING,
    source_tool STRING,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE OR REPLACE TABLE agent_tool_calls (
    tool_call_id STRING DEFAULT UUID_STRING(),
    run_id STRING,
    case_id STRING,
    tool_name STRING,
    input_summary STRING,
    output_summary STRING,
    call_status STRING,
    called_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

