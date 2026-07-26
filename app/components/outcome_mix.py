from __future__ import annotations

from decimal import Decimal

import streamlit as st

from app.components.formatting import format_money


def _percent(part: Decimal, whole: Decimal) -> Decimal:
    if whole == 0:
        return Decimal("0")
    return (part / whole * Decimal("100")).quantize(Decimal("0.1"))


def render_outcome_mix(summary) -> None:
    total = summary.gross_variance_detected
    suspected = _percent(summary.suspected_leakage, total)
    explained = _percent(summary.explained_variance, total)
    conflict = _percent(summary.evidence_conflict, total)
    st.markdown(
        f"""
        <div class="ra-outcome-mix">
          <div class="ra-outcome-mix__header">
            <div>
              <div class="ra-outcome-mix__eyebrow">Classification mix</div>
              <div class="ra-outcome-mix__title">Q3 variance distribution</div>
            </div>
            <div class="ra-outcome-mix__total">{format_money(total)}</div>
          </div>
          <div class="ra-outcome-mix__bar" aria-label="Outcome mix">
            <span class="ra-outcome-mix__seg ra-outcome-mix__seg--danger" style="width:{suspected}%"></span>
            <span class="ra-outcome-mix__seg ra-outcome-mix__seg--success" style="width:{explained}%"></span>
            <span class="ra-outcome-mix__seg ra-outcome-mix__seg--warning" style="width:{conflict}%"></span>
          </div>
          <div class="ra-outcome-mix__legend">
            <span><i class="danger"></i>Suspected {suspected}%</span>
            <span><i class="success"></i>Explained {explained}%</span>
            <span><i class="warning"></i>Conflict {conflict}%</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
