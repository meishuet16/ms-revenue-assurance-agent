from __future__ import annotations

import streamlit as st


def render_status_strip() -> None:
    st.markdown(
        """
        <div class="ra-status-strip">
          <div><strong>Finance action:</strong> review prepared cases only</div>
          <div><strong>Automation boundary:</strong> no billing, ledger, payment, or customer contact</div>
          <div><strong>Validation:</strong> live Snowflake pending</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
