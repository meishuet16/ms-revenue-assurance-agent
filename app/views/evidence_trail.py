from __future__ import annotations

import streamlit as st

from app.components.case_detail import render_case_detail
from app.components.evidence_timeline import render_evidence_timeline
from app.components.formatting import format_status
from app.components.status_badge import status_badge
from app.services.snowflake_service import fetch_cases


def render() -> None:
    st.header("Evidence Trail")
    cases = fetch_cases()
    selected = st.selectbox("Case", cases, format_func=lambda case: f"{case.customer_name} - {case.case_id}")
    left, right = st.columns([1.1, 1])
    with left:
        render_case_detail(selected)
        st.subheader("Evidence Timeline")
        render_evidence_timeline(selected)
    with right:
        st.markdown(
            f"""
            <div class="ra-classification-panel">
              <div class="ra-classification-panel__label">Agent classification</div>
              <div>{status_badge(selected.status)}</div>
              <div class="ra-classification-panel__title">{format_status(selected.status)}</div>
              <div class="ra-classification-panel__copy">{selected.evidence_summary}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.subheader("Recommended Human Action")
        st.write(selected.recommended_action)
