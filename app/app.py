from __future__ import annotations

import pathlib
import sys

import streamlit as st

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.pages import case_queue, evidence_trail, summary


st.set_page_config(page_title="Revenue Assurance Agent", layout="wide")
st.title("Revenue Assurance Investigation Agent")

tab_summary, tab_queue, tab_evidence = st.tabs(["Summary", "Case Queue", "Evidence Trail"])
with tab_summary:
    summary.render()
with tab_queue:
    case_queue.render()
with tab_evidence:
    evidence_trail.render()

