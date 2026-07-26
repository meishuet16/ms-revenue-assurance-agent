CREATE OR REPLACE PROCEDURE create_investigation_case(
    run_id STRING,
    customer_id STRING,
    review_period_label STRING,
    review_period_start DATE,
    review_period_end DATE,
    status STRING,
    coverage STRING,
    affected_period_start DATE,
    affected_period_end DATE,
    gross_variance NUMBER,
    explained_amount NUMBER,
    unexplained_amount NUMBER,
    confidence_tier STRING,
    evidence_summary STRING,
    recommended_action STRING
)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    v_finding_key STRING;
    v_case_id STRING;
BEGIN
    v_finding_key := :customer_id || '|' || TO_VARCHAR(:affected_period_start) || '|' || TO_VARCHAR(:affected_period_end);
    v_case_id := UUID_STRING();

    MERGE INTO investigation_cases AS tgt
    USING (SELECT :v_finding_key AS finding_key) AS src
    ON tgt.finding_key = src.finding_key
    WHEN MATCHED THEN UPDATE SET
        status = :status,
        coverage = :coverage,
        gross_variance = :gross_variance,
        explained_amount = :explained_amount,
        unexplained_amount = :unexplained_amount,
        confidence_tier = :confidence_tier,
        evidence_summary = :evidence_summary,
        recommended_action = :recommended_action,
        run_id = :run_id,
        review_period_label = :review_period_label,
        review_period_start = :review_period_start,
        review_period_end = :review_period_end,
        updated_at = CURRENT_TIMESTAMP()
    WHEN NOT MATCHED THEN INSERT (
        case_id, run_id, customer_id, review_period_label, review_period_start, review_period_end,
        status, coverage, affected_period_start, affected_period_end, gross_variance,
        explained_amount, unexplained_amount, confidence_tier, evidence_summary,
        recommended_action, finding_key, updated_at
    )
    VALUES (
        :v_case_id, :run_id, :customer_id, :review_period_label, :review_period_start, :review_period_end,
        :status, :coverage, :affected_period_start, :affected_period_end, :gross_variance,
        :explained_amount, :unexplained_amount, :confidence_tier, :evidence_summary,
        :recommended_action, :v_finding_key, CURRENT_TIMESTAMP()
    );

    SELECT MAX(case_id) INTO :v_case_id
    FROM investigation_cases
    WHERE finding_key = :v_finding_key;

    RETURN v_case_id;
END;
$$;

