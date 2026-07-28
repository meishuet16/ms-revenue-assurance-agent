from __future__ import annotations

from app.components.flow_map import render_flow_map
from app.components.section import render_section_header
from app.services.snowflake_service import fetch_cases


def render() -> None:
    render_section_header(
        "Investigation Flow Map",
        "Visual audit path",
        "Trace each customer from variance detection through evidence validation to finance review outcome.",
    )
    render_flow_map(fetch_cases())
