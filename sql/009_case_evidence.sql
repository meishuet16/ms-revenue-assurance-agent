CREATE OR REPLACE PROCEDURE add_case_evidence(
    case_id STRING,
    evidence_type STRING,
    evidence_id STRING,
    evidence_excerpt STRING,
    source_tool STRING
)
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    INSERT INTO case_evidence VALUES (
        :case_id,
        :evidence_type,
        :evidence_id,
        :evidence_excerpt,
        :source_tool,
        CURRENT_TIMESTAMP()
    );
    RETURN :case_id;
END;
$$;

