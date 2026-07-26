from __future__ import annotations

import streamlit as st

from app.components.formatting import format_coverage, format_date, format_money
from app.components.status_badge import confidence_badge, status_badge


def render_case_detail(case) -> None:
    st.markdown(
        f"""
        <div class="ra-detail-panel">
          <div class="ra-detail-panel__header">
            <div>
              <div class="ra-detail-panel__eyebrow">{case.case_id}</div>
              <div class="ra-detail-panel__title">{case.customer_name}</div>
            </div>
            {status_badge(case.status)}
          </div>
          <div class="ra-detail-grid">
            <div><span>Amount</span><strong>{format_money(case.gross_variance)}</strong></div>
            <div><span>Coverage</span><strong>{format_coverage(case.coverage)}</strong></div>
            <div><span>Period</span><strong>{format_date(case.affected_period_start)} - {format_date(case.affected_period_end)}</strong></div>
            <div><span>Confidence</span><strong>{confidence_badge(case.confidence_tier)}</strong></div>
          </div>
          <div class="ra-detail-panel__summary">{case.evidence_summary}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
