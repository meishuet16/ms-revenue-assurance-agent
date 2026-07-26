from decimal import Decimal

from app.services.local_engine import CaseStore, InvestigationCase


def test_case_upsert_preserves_case_id_when_classification_changes():
    store = CaseStore()
    first = InvestigationCase.synthetic(
        customer_id="CUST-NOVA",
        affected_period_start="2026-07-01",
        affected_period_end="2026-09-30",
        status="suspected_leakage",
        gross_variance=Decimal("9000.00"),
    )
    second = InvestigationCase.synthetic(
        customer_id="CUST-NOVA",
        affected_period_start="2026-07-01",
        affected_period_end="2026-09-30",
        status="explained_variance",
        gross_variance=Decimal("9000.00"),
    )

    first_id = store.upsert(first)
    second_id = store.upsert(second)

    assert second_id == first_id
    assert store.get(first_id).status == "explained_variance"

