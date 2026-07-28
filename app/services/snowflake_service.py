from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from app.config import settings
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


def fetch_cases() -> list[InvestigationCase]:
    if not settings.live_dashboard_requested:
        return list(run_q3_golden_investigation().cases)
    raise SnowflakeUnavailable("Live Snowflake fetch is pending account validation.")


def fetch_summary():
    return run_q3_golden_investigation().summary
