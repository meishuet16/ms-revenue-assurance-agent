from __future__ import annotations

import streamlit as st

from app.components.formatting import format_money


def render_summary_metrics(summary) -> None:
    cols = st.columns(5)
    cols[0].metric("Gross variance", format_money(summary.gross_variance_detected))
    cols[1].metric("Explained", format_money(summary.explained_variance))
    cols[2].metric("Suspected leakage", format_money(summary.suspected_leakage))
    cols[3].metric("Evidence conflict", format_money(summary.evidence_conflict))
    cols[4].metric("Data quality", summary.insufficient_data_cases)
