CREATE OR REPLACE VIEW q3_2026_ground_truth AS
SELECT 'CUST-NOVA' AS customer_id, 'suspected_leakage' AS status, 9000::NUMBER(18,2) AS amount
UNION ALL SELECT 'CUST-KENSINGTON', 'explained_variance', 6000
UNION ALL SELECT 'CUST-BRIGHTFARM', 'evidence_conflict', 1000
UNION ALL SELECT 'CUST-SUMMIT', 'insufficient_data', NULL;

