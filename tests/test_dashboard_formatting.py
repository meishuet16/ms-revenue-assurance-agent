from decimal import Decimal

from app.components.formatting import format_money, format_status, status_tone
from app.services.local_engine import run_q3_golden_investigation


def test_dashboard_money_status_and_action_labels_are_stable():
    result = run_q3_golden_investigation()

    assert format_money(Decimal("16000.00")) == "$16,000"
    assert format_money(None) == "-"
    assert format_status("evidence_conflict") == "Evidence conflict"
    assert status_tone("suspected_leakage") == "danger"
    assert result.case_by_customer("CUST-SUMMIT").queue_action == "Assign"
