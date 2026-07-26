CREATE OR REPLACE PROCEDURE get_commercial_exceptions(customer_id STRING, period_start DATE, period_end DATE)
RETURNS TABLE (
    exception_id STRING,
    customer_id STRING,
    exception_type STRING,
    approved_amount_or_rate NUMBER(18,6),
    effective_start_date DATE,
    effective_end_date DATE,
    approval_status STRING,
    approved_by STRING,
    source_document_id STRING
)
LANGUAGE SQL
AS
$$
BEGIN
    RETURN TABLE (
        SELECT *
        FROM commercial_exceptions
        WHERE customer_id = :customer_id
          AND effective_start_date <= :period_end
          AND effective_end_date >= :period_start
    );
END;
$$;

