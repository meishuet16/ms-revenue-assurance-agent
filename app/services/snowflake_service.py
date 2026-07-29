from __future__ import annotations

from contextlib import contextmanager
from datetime import date
from decimal import Decimal
from typing import Iterator

from app.config import settings
from app.services.local_engine import Evidence, InvestigationSummary
from app.services.local_engine import InvestigationCase, run_q3_golden_investigation


class SnowflakeUnavailable(RuntimeError):
    pass


@contextmanager
def connect() -> Iterator[object]:
    if not settings.has_snowflake_credentials:
        raise SnowflakeUnavailable("Snowflake credentials are not configured; using offline fixture mode.")
    import snowflake.connector

    connection_args = {
        "account": settings.account,
        "user": settings.user,
        "role": settings.role,
        "warehouse": settings.warehouse,
        "database": settings.database,
        "schema": settings.schema,
    }
    if settings.authenticator:
        connection_args["authenticator"] = settings.authenticator
    if settings.password:
        connection_args["password"] = settings.password

    connection = snowflake.connector.connect(**connection_args)
    try:
        yield connection
    finally:
        connection.close()


def _value(row: object, key: str, index: int) -> object:
    if hasattr(row, "as_dict"):
        return row.as_dict()[key]
    if isinstance(row, dict):
        return row[key]
    return row[index]


def _as_date(value: object) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _as_decimal(value: object) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value)).quantize(Decimal("0.01"))


def _live_cases() -> list[InvestigationCase]:
    query = """
        SELECT
            ic.case_id,
            ic.customer_id,
            COALESCE(c.customer_name, ic.customer_id) AS customer_name,
            ic.status,
            ic.coverage,
            ic.affected_period_start,
            ic.affected_period_end,
            ic.gross_variance,
            ic.explained_amount,
            ic.unexplained_amount,
            ic.confidence_tier,
            ic.evidence_summary,
            ic.recommended_action,
            ic.review_period_label,
            ic.review_period_start,
            ic.review_period_end,
            ic.review_status,
            ic.finding_key
        FROM investigation_cases ic
        LEFT JOIN contracts c ON c.customer_id = ic.customer_id
        ORDER BY
            CASE ic.status
                WHEN 'suspected_leakage' THEN 1
                WHEN 'explained_variance' THEN 2
                WHEN 'evidence_conflict' THEN 3
                ELSE 4
            END,
            ic.customer_id
    """
    evidence_query = """
        SELECT case_id, evidence_type, evidence_id, evidence_excerpt, source_tool
        FROM case_evidence
        ORDER BY case_id, created_at, evidence_type, evidence_id
    """
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.execute(evidence_query)
            evidence_rows = cursor.fetchall()

    evidence_by_case: dict[str, list[Evidence]] = {}
    for row in evidence_rows:
        case_id = str(_value(row, "CASE_ID", 0))
        evidence_by_case.setdefault(case_id, []).append(
            Evidence(
                evidence_type=str(_value(row, "EVIDENCE_TYPE", 1)),
                evidence_id=str(_value(row, "EVIDENCE_ID", 2)),
                evidence_excerpt=str(_value(row, "EVIDENCE_EXCERPT", 3)),
                source_tool=str(_value(row, "SOURCE_TOOL", 4)),
            )
        )

    cases = [
        InvestigationCase(
            case_id=str(_value(row, "CASE_ID", 0)),
            customer_id=str(_value(row, "CUSTOMER_ID", 1)),
            customer_name=str(_value(row, "CUSTOMER_NAME", 2)),
            status=str(_value(row, "STATUS", 3)),
            coverage=str(_value(row, "COVERAGE", 4)),
            affected_period_start=_as_date(_value(row, "AFFECTED_PERIOD_START", 5)),
            affected_period_end=_as_date(_value(row, "AFFECTED_PERIOD_END", 6)),
            gross_variance=_as_decimal(_value(row, "GROSS_VARIANCE", 7)),
            explained_amount=_as_decimal(_value(row, "EXPLAINED_AMOUNT", 8)),
            unexplained_amount=_as_decimal(_value(row, "UNEXPLAINED_AMOUNT", 9)),
            confidence_tier=str(_value(row, "CONFIDENCE_TIER", 10)),
            evidence_summary=str(_value(row, "EVIDENCE_SUMMARY", 11)),
            recommended_action=str(_value(row, "RECOMMENDED_ACTION", 12)),
            review_period_label=str(_value(row, "REVIEW_PERIOD_LABEL", 13)),
            review_period_start=_as_date(_value(row, "REVIEW_PERIOD_START", 14)),
            review_period_end=_as_date(_value(row, "REVIEW_PERIOD_END", 15)),
            review_status=str(_value(row, "REVIEW_STATUS", 16) or "pending"),
            finding_key=str(_value(row, "FINDING_KEY", 17)),
            evidence=tuple(evidence_by_case.get(str(_value(row, "CASE_ID", 0)), [])),
        )
        for row in rows
    ]
    if not cases:
        raise SnowflakeUnavailable(
            "Live dashboard mode found no investigation_cases rows. "
            "Run `python scripts\\setup_project.py --warehouse COMPUTE_WH --skip-search` first."
        )
    return cases


def fetch_cases() -> list[InvestigationCase]:
    if not settings.live_dashboard_requested:
        return list(run_q3_golden_investigation().cases)
    return _live_cases()


def fetch_summary() -> InvestigationSummary:
    cases = fetch_cases() if settings.live_dashboard_requested else list(run_q3_golden_investigation().cases)
    amount = lambda status: sum((case.gross_variance or Decimal("0.00")) for case in cases if case.status == status)
    gross = sum((case.gross_variance or Decimal("0.00")) for case in cases)
    return InvestigationSummary(
        gross_variance_detected=gross,
        explained_variance=amount("explained_variance"),
        suspected_leakage=amount("suspected_leakage"),
        evidence_conflict=amount("evidence_conflict"),
        insufficient_data_cases=sum(1 for case in cases if case.status == "insufficient_data"),
    )
