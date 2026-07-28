from decimal import Decimal

from app.config import Settings
from app.components.flow_map import build_flow_map_html, flow_map_nodes
from app.components.formatting import format_money, format_status, status_tone
from app.components.setup_readiness import build_setup_readiness_html, next_command, readiness_items
from app.components.status_strip import validation_label
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
    assert "Detect" in html
    assert "Validate" in html
    assert "Prepare" in html
    assert "CASE-NOVA-Q3" in html
    assert "Suspected leakage" in html


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
