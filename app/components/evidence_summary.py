from __future__ import annotations

import streamlit as st

from app.components.formatting import format_coverage, format_status


def render_evidence_summary(case) -> None:
    st.markdown(
        f"""
        <div class="ra-evidence-summary">
          <div><span>Evidence items</span><strong>{len(case.evidence)}</strong></div>
          <div><span>Classification</span><strong>{format_status(case.status)}</strong></div>
          <div><span>Coverage</span><strong>{format_coverage(case.coverage)}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
