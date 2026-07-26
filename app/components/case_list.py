from __future__ import annotations

import streamlit as st

from app.components.formatting import format_money
from app.components.status_badge import status_badge


def render_case_list(cases) -> None:
    cards = []
    for case in cases:
        cards.append(
            f"""
            <div class="ra-case-row ra-case-row--{case.status}">
              <div class="ra-case-row__main">
                <div class="ra-case-row__customer">{case.customer_name}</div>
                <div class="ra-case-row__meta">{case.case_id} · {case.queue_action}</div>
              </div>
              <div class="ra-case-row__side">
                {status_badge(case.status)}
                <div class="ra-case-row__amount">{format_money(case.gross_variance)}</div>
              </div>
            </div>
            """
        )
    st.markdown("".join(cards), unsafe_allow_html=True)
