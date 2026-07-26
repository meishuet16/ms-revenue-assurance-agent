CREATE OR REPLACE PROCEDURE start_investigation_run(
    review_period_start DATE,
    review_period_end DATE,
    initiated_by STRING
)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    v_run_id STRING;
BEGIN
    v_run_id := UUID_STRING();
    INSERT INTO investigation_runs (run_id, review_period_start, review_period_end, run_status, initiated_by)
    VALUES (:v_run_id, :review_period_start, :review_period_end, 'running', :initiated_by);
    RETURN v_run_id;
END;
$$;

CREATE OR REPLACE PROCEDURE log_agent_tool_call(
    run_id STRING,
    case_id STRING,
    tool_name STRING,
    input_summary STRING,
    output_summary STRING,
    call_status STRING
)
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    INSERT INTO agent_tool_calls (run_id, case_id, tool_name, input_summary, output_summary, call_status)
    VALUES (:run_id, :case_id, :tool_name, :input_summary, :output_summary, :call_status);
    RETURN 'logged';
END;
$$;

