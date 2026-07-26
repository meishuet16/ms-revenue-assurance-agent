from __future__ import annotations

import streamlit as st


def render_section_header(title: str, eyebrow: str, copy: str | None = None) -> None:
    copy_html = f'<div class="ra-section-header__copy">{copy}</div>' if copy else ""
    st.markdown(
        f"""
        <div class="ra-section-header">
          <div>
            <div class="ra-section-header__eyebrow">{eyebrow}</div>
            <div class="ra-section-header__title">{title}</div>
            {copy_html}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
