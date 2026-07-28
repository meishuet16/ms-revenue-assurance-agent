from __future__ import annotations

import streamlit as st

from app.components.formatting import format_coverage, format_money, format_status
from app.components.metrics import render_summary_metrics
from app.components.outcome_mix import render_outcome_mix
from app.components.section import render_section_header
from app.components.setup_readiness import render_setup_readiness
from app.components.status_strip import render_status_strip
from app.components.status_badge import status_badge
from app.services.snowflake_service import fetch_cases
from app.services.snowflake_service import fetch_summary


def render() -> None:
    render_section_header(
        "Investigation Summary",
        "Executive overview",
        "Separated outcomes for finance review. Suspected leakage is not combined with evidence conflicts.",
    )
    render_status_strip()
    summary = fetch_summary()
    render_summary_metrics(summary)
    render_setup_readiness()
    render_outcome_mix(summary)
    st.markdown(
        '<div class="ra-note">Dashboard fixture mode is deterministic. Snowflake core validation has passed; Cortex Search is pending on the trial account.</div>',
        unsafe_allow_html=True,
    )
    render_section_header("Q3 2026 Decision Branches", "Case outcomes")
    cols = st.columns(2)
    for index, case in enumerate(fetch_cases()):
        amount = format_money(case.gross_variance)
        cols[index % 2].markdown(
            f"""
            <div class="ra-branch-card ra-branch-card--{case.status}">
              <div class="ra-branch-card__top">
                <strong>{case.customer_name}</strong>
                {status_badge(case.status)}
              </div>
              <div class="ra-branch-card__amount">{amount}</div>
              <div class="ra-branch-card__meta">{format_coverage(case.coverage)} coverage</div>
              <div class="ra-branch-card__copy">{case.evidence_summary}</div>
              <div class="ra-branch-card__action">{case.queue_action}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
