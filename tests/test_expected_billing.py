from decimal import Decimal

from app.services.local_engine import run_q3_golden_investigation


def test_nova_retail_flat_fee_leakage_is_deterministic():
    result = run_q3_golden_investigation()

    nova = result.case_by_customer("CUST-NOVA")

    assert nova.status == "suspected_leakage"
    assert nova.coverage == "full_period"
    assert nova.gross_variance == Decimal("9000.00")
    assert nova.explained_amount == Decimal("0.00")
    assert nova.unexplained_amount == Decimal("9000.00")
    assert nova.confidence_tier == "high"

