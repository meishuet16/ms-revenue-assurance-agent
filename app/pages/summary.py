from __future__ import annotations

import streamlit as st

from app.components.metrics import render_summary_metrics
from app.services.snowflake_service import fetch_summary


def render() -> None:
    st.header("Investigation Summary")
    render_summary_metrics(fetch_summary())
    st.info("Live Snowflake validation is pending. Offline mode uses deterministic synthetic fixtures.")

