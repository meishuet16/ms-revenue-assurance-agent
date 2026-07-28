CREATE OR REPLACE PROCEDURE scan_billing_variances(period_start DATE, period_end DATE)
RETURNS TABLE (
    customer_id STRING,
    affected_period_start DATE,
    affected_period_end DATE,
    variance_type STRING,
    gross_variance NUMBER(18,2),
    data_quality_status STRING,
    pricing_term_ids STRING,
    invoice_line_ids STRING
)
LANGUAGE SQL
AS
$$
DECLARE
    variance_rows RESULTSET DEFAULT (
        WITH monthly_expected AS (
            SELECT c.customer_id, i.billing_period_start, i.billing_period_end,
                   MAX(pt.value) AS expected_amount,
                   MAX(i.total_amount) AS actual_amount,
                   LISTAGG(pt.term_id, ',') AS pricing_term_ids,
                   LISTAGG(il.invoice_line_id, ',') AS invoice_line_ids
            FROM contracts c
            JOIN pricing_terms pt ON pt.contract_id = c.contract_id
            JOIN invoices i ON i.customer_id = c.customer_id
            LEFT JOIN invoice_lines il ON il.invoice_id = i.invoice_id
            WHERE i.billing_period_start >= :period_start
              AND i.billing_period_end <= :period_end
              AND pt.approval_status = 'approved'
              AND pt.term_type = 'flat_fee'
              AND pt.effective_start_date <= i.billing_period_start
              AND COALESCE(pt.effective_end_date, '2999-12-31'::DATE) >= i.billing_period_end
            GROUP BY c.customer_id, i.billing_period_start, i.billing_period_end
        ),
        flat_variances AS (
            SELECT customer_id, MIN(billing_period_start) AS affected_period_start,
                   MAX(billing_period_end) AS affected_period_end,
                   'pricing_mismatch' AS variance_type,
                   SUM(expected_amount - actual_amount) AS gross_variance,
                   'clean' AS data_quality_status,
                   LISTAGG(pricing_term_ids, ',') AS pricing_term_ids,
                   LISTAGG(invoice_line_ids, ',') AS invoice_line_ids
            FROM monthly_expected
            WHERE expected_amount <> actual_amount
            GROUP BY customer_id
        ),
        usage_conflicts AS (
            SELECT customer_id, billing_period_start AS affected_period_start,
                   billing_period_end AS affected_period_end,
                   'conflicting_usage_records' AS variance_type,
                   NULL::NUMBER(18,2) AS gross_variance,
                   'conflicting_usage_records' AS data_quality_status,
                   NULL AS pricing_term_ids,
                   NULL AS invoice_line_ids
            FROM usage_records
            WHERE billing_period_start >= :period_start
              AND billing_period_end <= :period_end
            GROUP BY customer_id, billing_period_start, billing_period_end
            HAVING COUNT(*) > 1 AND COUNT(DISTINCT units_used) > 1
        )
        SELECT * FROM flat_variances
        UNION ALL
        SELECT * FROM usage_conflicts
    );
BEGIN
    RETURN TABLE(variance_rows);
END;
$$;
