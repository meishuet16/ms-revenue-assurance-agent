from __future__ import annotations

from html import escape
import streamlit as st


def _timeline_item(index: int, title: str, detail: str, source: str) -> str:
    return (
        '<div class="ra-timeline-item">'
        f'<div class="ra-timeline-item__index">{index}</div>'
        '<div class="ra-timeline-item__body">'
        f'<div class="ra-timeline-item__type">{escape(title)}</div>'
        f'<div class="ra-timeline-item__excerpt">{escape(detail)}</div>'
        f'<div class="ra-timeline-item__source"><span>Source</span>{escape(source)}</div>'
        '</div></div>'
    )


def build_investigation_trace_html(case) -> str:
    trace = getattr(case, "investigation_trace", ())
    if not trace:
        return '<div class="ra-note">No runtime investigation trace is available for this persisted case.</div>'
    items = [_timeline_item(index, "Investigation step", step, "adaptive local investigator") for index, step in enumerate(trace, start=1)]
    return f'<div class="ra-timeline">{"".join(items)}</div>'


def build_evidence_timeline_html(case) -> str:
    items: list[str] = []
    for index, item in enumerate(case.evidence, start=1):
        items.append(_timeline_item(index, item.evidence_type.replace("_", " ").title(), f"{item.evidence_id}: {item.evidence_excerpt}", item.source_tool))
    return f'<div class="ra-timeline">{"".join(items)}</div>'


def render_investigation_trace(case) -> None:
    st.markdown(build_investigation_trace_html(case), unsafe_allow_html=True)


def render_evidence_timeline(case) -> None:
    st.markdown(build_evidence_timeline_html(case), unsafe_allow_html=True)
