from decimal import Decimal

from app.services.local_engine import run_q3_golden_investigation


def test_q3_summary_separates_amount_categories():
    result = run_q3_golden_investigation()

    assert result.summary.gross_variance_detected == Decimal("16000.00")
    assert result.summary.explained_variance == Decimal("6000.00")
    assert result.summary.suspected_leakage == Decimal("9000.00")
    assert result.summary.evidence_conflict == Decimal("1000.00")
    assert result.summary.insufficient_data_cases == 1

