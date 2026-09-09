from __future__ import annotations

import streamlit as st

from app.components.formatting import format_coverage, format_money
from app.components.metrics import render_summary_metrics
from app.components.outcome_mix import render_outcome_mix
from app.components.section import render_section_header
from app.components.setup_readiness import render_setup_readiness
from app.components.status_strip import render_status_strip
from app.components.status_badge import status_badge
from app.services.snowflake_service import fetch_cases
from app.services.snowflake_service import fetch_summary


def render() -> None:
    summary = fetch_summary()
    render_section_header(
        "Investigation Summary",
        "01 · Portfolio signal",
        "Start with the business question: how much variance exists, and how much of it still needs finance attention?",
    )
    st.markdown(
        f"""
        <div class="ra-hero">
          <div class="ra-hero__eyebrow">Q3 2026 revenue assurance</div>
          <div class="ra-hero__title">{format_money(summary.gross_variance_detected)} detected · {format_money(summary.suspected_leakage)} still needs finance confirmation</div>
          <div class="ra-hero__copy">Not every variance is leakage. The investigator separates approved concessions, evidence conflicts, and data-quality blockers before a human reviews the case.</div>
          <div class="ra-hero__chips">
            <span>{format_money(summary.explained_variance)} explained</span>
            <span>{format_money(summary.evidence_conflict)} evidence conflict</span>
            <span>{summary.insufficient_data_cases} data-quality case</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_status_strip()
    render_summary_metrics(summary)
    render_outcome_mix(summary)

    render_section_header(
        "Q3 Decision Branches",
        "02 · Where attention goes next",
        "Each card is a different investigation outcome, not just another row in a variance report.",
    )
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
              <div class="ra-branch-card__action">Next: {case.queue_action}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_section_header(
        "Environment Readiness",
        "03 · Demo context",
        "The investigation can run deterministically in fixture mode; live Snowflake readiness is shown separately so demo state is never ambiguous.",
    )
    render_setup_readiness()
    st.markdown(
        '<div class="ra-note">Fixture mode is deterministic for public review. Snowflake core validation has passed; Cortex Search remains dependent on trial-account feature availability.</div>',
        unsafe_allow_html=True,
    )
