from decimal import Decimal

from app.config import Settings
from app.components.formatting import format_money, format_status, status_tone
from app.components.status_strip import validation_label
from app.services.local_engine import run_q3_golden_investigation


def test_dashboard_money_status_and_action_labels_are_stable():
    result = run_q3_golden_investigation()

    assert format_money(Decimal("16000.00")) == "$16,000"
    assert format_money(None) == "-"
    assert format_status("evidence_conflict") == "Evidence conflict"
    assert status_tone("suspected_leakage") == "danger"
    assert result.case_by_customer("CUST-SUMMIT").queue_action == "Assign"


def test_validation_label_reflects_dashboard_mode_without_live_connection():
    fixture_mode = Settings.from_env({})
    live_mode = Settings.from_env({"SNOWFLAKE_DASHBOARD_MODE": "live"})

    assert validation_label(fixture_mode) == "offline fixtures"
    assert validation_label(live_mode) == "live Snowflake requested"
