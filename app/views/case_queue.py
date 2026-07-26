from __future__ import annotations

import streamlit as st

from app.components.case_table import render_case_table
from app.components.case_detail import render_case_detail
from app.components.case_list import render_case_list
from app.services.review_service import update_review_status
from app.services.snowflake_service import fetch_cases


def render() -> None:
    st.header("Case Queue")
    cases = fetch_cases()
    left, right = st.columns([1.35, 1])
    with left:
        st.caption("Finance review queue")
        render_case_list(cases)
        st.caption("Structured table")
        render_case_table(cases)
    with right:
        selected = st.selectbox("Focused case", cases, format_func=lambda case: f"{case.customer_name} - {case.status}")
        render_case_detail(selected)
        st.subheader("Review Action")
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
        cols = st.columns(3)
        if cols[0].button("Accept finding"):
            st.success(update_review_status(selected.case_id or "", "accepted_for_billing_review", reviewed_by, comment))
        if cols[1].button("Dismiss"):
            st.success(update_review_status(selected.case_id or "", "dismissed", reviewed_by, comment))
        if cols[2].button("Assign"):
            st.success(update_review_status(selected.case_id or "", "assigned", reviewed_by, comment))
