from __future__ import annotations

import streamlit as st

from app.config import Settings, settings


def validation_label(active_settings: Settings = settings) -> str:
    if active_settings.live_dashboard_requested:
        return "live Snowflake requested"
    return "offline fixtures"


def render_status_strip() -> None:
    validation = validation_label()
    st.markdown(
        f"""
        <div class="ra-status-strip">
          <div><strong>Finance action:</strong> review prepared cases only</div>
          <div><strong>Automation boundary:</strong> no billing, ledger, payment, or customer contact</div>
          <div><strong>Validation:</strong> {validation}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
