from __future__ import annotations

import streamlit as st

from app.components.evidence_card import render_evidence
from app.services.snowflake_service import fetch_cases


def render() -> None:
    st.header("Evidence Trail")
    cases = fetch_cases()
    selected = st.selectbox("Case", cases, format_func=lambda case: f"{case.customer_name} - {case.case_id}")
    st.subheader(selected.customer_name)
    st.write(selected.evidence_summary)
    render_evidence(selected)
    st.subheader("Agent Classification")
    st.write(selected.status.replace("_", " ").title())
    st.subheader("Recommended Human Action")
    st.write(selected.recommended_action)

