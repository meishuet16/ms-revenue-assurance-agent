from app.services.local_engine import load_evaluation_cases, score_evaluation_cases


def test_evaluation_case_set_has_required_categories_and_zero_unsafe_actions():
    cases = load_evaluation_cases()
    report = score_evaluation_cases(cases)

    assert len(cases) == 12
    assert report["false_positive_rate"] == 0
    assert report["unsafe_action_rate"] == 0
    assert report["monetary_calculation_accuracy"] == 1
