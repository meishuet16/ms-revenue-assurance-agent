from __future__ import annotations

import pathlib
import tempfile

from app.config import Settings
from app.services import snowflake_service
from scripts import setup_project, verify_database
from scripts.validate_environment import missing_environment_variables


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
    assert paths[-2].name == "upload_documents.sql"
    assert paths[-1].name == "setup_search_service.sql"


def test_search_sql_uses_configured_warehouse():
    rendered = setup_project.render_sql("WAREHOUSE = RA_WH;", warehouse="COMPUTE_WH")

    assert rendered == "WAREHOUSE = COMPUTE_WH;"


class FakeCursor:
    def __init__(self):
        self.executed: list[str] = []

    def execute(self, sql: str):
        self.executed.append(sql)
        return self

    def fetchone(self):
        sql = self.executed[-1]
        if "COUNT(*) FROM q3_2026_ground_truth" in sql:
            return (4,)
        if "SUM(amount)" in sql:
            return (16000,)
        return (1,)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeConnection:
    def __init__(self):
        self.cursor_instance = FakeCursor()

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
    assert any("SHOW CORTEX SEARCH SERVICES" in sql for sql in connection.cursor_instance.executed)
