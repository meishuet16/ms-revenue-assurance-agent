from __future__ import annotations

import streamlit as st


def render_evidence(case) -> None:
    for item in case.evidence:
        with st.container(border=True):
            st.caption(item.evidence_type.replace("_", " ").title())
            st.write(f"**{item.evidence_id}**")
            st.write(item.evidence_excerpt)
            st.caption(f"Source tool: {item.source_tool}")

