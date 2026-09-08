from app.components.evidence_timeline import (
    build_evidence_timeline_html,
    build_investigation_trace_html,
)
from app.services.local_engine import run_q3_golden_investigation


def test_evidence_timeline_html_does_not_create_markdown_code_blocks():
    case = run_q3_golden_investigation().case_by_customer("CUST-NOVA")

    html = build_evidence_timeline_html(case)

    assert "<code>" not in html
    assert "Invoice Line" in html
    assert "Document" in html
    assert html.count('class="ra-timeline-item"') == 3


def test_investigation_console_shows_runtime_path_and_final_verdict():
    case = run_q3_golden_investigation().case_by_customer("CUST-BRIGHTFARM")

    html = build_investigation_trace_html(case)

    assert "Runtime investigation" in html
    assert "Final verdict" in html
    assert "Evidence conflict" in html
    assert "RESOLVE" in html
    assert "DECIDE" in html
    assert html.count('class="ra-trace-step') == len(case.investigation_trace)
