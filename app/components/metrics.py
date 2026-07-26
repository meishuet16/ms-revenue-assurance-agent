from __future__ import annotations

import streamlit as st


def money_label(value) -> str:
    if value is None:
        return "-"
    return f"${value:,.0f}"


def render_summary_metrics(summary) -> None:
    cols = st.columns(5)
    cols[0].metric("Gross variance", money_label(summary.gross_variance_detected))
    cols[1].metric("Explained", money_label(summary.explained_variance))
    cols[2].metric("Suspected leakage", money_label(summary.suspected_leakage))
    cols[3].metric("Evidence conflict", money_label(summary.evidence_conflict))
    cols[4].metric("Data quality", summary.insufficient_data_cases)

