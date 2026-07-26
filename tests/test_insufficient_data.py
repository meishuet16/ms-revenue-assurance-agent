from app.services.local_engine import run_q3_golden_investigation


def test_conflicting_usage_records_stop_monetary_calculation():
    result = run_q3_golden_investigation()

    summit = result.case_by_customer("CUST-SUMMIT")

    assert summit.status == "insufficient_data"
    assert summit.confidence_tier == "needs_investigation"
    assert summit.gross_variance is None
    assert summit.explained_amount is None
    assert summit.unexplained_amount is None
    assert "reconciled before financial calculation" in summit.recommended_action

