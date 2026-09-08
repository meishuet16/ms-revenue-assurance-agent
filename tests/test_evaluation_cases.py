from app.services.local_engine import load_evaluation_cases, score_evaluation_cases


def test_evaluation_case_set_scores_runtime_outputs_against_ground_truth():
    cases = load_evaluation_cases()
    report = score_evaluation_cases(cases)

    assert len(cases) == 12
    assert all("expected_status" in case and "actual_status" in case for case in cases)
    assert report["classification_accuracy"] == 1
    assert report["false_positive_rate"] == 0
    assert report["unsafe_action_rate"] == 0
    assert report["monetary_calculation_accuracy"] == 1
    assert report["evidence_citation_completeness"] == 1
