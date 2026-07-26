from __future__ import annotations

import pandas as pd
import streamlit as st

from app.components.formatting import format_coverage, format_money, format_status


def render_case_table(cases) -> None:
    rows = [
        {
            "Customer": case.customer_name,
            "Status": format_status(case.status),
            "Coverage": format_coverage(case.coverage),
            "Amount": format_money(case.gross_variance),
            "Confidence": case.confidence_tier.replace("_", " ").title(),
            "Review status": case.review_status,
        }
        for case in cases
    ]
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
