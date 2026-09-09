from app.components.replay_status import build_replay_status_html, replay_steps
from app.services.local_engine import run_q3_golden_investigation


def test_replay_status_tracks_conflict_path_and_completion():
    case = run_q3_golden_investigation().case_by_customer("CUST-BRIGHTFARM")

    steps = replay_steps(case)
    html = build_replay_status_html(case, replay_token=7)

    assert steps == ("signal", "pricing", "exception", "approval", "conflict")
    assert "Step 1/5" in html
    assert "Step 5/5" in html
    assert "Validating approval document" in html
    assert "Preparing evidence conflict verdict" in html
    assert "Investigation complete" in html
    assert 'data-replay-status="7"' in html


def test_replay_status_shortens_for_data_quality_stop():
    case = run_q3_golden_investigation().case_by_customer("CUST-SUMMIT")

    steps = replay_steps(case)
    html = build_replay_status_html(case)

    assert steps == ("signal", "usage", "blocked")
    assert "Step 3/3" in html
    assert "Stopping unsafe monetary classification" in html
