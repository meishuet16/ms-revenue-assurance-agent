from __future__ import annotations

import streamlit as st

from app.components.case_table import render_case_table
from app.services.review_service import update_review_status
from app.services.snowflake_service import fetch_cases


def render() -> None:
    st.header("Case Queue")
    cases = fetch_cases()
    render_case_table(cases)
    selected = st.selectbox("Case", cases, format_func=lambda case: f"{case.customer_name} - {case.status}")
    reviewed_by = st.text_input("Reviewer", value="finance.reviewer@example.com")
    comment = st.text_area("Review comment", value="Offline review note.")
    cols = st.columns(3)
    if cols[0].button("Accept finding"):
        st.success(update_review_status(selected.case_id or "", "accepted_for_billing_review", reviewed_by, comment))
    if cols[1].button("Dismiss"):
        st.success(update_review_status(selected.case_id or "", "dismissed", reviewed_by, comment))
    if cols[2].button("Assign to data team"):
        st.success(update_review_status(selected.case_id or "", "assigned", reviewed_by, comment))

