from __future__ import annotations

import streamlit as st


def render_action_panel(title: str, copy: str) -> None:
    st.markdown(
        f"""
        <div class="ra-action-panel">
          <div class="ra-action-panel__label">{title}</div>
          <div class="ra-action-panel__copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
