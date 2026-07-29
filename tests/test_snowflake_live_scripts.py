from __future__ import annotations

import pathlib
import tempfile
from contextlib import contextmanager

from app.config import Settings
from app.services import review_service, snowflake_service
from app.services.snowflake_service import SnowflakeUnavailable
from scripts import setup_project, verify_database
from scripts.validate_environment import describe_environment, missing_environment_variables


def test_externalbrowser_settings_do_not_require_password_and_trim_values():
    settings = Settings.from_env(
        {
            "SNOWFLAKE_ACCOUNT": "CW23947 ",
            "SNOWFLAKE_USER": "MEISHUET",
            "SNOWFLAKE_AUTHENTICATOR": "externalbrowser",
            "SNOWFLAKE_WAREHOUSE": "COMPUTE_WH",
        }
    )

    assert settings.account == "CW23947"
    assert settings.authenticator == "externalbrowser"
    assert settings.has_snowflake_credentials


def test_validate_environment_accepts_externalbrowser_without_password():
    missing = missing_environment_variables(
        {
            "SNOWFLAKE_ACCOUNT": "CW23947 ",
            "SNOWFLAKE_USER": "MEISHUET",
            "SNOWFLAKE_AUTHENTICATOR": "externalbrowser",
            "SNOWFLAKE_WAREHOUSE": "COMPUTE_WH",
            "SNOWFLAKE_DATABASE": "REVENUE_ASSURANCE",
            "SNOWFLAKE_SCHEMA": "PUBLIC",
        }
    )

    assert missing == []


def test_environment_description_redacts_password_but_reports_length():
    rows = describe_environment(
        {
            "SNOWFLAKE_ACCOUNT": "CIZUPDQ-NV95442",
            "SNOWFLAKE_USER": "MEISHUET",
            "SNOWFLAKE_PASSWORD": "super-secret",
            "SNOWFLAKE_WAREHOUSE": "COMPUTE_WH",
            "SNOWFLAKE_DATABASE": "REVENUE_ASSURANCE",
            "SNOWFLAKE_SCHEMA": "PUBLIC",
            "SNOWFLAKE_DASHBOARD_MODE": "fixture",
        }
    )

    assert "SNOWFLAKE_PASSWORD=<hidden>, length=12" in rows
    assert all("super-secret" not in row for row in rows)
    assert "SNOWFLAKE_ACCOUNT=CIZUPDQ-NV95442, length=15" in rows


def test_snowflake_error_guidance_classifies_common_connection_failures():
    host_error = RuntimeError("404 Not Found: post CW23947.snowflakecomputing.com:443/session/authenticator-request")
    saml_error = RuntimeError("390190 SAML Identity Provider account parameter")
    missing_error = SnowflakeUnavailable("Snowflake credentials are not configured")
    password_error = RuntimeError("250001 (08001): Incorrect username or password was specified.")
    trial_search_error = RuntimeError("399258 (0A000): AI function EMBED_TEXT_768 is not available for trial accounts.")

    assert "account identifier" in setup_project.snowflake_error_guidance(host_error)
    assert "SNOWFLAKE_AUTHENTICATOR" in setup_project.snowflake_error_guidance(saml_error)
    assert "validate_environment.py" in setup_project.snowflake_error_guidance(missing_error)
    assert "password" in setup_project.snowflake_error_guidance(password_error)
    assert "externalbrowser" in setup_project.snowflake_error_guidance(password_error)
    assert "trial accounts" in setup_project.snowflake_error_guidance(trial_search_error)
    assert "--skip-search" in setup_project.snowflake_error_guidance(trial_search_error)


def test_run_live_setup_returns_failure_without_traceback_when_connection_fails():
    def failing_connect():
        raise SnowflakeUnavailable("Snowflake credentials are not configured")

    exit_code = setup_project.run_live_setup([], "COMPUTE_WH", connect_fn=failing_connect)

    assert exit_code == 1


def test_dashboard_uses_offline_fixtures_when_credentials_exist_without_live_mode():
    previous_settings = snowflake_service.settings
    snowflake_service.settings = Settings.from_env(
        {
            "SNOWFLAKE_ACCOUNT": "CIZUPDQ-NV95442",
            "SNOWFLAKE_USER": "MEISHUET",
            "SNOWFLAKE_PASSWORD": "secret",
            "SNOWFLAKE_WAREHOUSE": "COMPUTE_WH",
            "SNOWFLAKE_DATABASE": "REVENUE_ASSURANCE",
            "SNOWFLAKE_SCHEMA": "PUBLIC",
        }
    )
    try:
        cases = snowflake_service.fetch_cases()
    finally:
        snowflake_service.settings = previous_settings

    assert len(cases) == 4
    assert cases[0].case_id == "CASE-NOVA-Q3"


def test_dashboard_live_mode_requires_explicit_opt_in():
    settings = Settings.from_env(
        {
            "SNOWFLAKE_ACCOUNT": "CIZUPDQ-NV95442",
            "SNOWFLAKE_USER": "MEISHUET",
            "SNOWFLAKE_PASSWORD": "secret",
            "SNOWFLAKE_DASHBOARD_MODE": "live",
        }
    )

    assert settings.dashboard_mode == "live"
    assert settings.live_dashboard_requested


class FakeLiveCursor:
    def __init__(self):
        self.executed: list[tuple[str, object | None]] = []
        self._rows: list[tuple[object, ...]] = []
        self._single_row: tuple[object, ...] | None = None

    def execute(self, sql: str, params: object | None = None):
        self.executed.append((sql, params))
        if "FROM investigation_cases" in sql:
            self._rows = [
                (
                    "CASE-NOVA-Q3",
                    "CUST-NOVA",
                    "Nova Retail",
                    "suspected_leakage",
                    "full_period",
                    "2026-07-01",
                    "2026-09-30",
                    9000,
                    0,
                    9000,
                    "high",
                    "Approved pricing was not reflected in invoices.",
                    "Review for billing correction.",
                    "Q3 2026",
                    "2026-07-01",
                    "2026-09-30",
                    "pending",
                    "CUST-NOVA|2026-07-01|2026-09-30",
                )
            ]
        elif "FROM case_evidence" in sql:
            self._rows = [
                ("CASE-NOVA-Q3", "pricing_term", "PT-0142", "Approved monthly fee.", "get_pricing_evidence")
            ]
        elif sql.startswith("CALL update_case_review_status"):
            self._single_row = ("CASE-NOVA-Q3",)
        return self

    def fetchall(self):
        return self._rows

    def fetchone(self):
        return self._single_row

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeLiveConnection:
    def __init__(self):
        self.cursor_instance = FakeLiveCursor()

    def cursor(self):
        return self.cursor_instance


@contextmanager
def fake_live_connect(connection: FakeLiveConnection):
    yield connection


def test_dashboard_live_mode_reads_cases_and_summary_from_snowflake():
    previous_settings = snowflake_service.settings
    previous_connect = snowflake_service.connect
    connection = FakeLiveConnection()
    snowflake_service.settings = Settings.from_env(
        {
            "SNOWFLAKE_ACCOUNT": "CIZUPDQ-NV95442",
            "SNOWFLAKE_USER": "MEISHUET",
            "SNOWFLAKE_PASSWORD": "secret",
            "SNOWFLAKE_DASHBOARD_MODE": "live",
        }
    )
    snowflake_service.connect = lambda: fake_live_connect(connection)
    try:
        cases = snowflake_service.fetch_cases()
        summary = snowflake_service.fetch_summary()
    finally:
        snowflake_service.settings = previous_settings
        snowflake_service.connect = previous_connect

    assert cases[0].case_id == "CASE-NOVA-Q3"
    assert cases[0].customer_name == "Nova Retail"
    assert cases[0].evidence[0].evidence_id == "PT-0142"
    assert summary.suspected_leakage == 9000
    assert any("FROM investigation_cases" in sql for sql, _ in connection.cursor_instance.executed)


def test_live_review_action_calls_snowflake_review_procedure():
    previous_settings = review_service.settings
    previous_connect = review_service.connect
    connection = FakeLiveConnection()
    review_service.settings = Settings.from_env(
        {
            "SNOWFLAKE_ACCOUNT": "CIZUPDQ-NV95442",
            "SNOWFLAKE_USER": "MEISHUET",
            "SNOWFLAKE_PASSWORD": "secret",
            "SNOWFLAKE_DASHBOARD_MODE": "live",
        }
    )
    review_service.connect = lambda: fake_live_connect(connection)
    try:
        message = review_service.update_review_status(
            "CASE-NOVA-Q3",
            "assigned",
            "finance@example.com",
            "Please review.",
        )
    finally:
        review_service.settings = previous_settings
        review_service.connect = previous_connect

    assert "Updated Snowflake review state" in message
    assert connection.cursor_instance.executed[-1][1] == (
        "CASE-NOVA-Q3",
        "assigned",
        "finance@example.com",
        "Please review.",
    )


def test_split_sql_statements_preserves_procedure_body_semicolons():
    sql = """
CREATE TABLE demo (id STRING);
CREATE OR REPLACE PROCEDURE demo_proc()
RETURNS STRING
LANGUAGE SQL
AS
$$
BEGIN
    LET msg := 'hello; still inside body';
    RETURN msg;
END;
$$;
"""

    statements = setup_project.split_sql_statements(sql)

    assert len(statements) == 2
    assert statements[0] == "CREATE TABLE demo (id STRING)"
    assert "hello; still inside body" in statements[1]
    assert statements[1].endswith("$$")


def test_table_returning_sql_procedures_use_resultset_return_pattern():
    root = pathlib.Path(__file__).resolve().parents[1]

    for name in [
        "005_scan_billing_variances.sql",
        "006_get_pricing_evidence.sql",
        "007_get_commercial_exceptions.sql",
    ]:
        source = (root / "sql" / name).read_text(encoding="utf-8")
        assert "RESULTSET DEFAULT" in source
        assert "RETURN TABLE(" in source
        assert "RETURN TABLE (\n        SELECT" not in source
        assert "RETURN TABLE (\n        WITH" not in source


def test_safe_identifier_rejects_unsafe_warehouse_names():
    assert setup_project.quote_identifier("COMPUTE_WH") == "COMPUTE_WH"

    try:
        setup_project.quote_identifier("WH;DROP DATABASE PROD")
    except ValueError as exc:
        assert "Unsafe Snowflake identifier" in str(exc)
    else:
        raise AssertionError("unsafe warehouse name was accepted")


def test_project_sql_files_include_search_after_core_sql():
    root = pathlib.Path(__file__).resolve().parents[1]

    paths = setup_project.project_sql_paths(root, include_search=True)

    assert paths[0].name == "001_database_setup.sql"
    assert "013_materialize_demo_cases.sql" in [path.name for path in paths]
    assert paths[-3].name == "013_materialize_demo_cases.sql"
    assert paths[-2].name == "upload_documents.sql"
    assert paths[-1].name == "setup_search_service.sql"


def test_render_blueprint_supports_live_mode_without_committed_secrets():
    root = pathlib.Path(__file__).resolve().parents[1]
    source = (root / "render.yaml").read_text(encoding="utf-8")

    assert "SNOWFLAKE_DASHBOARD_MODE" in source
    assert "value: live" in source
    assert "SNOWFLAKE_PASSWORD" in source
    assert "sync: false" in source
    assert "CIZUPDQ" not in source


def test_search_sql_uses_configured_warehouse():
    rendered = setup_project.render_sql("WAREHOUSE = RA_WH;", warehouse="COMPUTE_WH")

    assert rendered == "WAREHOUSE = COMPUTE_WH;"


class FakeCursor:
    def __init__(self, search_exists: bool = True):
        self.executed: list[str] = []
        self.search_exists = search_exists

    def execute(self, sql: str):
        self.executed.append(sql)
        return self

    def fetchone(self):
        sql = self.executed[-1]
        if "SHOW CORTEX SEARCH SERVICES" in sql:
            return (1,) if self.search_exists else None
        if "COUNT(*) FROM q3_2026_ground_truth" in sql:
            return (4,)
        if "COUNT(*) FROM investigation_cases" in sql:
            return (4,)
        if "COUNT(*) FROM case_evidence" in sql:
            return (9,)
        if "SUM(amount)" in sql:
            return (16000,)
        return (1,)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeConnection:
    def __init__(self, search_exists: bool = True):
        self.cursor_instance = FakeCursor(search_exists=search_exists)

    def cursor(self):
        return self.cursor_instance


def test_execute_project_setup_creates_and_uses_configured_warehouse():
    with tempfile.TemporaryDirectory() as tmp:
        sql_file = pathlib.Path(tmp) / "001_database_setup.sql"
        sql_file.write_text("CREATE DATABASE IF NOT EXISTS REVENUE_ASSURANCE;", encoding="utf-8")
        connection = FakeConnection()

        count = setup_project.execute_sql_files(
            connection,
            [sql_file],
            warehouse="COMPUTE_WH",
        )

        assert count == 3
        assert connection.cursor_instance.executed[0].startswith("CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH")
        assert connection.cursor_instance.executed[1] == "USE WAREHOUSE COMPUTE_WH"


def test_verify_database_reports_required_object_checks():
    connection = FakeConnection()

    result = verify_database.verify_database(connection)

    assert result.ok
    assert any(check.name == "ground truth row count" for check in result.checks)
    assert any(check.name == "investigation case row count" for check in result.checks)
    assert any(check.name == "case evidence row count" for check in result.checks)
    assert any("SHOW CORTEX SEARCH SERVICES" in sql for sql in connection.cursor_instance.executed)


def test_verify_database_can_allow_missing_cortex_search_for_trial_accounts():
    connection = FakeConnection(search_exists=False)

    strict_result = verify_database.verify_database(connection)
    allowed_result = verify_database.verify_database(connection, allow_missing_search=True)

    assert not strict_result.ok
    assert allowed_result.ok
    search_check = next(check for check in allowed_result.checks if check.name == "cortex search search_approval_documents")
    assert search_check.ok
    assert "pending" in search_check.detail
