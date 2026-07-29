from __future__ import annotations

import pathlib
import sys
import argparse
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.snowflake_service import connect  # noqa: E402
from scripts.setup_project import print_snowflake_error  # noqa: E402


EXPECTED_TABLES = [
    "CONTRACTS",
    "PRICING_TERMS",
    "USAGE_RECORDS",
    "INVOICES",
    "INVOICE_LINES",
    "COMMERCIAL_EXCEPTIONS",
    "INVESTIGATION_RUNS",
    "INVESTIGATION_CASES",
    "CASE_EVIDENCE",
    "AGENT_TOOL_CALLS",
    "APPROVAL_DOCUMENTS",
]

EXPECTED_PROCEDURES = [
    "SCAN_BILLING_VARIANCES",
    "GET_PRICING_EVIDENCE",
    "GET_COMMERCIAL_EXCEPTIONS",
    "CREATE_INVESTIGATION_CASE",
    "ADD_CASE_EVIDENCE",
    "UPDATE_CASE_REVIEW_STATUS",
    "START_INVESTIGATION_RUN",
    "LOG_AGENT_TOOL_CALL",
]


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class VerificationResult:
    checks: list[Check]

    @property
    def ok(self) -> bool:
        return all(check.ok for check in self.checks)


def fetch_scalar(cursor: object, sql: str) -> object:
    cursor.execute(sql)
    row = cursor.fetchone()
    return row[0] if row else None


def object_exists(cursor: object, object_type: str, object_name: str) -> bool:
    if object_type == "TABLE":
        sql = (
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES "
            f"WHERE TABLE_SCHEMA = CURRENT_SCHEMA() AND TABLE_NAME = '{object_name}'"
        )
    elif object_type == "VIEW":
        sql = (
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.VIEWS "
            f"WHERE TABLE_SCHEMA = CURRENT_SCHEMA() AND TABLE_NAME = '{object_name}'"
        )
    elif object_type == "PROCEDURE":
        sql = (
            "SELECT COUNT(*) FROM INFORMATION_SCHEMA.PROCEDURES "
            f"WHERE PROCEDURE_SCHEMA = CURRENT_SCHEMA() AND PROCEDURE_NAME = '{object_name}'"
        )
    else:
        raise ValueError(f"Unsupported object type: {object_type}")
    return bool(fetch_scalar(cursor, sql))


def cortex_search_exists(cursor: object) -> bool:
    cursor.execute("SHOW CORTEX SEARCH SERVICES LIKE 'SEARCH_APPROVAL_DOCUMENTS'")
    return cursor.fetchone() is not None


def verify_database(connection: object, allow_missing_search: bool = False) -> VerificationResult:
    checks: list[Check] = []
    with connection.cursor() as cursor:
        for table in EXPECTED_TABLES:
            ok = object_exists(cursor, "TABLE", table)
            checks.append(Check(f"table {table.lower()}", ok, "present" if ok else "missing"))

        for procedure in EXPECTED_PROCEDURES:
            ok = object_exists(cursor, "PROCEDURE", procedure)
            checks.append(Check(f"procedure {procedure.lower()}", ok, "present" if ok else "missing"))

        view_ok = object_exists(cursor, "VIEW", "Q3_2026_GROUND_TRUTH")
        checks.append(Check("view q3_2026_ground_truth", view_ok, "present" if view_ok else "missing"))

        try:
            search_ok = cortex_search_exists(cursor)
            if search_ok:
                checks.append(Check("cortex search search_approval_documents", True, "present"))
            elif allow_missing_search:
                checks.append(
                    Check(
                        "cortex search search_approval_documents",
                        True,
                        "pending: missing because Cortex Search embeddings may be unavailable on trial accounts",
                    )
                )
            else:
                checks.append(Check("cortex search search_approval_documents", False, "missing"))
        except Exception as exc:
            if allow_missing_search:
                checks.append(
                    Check(
                        "cortex search search_approval_documents",
                        True,
                        f"pending: check failed but allowed for trial accounts: {exc}",
                    )
                )
            else:
                checks.append(Check("cortex search search_approval_documents", False, f"check failed: {exc}"))

        try:
            row_count = fetch_scalar(cursor, "SELECT COUNT(*) FROM q3_2026_ground_truth")
            checks.append(Check("ground truth row count", row_count == 4, f"{row_count} rows"))
        except Exception as exc:
            checks.append(Check("ground truth row count", False, f"query failed: {exc}"))

        try:
            case_count = fetch_scalar(cursor, "SELECT COUNT(*) FROM investigation_cases")
            checks.append(Check("investigation case row count", case_count == 4, f"{case_count} rows"))
        except Exception as exc:
            checks.append(Check("investigation case row count", False, f"query failed: {exc}"))

        try:
            evidence_count = fetch_scalar(cursor, "SELECT COUNT(*) FROM case_evidence")
            checks.append(Check("case evidence row count", int(evidence_count or 0) >= 8, f"{evidence_count} rows"))
        except Exception as exc:
            checks.append(Check("case evidence row count", False, f"query failed: {exc}"))

        try:
            amount = fetch_scalar(cursor, "SELECT SUM(amount) FROM q3_2026_ground_truth")
            checks.append(Check("ground truth total variance", float(amount or 0) == 16000.0, f"{amount} total"))
        except Exception as exc:
            checks.append(Check("ground truth total variance", False, f"query failed: {exc}"))

    return VerificationResult(checks)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-missing-search",
        action="store_true",
        help="Treat missing Cortex Search as pending so trial accounts can validate the core live database.",
    )
    args = parser.parse_args()

    try:
        with connect() as connection:
            result = verify_database(connection, allow_missing_search=args.allow_missing_search)
    except Exception as exc:
        print_snowflake_error(exc)
        return 1

    for check in result.checks:
        status = "PASS" if check.ok else "FAIL"
        print(f"{status} {check.name}: {check.detail}")

    if result.ok:
        if args.allow_missing_search:
            print("Live Snowflake core database verification passed; Cortex Search validation is pending.")
        else:
            print("Live Snowflake database verification passed.")
        return 0
    print("Live Snowflake database verification failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
