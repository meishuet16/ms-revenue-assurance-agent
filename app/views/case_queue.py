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
        "Case Queue",
        "Finance workbench",
        "Prioritize findings, inspect evidence summaries, and record human review state.",
    )
    cases = fetch_cases()
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown('<div class="ra-panel-label">Finance review queue</div>', unsafe_allow_html=True)
        render_case_list(cases)
        with st.expander("Audit table", expanded=False):
            render_case_table(cases)
    with right:
        selected = st.selectbox("Focused case", cases, format_func=lambda case: f"{case.customer_name} - {case.status}")
        render_case_detail(selected)
        render_section_header("Review Action", "Human decision")
        st.markdown(
            """
            <div class="ra-safety-panel">
              Review actions only update investigation review state. They do not create invoices,
              send emails, update ledgers, trigger payments, or change customer balances.
            </div>
            """,
            unsafe_allow_html=True,
        )
        reviewed_by = st.text_input("Reviewer", value="finance.reviewer@example.com")
        comment = st.text_area("Review comment", value="Offline review note.")
        if "review_action_message" in st.session_state:
            st.success(st.session_state["review_action_message"])
        cols = st.columns(3)
        if cols[0].button("Accept finding"):
            _submit_review_action(selected.case_id or "", "accepted_for_billing_review", reviewed_by, comment)
        if cols[1].button("Dismiss"):
            _submit_review_action(selected.case_id or "", "dismissed", reviewed_by, comment)
        if cols[2].button("Assign"):
            _submit_review_action(selected.case_id or "", "assigned", reviewed_by, comment)
