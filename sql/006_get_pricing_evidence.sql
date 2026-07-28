CREATE OR REPLACE PROCEDURE get_pricing_evidence(customer_id STRING, period_start DATE, period_end DATE)
RETURNS TABLE (
    term_id STRING,
    customer_id STRING,
    term_type STRING,
    value NUMBER(18,6),
    effective_start_date DATE,
    effective_end_date DATE,
    approval_status STRING,
    source_document_id STRING
)
LANGUAGE SQL
AS
$$
DECLARE
    pricing_rows RESULTSET DEFAULT (
        SELECT pt.term_id, c.customer_id, pt.term_type, pt.value,
               pt.effective_start_date, pt.effective_end_date,
               pt.approval_status, pt.source_document_id
        FROM pricing_terms pt
        JOIN contracts c ON c.contract_id = pt.contract_id
        WHERE c.customer_id = :customer_id
          AND pt.effective_start_date <= :period_end
          AND COALESCE(pt.effective_end_date, '2999-12-31'::DATE) >= :period_start
    );
BEGIN
    RETURN TABLE(pricing_rows);
END;
$$;
