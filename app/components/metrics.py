from __future__ import annotations

import streamlit as st

from app.components.formatting import format_money


def _metric_card(label: str, value: str, helper: str) -> str:
    return f"""
    <div class="ra-metric-card">
      <div class="ra-metric-card__label">{label}</div>
      <div class="ra-metric-card__value">{value}</div>
      <div class="ra-metric-card__helper">{helper}</div>
    </div>
    """


def render_summary_metrics(summary) -> None:
    metrics = [
        ("Gross variance", format_money(summary.gross_variance_detected), "Detected before classification"),
        ("Suspected leakage", format_money(summary.suspected_leakage), "Pending finance confirmation"),
        ("Explained", format_money(summary.explained_variance), "Supported by exception evidence"),
        ("Evidence conflict", format_money(summary.evidence_conflict), "Requires approval resolution"),
        ("Data quality", str(summary.insufficient_data_cases), "Calculation intentionally stopped"),
    ]
    cols = st.columns(len(metrics))
    for col, (label, value, helper) in zip(cols, metrics):
        col.markdown(_metric_card(label, value, helper), unsafe_allow_html=True)
