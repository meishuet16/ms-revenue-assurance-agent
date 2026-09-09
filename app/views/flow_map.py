from __future__ import annotations

import streamlit as st

from app.components.flow_map import render_agent_graph, render_flow_map
from app.components.replay_status import render_replay_status
from app.components.section import render_section_header
from app.services.snowflake_service import fetch_cases


def render() -> None:
    render_section_header(
        "Replay the Investigation",
        "04 · Agent decision path",
        "Watch the executed branch from the original variance signal through the evidence checks to the final finance handoff.",
    )
    cases = fetch_cases()
    selected = st.selectbox(
        "Focused investigation",
        cases,
        format_func=lambda case: f"{case.customer_name} · {case.status.replace('_', ' ').title()}",
        key="flow_map_selected_case",
    )

    if "agent_replay_token" not in st.session_state:
        st.session_state["agent_replay_token"] = 1

    replay_col, note_col = st.columns([0.32, 0.68])
    with replay_col:
        if st.button("▶ Replay Investigation", use_container_width=True, type="primary"):
            st.session_state["agent_replay_token"] += 1
    with note_col:
        st.markdown(
            '<div class="ra-note"><strong>How to read this:</strong> bright nodes were visited, dim branches were not taken, and evidence cards show what entered the auditable decision context. The replay does not expose hidden chain-of-thought.</div>',
            unsafe_allow_html=True,
        )

    render_replay_status(selected, replay_token=st.session_state["agent_replay_token"])
    render_agent_graph(selected, replay_token=st.session_state["agent_replay_token"])

    st.markdown(
        f"""
        <div class="ra-safety-panel">
          <strong>Investigation complete → Human review required</strong><br>
          Recommended next step: {selected.recommended_action}<br>
          No financial action has been executed.
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_section_header(
        "Portfolio Outcomes",
        "All Q3 cases",
        "The replay above explains one adaptive path. The portfolio below keeps every Q3 outcome visible for comparison.",
    )
    render_flow_map(cases)
