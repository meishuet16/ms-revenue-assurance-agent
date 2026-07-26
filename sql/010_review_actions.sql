CREATE OR REPLACE PROCEDURE update_case_review_status(
    case_id STRING,
    review_status STRING,
    reviewed_by STRING,
    review_comment STRING
)
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    IF (:review_status NOT IN ('accepted_for_billing_review', 'dismissed', 'assigned')) THEN
        RETURN 'unsupported_review_status';
    END IF;

    UPDATE investigation_cases
    SET review_status = :review_status,
        reviewed_by = :reviewed_by,
        reviewed_at = CURRENT_TIMESTAMP(),
        review_comment = :review_comment,
        updated_at = CURRENT_TIMESTAMP()
    WHERE case_id = :case_id;

    RETURN :case_id;
END;
$$;

