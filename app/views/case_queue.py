from __future__ import annotations

import streamlit as st

from app.components.case_table import render_case_table
from app.components.case_detail import render_case_detail
from app.components.case_list import render_case_list
from app.components.section import render_section_header
from app.config import settings
from app.services.review_service import update_review_status
from app.services.snowflake_service import fetch_cases


def _submit_review_action(case_id: str, review_status: str, reviewed_by: str, comment: str) -> None:
    with st.spinner("Updating review status..."):
        st.session_state["review_action_message"] = update_review_status(case_id, review_status, reviewed_by, comment)
    if settings.live_dashboard_requested:
        st.rerun()


def render() -> None:
    render_section_header(
        "Investigate a Case",
        "02 · Finance workbench",
        "Choose a finding, understand why it was flagged, then record the human review state. The queue is the starting point — not the conclusion.",
    )
    cases = fetch_cases()
    left, right = st.columns([1.25, 1])
    with left:
        st.markdown('<div class="ra-panel-label">Cases needing review</div>', unsafe_allow_html=True)
        render_case_list(cases)
        with st.expander("Open audit table", expanded=False):
            render_case_table(cases)
    with right:
        selected = st.selectbox(
            "Focused case",
            cases,
            format_func=lambda case: f"{case.customer_name} · {case.status.replace('_', ' ').title()}",
        )
        st.markdown(
            f'<div class="ra-note"><strong>Why this case is here:</strong> {selected.evidence_summary}<br><strong>Queue direction:</strong> {selected.queue_action}</div>',
            unsafe_allow_html=True,
        )
        render_case_detail(selected)
        render_section_header(
            "Human Review",
            "Decision boundary",
            "The system has prepared the finding. Any financial consequence still requires a reviewer.",
        )
        st.markdown(
            """
            <div class="ra-safety-panel">
              <strong>No financial action is executed here.</strong><br>
              Review controls only update investigation review state — never invoices, ledgers, payments,
              customer balances, or outbound communication.
            </div>
            """,
            unsafe_allow_html=True,
        )
        reviewed_by = st.text_input("Reviewer", value="finance.reviewer@example.com")
        comment = st.text_area("Review note", value="Offline review note.")
        if "review_action_message" in st.session_state:
            st.success(st.session_state["review_action_message"])
        cols = st.columns(3)
        if cols[0].button("Accept for review", use_container_width=True, type="primary"):
            _submit_review_action(selected.case_id or "", "accepted_for_billing_review", reviewed_by, comment)
        if cols[1].button("Dismiss", use_container_width=True):
            _submit_review_action(selected.case_id or "", "dismissed", reviewed_by, comment)
        if cols[2].button("Assign", use_container_width=True):
            _submit_review_action(selected.case_id or "", "assigned", reviewed_by, comment)
