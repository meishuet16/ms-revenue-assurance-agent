from __future__ import annotations

from html import escape

import streamlit as st


def build_evidence_timeline_html(case) -> str:
    items: list[str] = []
    for index, item in enumerate(case.evidence, start=1):
        items.append(
            '<div class="ra-timeline-item">'
            f'<div class="ra-timeline-item__index">{index}</div>'
            '<div class="ra-timeline-item__body">'
            f'<div class="ra-timeline-item__type">{escape(item.evidence_type.replace("_", " ").title())}</div>'
            f'<div class="ra-timeline-item__id">{escape(item.evidence_id)}</div>'
            f'<div class="ra-timeline-item__excerpt">{escape(item.evidence_excerpt)}</div>'
            f'<div class="ra-timeline-item__source"><span>Source tool</span>{escape(item.source_tool)}</div>'
            "</div>"
            "</div>"
        )
    return f'<div class="ra-timeline">{"".join(items)}</div>'


def render_evidence_timeline(case) -> None:
    st.markdown(build_evidence_timeline_html(case), unsafe_allow_html=True)
