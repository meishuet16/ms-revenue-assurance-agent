from __future__ import annotations

from app.config import settings


ALLOWED_REVIEW_STATUSES = {
    "accepted_for_billing_review",
    "dismissed",
    "assigned",
}


def update_review_status(case_id: str, review_status: str, reviewed_by: str, review_comment: str) -> str:
    if review_status not in ALLOWED_REVIEW_STATUSES:
        raise ValueError(f"Unsupported review status: {review_status}")
    if not settings.has_snowflake_credentials:
        return (
            f"Offline mode: would update {case_id} to {review_status} for {reviewed_by}. "
            "No invoice, ledger, payment, balance, email, or customer action is triggered."
        )
    return (
        f"Snowflake write-back pending live validation for {case_id}. "
        "The intended action only updates investigation_cases review fields."
    )

