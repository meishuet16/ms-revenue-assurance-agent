from __future__ import annotations

import streamlit as st

from app.components.formatting import format_coverage, format_money, format_status
from app.components.metrics import render_summary_metrics
from app.components.status_badge import status_badge
from app.services.snowflake_service import fetch_cases
from app.services.snowflake_service import fetch_summary


def render() -> None:
    st.header("Investigation Summary")
    render_summary_metrics(fetch_summary())
    st.markdown(
        '<div class="ra-note">Live Snowflake validation is pending. Offline mode uses deterministic synthetic fixtures.</div>',
        unsafe_allow_html=True,
    )
    st.subheader("Q3 2026 Decision Branches")
    cols = st.columns(2)
    for index, case in enumerate(fetch_cases()):
        amount = format_money(case.gross_variance)
        cols[index % 2].markdown(
            f"""
            <div class="ra-branch-card">
              <div class="ra-branch-card__top">
                <strong>{case.customer_name}</strong>
                {status_badge(case.status)}
              </div>
              <div class="ra-branch-card__amount">{amount}</div>
              <div class="ra-branch-card__meta">{format_coverage(case.coverage)} coverage</div>
              <div class="ra-branch-card__copy">{case.evidence_summary}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
