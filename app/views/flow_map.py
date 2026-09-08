from __future__ import annotations

import streamlit as st

from app.components.flow_map import render_agent_graph, render_flow_map
from app.components.section import render_section_header
from app.services.snowflake_service import fetch_cases


def render() -> None:
    render_section_header(
        "Agent Investigation Graph",
        "Animated decision path",
        "Watch the executed branch light up from variance signal to evidence checks and the final human-review verdict.",
    )
    cases = fetch_cases()
    selected = st.selectbox(
        "Focused investigation",
        cases,
        format_func=lambda case: f"{case.customer_name} · {case.status.replace('_', ' ').title()}",
        key="flow_map_selected_case",
    )
    render_agent_graph(selected)

    render_section_header(
        "Portfolio Outcomes",
        "All Q3 cases",
        "The focused graph explains one adaptive path; the cards below keep the complete review queue visible.",
    )
    render_flow_map(cases)
