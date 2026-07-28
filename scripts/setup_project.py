from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import settings  # noqa: E402
from app.services.snowflake_service import connect  # noqa: E402
from app.services.snowflake_service import SnowflakeUnavailable  # noqa: E402


SQL_ORDER = [
    "001_database_setup.sql",
    "002_schema.sql",
    "003_seed_golden_cases.sql",
    "004_seed_evaluation_cases.sql",
    "005_scan_billing_variances.sql",
    "006_get_pricing_evidence.sql",
    "007_get_commercial_exceptions.sql",
    "008_create_investigation_case.sql",
    "009_case_evidence.sql",
    "010_review_actions.sql",
    "011_run_audit.sql",
    "012_ground_truth.sql",
]

SEARCH_SQL_ORDER = [
    "upload_documents.sql",
    "setup_search_service.sql",
]

IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_$]*$")


def quote_identifier(value: str) -> str:
    if not IDENTIFIER_PATTERN.match(value):
        raise ValueError(f"Unsafe Snowflake identifier: {value!r}")
    return value.upper()


def split_sql_statements(sql: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    in_single_quote = False
    in_double_quote = False
    in_dollar_quote = False
    index = 0

    while index < len(sql):
        pair = sql[index : index + 2]
        char = sql[index]

        if pair == "$$" and not in_single_quote and not in_double_quote:
            in_dollar_quote = not in_dollar_quote
            current.append(pair)
            index += 2
            continue

        if char == "'" and not in_double_quote and not in_dollar_quote:
            current.append(char)
            if index + 1 < len(sql) and sql[index + 1] == "'":
                current.append(sql[index + 1])
                index += 2
                continue
            in_single_quote = not in_single_quote
            index += 1
            continue

        if char == '"' and not in_single_quote and not in_dollar_quote:
            in_double_quote = not in_double_quote
            current.append(char)
            index += 1
            continue

        if char == ";" and not in_single_quote and not in_double_quote and not in_dollar_quote:
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
            index += 1
            continue

        current.append(char)
        index += 1

    trailing = "".join(current).strip()
    if trailing:
        statements.append(trailing)
    return statements


def project_sql_paths(root: pathlib.Path, include_search: bool) -> list[pathlib.Path]:
    paths = [root / "sql" / filename for filename in SQL_ORDER]
    if include_search:
        paths.extend(root / "search" / filename for filename in SEARCH_SQL_ORDER)
    return paths


def render_sql(sql: str, warehouse: str) -> str:
    return sql.replace("WAREHOUSE = RA_WH", f"WAREHOUSE = {quote_identifier(warehouse)}")


def execute_sql_files(connection: object, paths: list[pathlib.Path], warehouse: str) -> int:
    warehouse_identifier = quote_identifier(warehouse)
    executed = 0
    with connection.cursor() as cursor:
        cursor.execute(
            f"CREATE WAREHOUSE IF NOT EXISTS {warehouse_identifier} "
            "WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE"
        )
        executed += 1
        cursor.execute(f"USE WAREHOUSE {warehouse_identifier}")
        executed += 1

        for path in paths:
            sql = render_sql(path.read_text(encoding="utf-8"), warehouse=warehouse)
            for statement in split_sql_statements(sql):
                print(f"Executing {path.name}: {statement.splitlines()[0][:90]}")
                cursor.execute(statement)
                executed += 1
    return executed


def snowflake_error_guidance(error: Exception) -> str:
    message = str(error)
    lowered = message.lower()
    if isinstance(error, SnowflakeUnavailable) or "credentials are not configured" in lowered:
        return (
            "Snowflake credentials are not configured. Run `python scripts\\validate_environment.py` "
            "and confirm SNOWFLAKE_PASSWORD has a non-zero length, or set SNOWFLAKE_AUTHENTICATOR=externalbrowser."
        )
    if "404 not found" in lowered and "snowflakecomputing.com" in lowered:
        return (
            "Snowflake rejected the account host. Use the full account identifier from Snowsight, "
            "for example `CIZUPDQ-NV95442`, not only the account locator."
        )
    if "saml identity provider" in lowered or "390190" in lowered:
        return (
            "Snowflake external browser authentication was rejected by the account. Remove "
            "SNOWFLAKE_AUTHENTICATOR and use SNOWFLAKE_PASSWORD, or verify the account supports SSO browser auth."
        )
    if "warehouse" in lowered and ("does not exist" in lowered or "not authorized" in lowered):
        return (
            "The configured warehouse is missing or not authorized. Confirm SNOWFLAKE_WAREHOUSE and role, "
            "or rerun setup with `--warehouse COMPUTE_WH`."
        )
    if "cortex search" in lowered:
        return (
            "Cortex Search setup failed. The core schema may still be usable; rerun setup with `--skip-search` "
            "if Cortex Search is not enabled in this account yet."
        )
    return "Snowflake live operation failed. Check the account, role, warehouse, and Snowflake feature availability."


def print_snowflake_error(error: Exception) -> None:
    print("Snowflake live operation failed.")
    print(f"Error type: {type(error).__name__}")
    print(f"Error summary: {error}")
    print(f"Suggested next step: {snowflake_error_guidance(error)}")


def run_live_setup(paths: list[pathlib.Path], warehouse: str, connect_fn=connect) -> int:
    try:
        with connect_fn() as connection:
            executed = execute_sql_files(connection, paths, warehouse=warehouse)
    except Exception as exc:
        print_snowflake_error(exc)
        return 1
    print(f"Snowflake setup complete. Executed {executed} statements.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-search", action="store_true", help="Skip approval document and Cortex Search setup.")
    parser.add_argument("--warehouse", default=settings.warehouse)
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parents[1]
    paths = project_sql_paths(root, include_search=not args.skip_search)

    for path in paths:
        print(f"-- {path}")
        if args.dry_run:
            preview = render_sql(path.read_text(encoding="utf-8"), warehouse=args.warehouse)
            print(preview[:500].rstrip())
            print()
    if not args.dry_run:
        return run_live_setup(paths, args.warehouse)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
