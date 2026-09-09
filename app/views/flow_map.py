from __future__ import annotations

import streamlit as st

from app.components.flow_map import render_agent_graph, render_flow_map
from app.components.replay_status import render_replay_status
from app.components.section import render_section_header
from app.services.snowflake_service import fetch_cases


def render() -> None:
    render_section_header(
        "Agent Investigation Graph",
        "Replayable decision path",
        "Replay the executed branch from variance signal to evidence checks and the final human-review verdict.",
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
        st.caption("Replays auditable runtime state: visited checks, evidence, branch changes, and final verdict. It does not expose hidden chain-of-thought.")

    replay_token = st.session_state["agent_replay_token"]
    render_replay_status(selected, replay_token=replay_token)
    render_agent_graph(selected, replay_token=replay_token)

    render_section_header(
        "Portfolio Outcomes",
        "All Q3 cases",
        "The focused replay explains one adaptive path; the cards below keep the complete review queue visible.",
    )
    render_flow_map(cases)
