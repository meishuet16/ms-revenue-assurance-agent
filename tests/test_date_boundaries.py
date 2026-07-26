from decimal import Decimal

from app.services.local_engine import run_q3_golden_investigation


def test_brightfarm_conflict_only_affects_august_through_september():
    result = run_q3_golden_investigation()

    brightfarm = result.case_by_customer("CUST-BRIGHTFARM")

    assert brightfarm.status == "evidence_conflict"
    assert brightfarm.coverage == "partial_period"
    assert brightfarm.affected_period_start.isoformat() == "2026-08-01"
    assert brightfarm.affected_period_end.isoformat() == "2026-09-30"
    assert brightfarm.gross_variance == Decimal("1000.00")

