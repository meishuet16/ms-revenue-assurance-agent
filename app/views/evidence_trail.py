from __future__ import annotations

import streamlit as st

from app.components.action_panel import render_action_panel
from app.components.case_detail import render_case_detail
from app.components.evidence_timeline import render_evidence_timeline, render_investigation_trace
from app.components.evidence_summary import render_evidence_summary
from app.components.formatting import format_status
from app.components.section import render_section_header
from app.components.status_badge import status_badge
from app.services.snowflake_service import fetch_cases


def render() -> None:
    render_section_header("Evidence Trail", "Investigation record", "See what the investigator checked, why its path changed, the evidence it used, and where human review begins.")
    cases = fetch_cases()
    selected = st.selectbox("Case", cases, format_func=lambda case: f"{case.customer_name} - {case.case_id}")
    render_evidence_summary(selected)
    left, right = st.columns([1.1, 1])
    with left:
        render_case_detail(selected)
        render_section_header("Investigation Trace", "Runtime decisions")
        render_investigation_trace(selected)
        render_section_header("Evidence Timeline", "Supporting evidence")
        render_evidence_timeline(selected)
    with right:
        st.markdown(f'''<div class="ra-classification-panel"><div class="ra-classification-panel__label">Investigator classification</div><div>{status_badge(selected.status)}</div><div class="ra-classification-panel__title">{format_status(selected.status)}</div><div class="ra-classification-panel__copy">{selected.evidence_summary}</div></div>''', unsafe_allow_html=True)
        render_section_header("Recommended Human Action", "Review guidance")
        render_action_panel("Finance next step", selected.recommended_action)
