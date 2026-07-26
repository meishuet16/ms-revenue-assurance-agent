from decimal import Decimal

from app.components.outcome_mix import _percent


def test_outcome_mix_percentages_are_stable():
    assert _percent(Decimal("9000"), Decimal("16000")) == Decimal("56.3")
    assert _percent(Decimal("6000"), Decimal("16000")) == Decimal("37.5")
    assert _percent(Decimal("1000"), Decimal("16000")) == Decimal("6.3")
    assert _percent(Decimal("1"), Decimal("0")) == Decimal("0")
