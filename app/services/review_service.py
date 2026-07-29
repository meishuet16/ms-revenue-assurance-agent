from __future__ import annotations

from app.config import settings
from app.services.snowflake_service import connect


ALLOWED_REVIEW_STATUSES = {
    "accepted_for_billing_review",
    "dismissed",
    "assigned",
}


def update_review_status(case_id: str, review_status: str, reviewed_by: str, review_comment: str) -> str:
    if review_status not in ALLOWED_REVIEW_STATUSES:
        raise ValueError(f"Unsupported review status: {review_status}")
    if not settings.live_dashboard_requested:
        return (
            f"Offline mode: would update {case_id} to {review_status} for {reviewed_by}. "
            "No invoice, ledger, payment, balance, email, or customer action is triggered."
        )
    with connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "CALL update_case_review_status(%s, %s, %s, %s)",
                (case_id, review_status, reviewed_by, review_comment),
            )
            row = cursor.fetchone()
    updated_case = row[0] if row else case_id
    return (
        f"Updated Snowflake review state for {updated_case} to {review_status}. "
        "No invoice, ledger, payment, balance, email, or customer action was triggered."
    )
