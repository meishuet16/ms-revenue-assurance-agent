MERGE INTO investigation_runs AS tgt
USING (
    SELECT
        'RUN-Q3-2026-DEMO' AS run_id,
        '2026-07-01'::DATE AS review_period_start,
        '2026-09-30'::DATE AS review_period_end,
        'completed' AS run_status,
        'setup_project.py' AS initiated_by,
        CURRENT_TIMESTAMP() AS completed_at
) AS src
ON tgt.run_id = src.run_id
WHEN MATCHED THEN UPDATE SET
    run_status = src.run_status,
    completed_at = src.completed_at
WHEN NOT MATCHED THEN INSERT (
    run_id, review_period_start, review_period_end, run_status, initiated_by, completed_at
) VALUES (
    src.run_id, src.review_period_start, src.review_period_end, src.run_status, src.initiated_by, src.completed_at
);

MERGE INTO investigation_cases AS tgt
USING (
    SELECT
        'CASE-NOVA-Q3' AS case_id,
        'CUST-NOVA' AS customer_id,
        'Q3 2026' AS review_period_label,
        '2026-07-01'::DATE AS review_period_start,
        '2026-09-30'::DATE AS review_period_end,
        'suspected_leakage' AS status,
        'full_period' AS coverage,
        '2026-07-01'::DATE AS affected_period_start,
        '2026-09-30'::DATE AS affected_period_end,
        9000::NUMBER(18,2) AS gross_variance,
        0::NUMBER(18,2) AS explained_amount,
        9000::NUMBER(18,2) AS unexplained_amount,
        'high' AS confidence_tier,
        'Approved $21,000 monthly fee was active for Q3; invoices remained at $18,000. No contradictory evidence retrieved from indexed sources.' AS evidence_summary,
        'Escalate to finance for billing correction review. The billing system did not apply the active approved pricing term for Q3 2026. Final recoverability remains subject to finance confirmation.' AS recommended_action,
        'RUN-Q3-2026-DEMO' AS run_id,
        'CUST-NOVA|2026-07-01|2026-09-30' AS finding_key
    UNION ALL SELECT
        'CASE-KENSINGTON-Q3', 'CUST-KENSINGTON', 'Q3 2026', '2026-07-01'::DATE, '2026-09-30'::DATE,
        'explained_variance', 'full_period', '2026-07-01'::DATE, '2026-09-30'::DATE,
        6000::NUMBER(18,2), 6000::NUMBER(18,2), 0::NUMBER(18,2), 'medium',
        'Structured retention concession covers Q3 and linked approval email confirms full-period approval.',
        'No billing correction is required. Close the investigation as an approved commercial variance.',
        'RUN-Q3-2026-DEMO', 'CUST-KENSINGTON|2026-07-01|2026-09-30'
    UNION ALL SELECT
        'CASE-BRIGHTFARM-Q3', 'CUST-BRIGHTFARM', 'Q3 2026', '2026-07-01'::DATE, '2026-09-30'::DATE,
        'evidence_conflict', 'partial_period', '2026-08-01'::DATE, '2026-09-30'::DATE,
        1000::NUMBER(18,2), 0::NUMBER(18,2), 1000::NUMBER(18,2), 'needs_investigation',
        'Exception registry marks August and September approved, but linked source document says the extension is conditional and should not be applied yet.',
        'Escalate to finance because the exception registry conflicts with the supporting approval document. Confirm whether CFO approval was completed before treating the amount as leakage or explained variance.',
        'RUN-Q3-2026-DEMO', 'CUST-BRIGHTFARM|2026-08-01|2026-09-30'
    UNION ALL SELECT
        'CASE-SUMMIT-Q3', 'CUST-SUMMIT', 'Q3 2026', '2026-07-01'::DATE, '2026-09-30'::DATE,
        'insufficient_data', 'partial_period', '2026-09-01'::DATE, '2026-09-30'::DATE,
        NULL::NUMBER(18,2), NULL::NUMBER(18,2), NULL::NUMBER(18,2), 'needs_investigation',
        'Two September usage records exist for the same customer and period with conflicting unit values.',
        'Assign to the data quality team. The duplicate and conflicting September usage records must be reconciled before financial calculation or billing review.',
        'RUN-Q3-2026-DEMO', 'CUST-SUMMIT|2026-09-01|2026-09-30'
) AS src
ON tgt.case_id = src.case_id
WHEN MATCHED THEN UPDATE SET
    customer_id = src.customer_id,
    review_period_label = src.review_period_label,
    review_period_start = src.review_period_start,
    review_period_end = src.review_period_end,
    status = src.status,
    coverage = src.coverage,
    affected_period_start = src.affected_period_start,
    affected_period_end = src.affected_period_end,
    gross_variance = src.gross_variance,
    explained_amount = src.explained_amount,
    unexplained_amount = src.unexplained_amount,
    confidence_tier = src.confidence_tier,
    evidence_summary = src.evidence_summary,
    recommended_action = src.recommended_action,
    run_id = src.run_id,
    finding_key = src.finding_key,
    updated_at = CURRENT_TIMESTAMP()
WHEN NOT MATCHED THEN INSERT (
    case_id, customer_id, review_period_label, review_period_start, review_period_end,
    status, coverage, affected_period_start, affected_period_end, gross_variance,
    explained_amount, unexplained_amount, confidence_tier, evidence_summary,
    recommended_action, run_id, finding_key, updated_at
) VALUES (
    src.case_id, src.customer_id, src.review_period_label, src.review_period_start, src.review_period_end,
    src.status, src.coverage, src.affected_period_start, src.affected_period_end, src.gross_variance,
    src.explained_amount, src.unexplained_amount, src.confidence_tier, src.evidence_summary,
    src.recommended_action, src.run_id, src.finding_key, CURRENT_TIMESTAMP()
);

DELETE FROM case_evidence
WHERE case_id IN ('CASE-NOVA-Q3', 'CASE-KENSINGTON-Q3', 'CASE-BRIGHTFARM-Q3', 'CASE-SUMMIT-Q3');

INSERT INTO case_evidence (case_id, evidence_type, evidence_id, evidence_excerpt, source_tool)
SELECT 'CASE-NOVA-Q3', 'pricing_term', 'PT-0142', 'Approved pricing amendment effective 2026-01-01 sets monthly fee to 21000.', 'get_pricing_evidence'
UNION ALL SELECT 'CASE-NOVA-Q3', 'invoice_line', 'IL-NOVA-2026-07', 'Invoice line charged 18000 base fee for July 2026.', 'scan_billing_variances'
UNION ALL SELECT 'CASE-NOVA-Q3', 'document', 'PT-0142', 'Pricing amendment records a 21000 monthly platform fee.', 'search_approval_documents'
UNION ALL SELECT 'CASE-KENSINGTON-Q3', 'exception', 'EX-KEN-Q3', 'Approved retention concession of 2000 per month for Q3 2026.', 'get_commercial_exceptions'
UNION ALL SELECT 'CASE-KENSINGTON-Q3', 'document', 'DOC-0001', 'Approval email confirms the concession was formally approved for the full Q3 period.', 'search_approval_documents'
UNION ALL SELECT 'CASE-BRIGHTFARM-Q3', 'exception', 'EX-BF-AUGSEP', 'Registry marks extension approved by J. Tan for August through September.', 'get_commercial_exceptions'
UNION ALL SELECT 'CASE-BRIGHTFARM-Q3', 'document', 'DOC-0044', 'Extension is approved in principle, subject to CFO final approval. Do not apply it to billing yet.', 'search_approval_documents'
UNION ALL SELECT 'CASE-SUMMIT-Q3', 'usage_record', 'UR-SUMMIT-SEP-A', 'September usage shows 4200 units.', 'scan_billing_variances'
UNION ALL SELECT 'CASE-SUMMIT-Q3', 'usage_record', 'UR-SUMMIT-SEP-B', 'September usage shows 3850 units.', 'scan_billing_variances';
