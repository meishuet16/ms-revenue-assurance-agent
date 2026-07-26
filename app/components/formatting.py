from __future__ import annotations

from datetime import date
from decimal import Decimal


STATUS_LABELS = {
    "suspected_leakage": "Suspected leakage",
    "explained_variance": "Explained variance",
    "evidence_conflict": "Evidence conflict",
    "insufficient_data": "Insufficient data",
}

STATUS_TONES = {
    "suspected_leakage": "danger",
    "explained_variance": "success",
    "evidence_conflict": "warning",
    "insufficient_data": "neutral",
}


def format_money(value: Decimal | float | int | None) -> str:
    if value is None:
        return "-"
    return f"${value:,.0f}"


def format_date(value: date) -> str:
    return value.strftime("%b %d, %Y")


def format_status(value: str) -> str:
    return STATUS_LABELS.get(value, value.replace("_", " ").title())


def status_tone(value: str) -> str:
    return STATUS_TONES.get(value, "neutral")


def format_coverage(value: str) -> str:
    return value.replace("_", " ").title()
