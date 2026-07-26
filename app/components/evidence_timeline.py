from __future__ import annotations

import streamlit as st


def render_evidence_timeline(case) -> None:
    items = []
    for index, item in enumerate(case.evidence, start=1):
        items.append(
            f"""
            <div class="ra-timeline-item">
              <div class="ra-timeline-item__index">{index}</div>
              <div class="ra-timeline-item__body">
                <div class="ra-timeline-item__type">{item.evidence_type.replace('_', ' ').title()}</div>
                <div class="ra-timeline-item__id">{item.evidence_id}</div>
                <div class="ra-timeline-item__excerpt">{item.evidence_excerpt}</div>
                <div class="ra-timeline-item__source">Source tool: {item.source_tool}</div>
              </div>
            </div>
            """
        )
    st.markdown(f'<div class="ra-timeline">{"".join(items)}</div>', unsafe_allow_html=True)
