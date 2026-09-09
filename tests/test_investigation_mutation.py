from copy import deepcopy

from app.services.local_engine import GOLDEN_INPUTS, investigate_record


def test_brightfarm_classification_changes_when_source_approval_changes():
    original = deepcopy(next(record for record in GOLDEN_INPUTS if record["customer_id"] == "CUST-BRIGHTFARM"))

    conflict = investigate_record(original)
    assert conflict.status == "evidence_conflict"

    original["document"] = (
        "DOC-0044",
        "CFO final approval completed. Apply the approved extension to August and September billing.",
        "matching",
    )

    explained = investigate_record(original)

    assert explained.status == "explained_variance"
    assert explained.status != conflict.status
    assert explained.gross_variance == conflict.gross_variance
    assert explained.explained_amount == explained.gross_variance
    assert explained.unexplained_amount == 0
    assert "structured exception agrees with source approval" in explained.investigation_trace


def test_removing_exception_changes_same_variance_to_suspected_leakage():
    original = deepcopy(next(record for record in GOLDEN_INPUTS if record["customer_id"] == "CUST-BRIGHTFARM"))
    original["exception"] = None
    original["document"] = (
        "DOC-0044",
        "No approved commercial exception exists for the billed period.",
        "matching",
    )

    leakage = investigate_record(original)

    assert leakage.status == "suspected_leakage"
    assert leakage.gross_variance is not None
    assert leakage.explained_amount == 0
    assert leakage.unexplained_amount == leakage.gross_variance
    assert "no structured commercial exception found" in leakage.investigation_trace
