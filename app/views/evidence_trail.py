from __future__ import annotations

import streamlit as st

from app.components.action_panel import render_action_panel
from app.components.case_detail import render_case_detail
from app.components.evidence_timeline import render_evidence_timeline, render_investigation_trace
from app.components.evidence_summary import render_evidence_summary
from app.components.formatting import format_status
from app.components.section import render_section_header
from app.components.status_badge import status_badge
from app.services.snowflake_service import fetch_cases


def render() -> None:
    render_section_header(
        "Evidence & Decision",
        "03 · Investigation record",
        "Follow the case in the same order a reviewer would: what was checked, what the evidence means, then what still requires a human decision.",
    )
    cases = fetch_cases()
    selected = st.selectbox(
        "Focused evidence record",
        cases,
        format_func=lambda case: f"{case.customer_name} · {case.case_id}",
    )

    st.markdown(
        """
        <div class="ra-status-strip">
          <div><strong>1 · Evidence</strong><br>Pricing, usage, invoice and approval records</div>
          <div><strong>2 · Interpretation</strong><br>Executed checks and classification</div>
          <div><strong>3 · Human decision</strong><br>Finance reviews the recommended next step</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_evidence_summary(selected)

    render_section_header(
        "What the Investigator Checked",
        "Executed path",
        "This is the auditable runtime trace: observable checks and branch decisions, not hidden chain-of-thought.",
    )
    render_investigation_trace(selected)

    left, right = st.columns([1.12, 0.88])
    with left:
        render_section_header("Supporting Evidence", "What we know")
        render_case_detail(selected)
        render_evidence_timeline(selected)

    with right:
        render_section_header("What It Means", "Investigator outcome")
        st.markdown(
            f'''
            <div class="ra-classification-panel">
              <div class="ra-classification-panel__label">Evidence-backed classification</div>
              <div>{status_badge(selected.status)}</div>
              <div class="ra-classification-panel__title">{format_status(selected.status)}</div>
              <div class="ra-classification-panel__copy">{selected.evidence_summary}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )
        render_section_header("What Finance Does Next", "Human authority")
        render_action_panel("Recommended next step", selected.recommended_action)
        st.markdown(
            '<div class="ra-safety-panel"><strong>Decision boundary:</strong> the investigation ends here. No invoice, ledger, payment, balance, or customer action has been executed.</div>',
            unsafe_allow_html=True,
        )
