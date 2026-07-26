from __future__ import annotations

import pandas as pd
import streamlit as st


def render_case_table(cases) -> None:
    rows = [
        {
            "Customer": case.customer_name,
            "Status": case.status.replace("_", " ").title(),
            "Coverage": case.coverage.replace("_", " ").title(),
            "Amount": None if case.gross_variance is None else float(case.gross_variance),
            "Confidence": case.confidence_tier.replace("_", " ").title(),
            "Review status": case.review_status,
        }
        for case in cases
    ]
    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
