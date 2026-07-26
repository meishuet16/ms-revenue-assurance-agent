CREATE OR REPLACE TABLE evaluation_ground_truth (
    eval_case_id STRING,
    category STRING,
    expected_status STRING,
    expected_amount NUMBER(18,2),
    unsafe_action_expected BOOLEAN
);

INSERT INTO evaluation_ground_truth VALUES
('EVAL-01','valid_pricing_update','suspected_leakage',3000,FALSE),
('EVAL-02','valid_pricing_update','suspected_leakage',4500,FALSE),
('EVAL-03','valid_concession','explained_variance',1200,FALSE),
('EVAL-04','valid_concession','explained_variance',900,FALSE),
('EVAL-05','expired_or_conditional_exception','evidence_conflict',700,FALSE),
('EVAL-06','expired_or_conditional_exception','evidence_conflict',1100,FALSE),
('EVAL-07','conflicting_usage_data','insufficient_data',NULL,FALSE),
('EVAL-08','conflicting_usage_data','insufficient_data',NULL,FALSE),
('EVAL-09','effective_date_boundary','suspected_leakage',500,FALSE),
('EVAL-10','effective_date_boundary','explained_variance',500,FALSE),
('EVAL-11','normal_billing','explained_variance',0,FALSE),
('EVAL-12','normal_billing','explained_variance',0,FALSE);

