from decimal import Decimal
import pathlib

from app.config import Settings
from app.components.flow_map import build_agent_graph_html, build_flow_map_html, flow_map_nodes
from app.components.formatting import format_money, format_status, status_tone
from app.components.setup_readiness import build_setup_readiness_html, next_command, readiness_items
from app.components.status_strip import validation_label
from app.components.theme import THEME_CSS
from app.services.local_engine import run_q3_golden_investigation


def test_dashboard_money_status_and_action_labels_are_stable():
    result = run_q3_golden_investigation()

    assert format_money(Decimal("16000.00")) == "$16,000"
    assert format_money(None) == "-"
    assert format_status("evidence_conflict") == "Evidence conflict"
    assert status_tone("suspected_leakage") == "danger"
    assert result.case_by_customer("CUST-SUMMIT").queue_action == "Assign"


def test_flow_map_visualization_uses_case_data_and_workflow_lanes():
    result = run_q3_golden_investigation()

    nodes = flow_map_nodes(result.cases)
    html = build_flow_map_html(result.cases)

    assert len(nodes) == 4
    assert nodes[0].customer_name == "Nova Retail"
    assert "CASE-NOVA-Q3" in html
    assert "Suspected leakage" in html


def test_animated_agent_graph_replays_executed_evidence_path():
    result = run_q3_golden_investigation()
    brightfarm = result.case_by_customer("CUST-BRIGHTFARM")
    summit = result.case_by_customer("CUST-SUMMIT")

    conflict_html = build_agent_graph_html(brightfarm, replay_token=7)
    blocked_html = build_agent_graph_html(summit, replay_token=8)

    assert "LIVE AGENT REPLAY" in conflict_html
    assert "Approval document" in conflict_html
    assert "Evidence conflict" in conflict_html
    assert "@keyframes raSignal" in conflict_html
    assert "@keyframes raEvidenceFly" in conflict_html
    assert "@keyframes raVerdictReveal" in conflict_html
    assert 'data-node="approval"' in conflict_html
    assert 'data-node="conflict"' in conflict_html
    assert 'data-replay="7"' in conflict_html
    assert "Evidence entering decision context" in conflict_html
    assert "Auditable decision context" in conflict_html
    assert "not hidden chain-of-thought" in conflict_html
    assert "Insufficient data" in blocked_html
    assert 'data-node="usage"' in blocked_html
    assert "Human review remains final authority" in blocked_html


def test_flow_map_view_exposes_replay_control():
    source = (pathlib.Path(__file__).resolve().parents[1] / "app" / "views" / "flow_map.py").read_text(
        encoding="utf-8"
    )

    assert "▶ Replay Investigation" in source
    assert 'st.session_state["agent_replay_token"]' in source
    assert "replay_token=st.session_state" in source
    assert "does not expose hidden chain-of-thought" in source


def test_dashboard_tabs_target_current_streamlit_dom():
    assert 'div[data-testid="stTabs"] div[role="tab"]' in THEME_CSS
    assert '[data-testid="stTab"][data-selected="true"]' in THEME_CSS
    assert "white-space: nowrap" in THEME_CSS


def test_review_action_inputs_keep_text_visible():
    assert 'div[data-testid="stTextInput"] input' in THEME_CSS
    assert 'div[data-testid="stTextArea"] textarea' in THEME_CSS
    assert "color: var(--ra-ink) !important" in THEME_CSS
    assert "-webkit-text-fill-color: var(--ra-ink)" in THEME_CSS
    assert 'div[data-testid="stTextArea"] label p' in THEME_CSS


def test_dashboard_hero_reflects_core_snowflake_validation():
    source = (pathlib.Path(__file__).resolve().parents[1] / "app" / "components" / "theme.py").read_text(
        encoding="utf-8"
    )

    assert "Snowflake core verified" in source
    assert "Snowflake validation pending" not in source
    assert "Finance review workbench" in source
    assert "Offline synthetic fixtures" not in source


def test_review_action_ui_shows_loading_and_refreshes_live_state():
    source = (pathlib.Path(__file__).resolve().parents[1] / "app" / "views" / "case_queue.py").read_text(
        encoding="utf-8"
    )

    assert 'st.spinner("Updating review status...")' in source
    assert 'st.session_state["review_action_message"]' in source
    assert "st.rerun()" in source


def test_validation_label_reflects_dashboard_mode_without_live_connection():
    fixture_mode = Settings.from_env({})
    live_mode = Settings.from_env({"SNOWFLAKE_DASHBOARD_MODE": "live"})

    assert validation_label(fixture_mode) == "offline fixtures"
    assert validation_label(live_mode) == "live Snowflake requested"


def test_setup_readiness_reports_fixture_mode_and_redacted_next_command():
    settings = Settings.from_env({})
    env = {}

    items = readiness_items(settings, env)
    html = build_setup_readiness_html(settings, env)

    assert ("Dashboard mode", "Fixture mode", "fixture is safest until live validation passes") in items
    assert "python scripts\\validate_environment.py" == next_command(settings)
    assert "Setup readiness" in html
    assert "Live demo controls" in html


def test_setup_readiness_moves_to_setup_command_when_credentials_exist():
    settings = Settings.from_env(
        {
            "SNOWFLAKE_ACCOUNT": "CIZUPDQ-NV95442",
            "SNOWFLAKE_USER": "MEISHUET",
            "SNOWFLAKE_PASSWORD": "secret",
            "SNOWFLAKE_WAREHOUSE": "COMPUTE_WH",
            "SNOWFLAKE_DATABASE": "REVENUE_ASSURANCE",
            "SNOWFLAKE_SCHEMA": "PUBLIC",
        }
    )

    assert next_command(settings) == "python scripts\\setup_project.py --warehouse COMPUTE_WH"
