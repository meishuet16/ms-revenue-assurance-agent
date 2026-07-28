from __future__ import annotations

import pathlib
import sys

import streamlit as st

ROOT = pathlib.Path(__file__).resolve().parents[1]
APP_DIR = pathlib.Path(__file__).resolve().parent
sys.path = [
    path
    for path in sys.path
    if pathlib.Path(path or ".").resolve() != APP_DIR
]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

shadowed_app = sys.modules.get("app")
if shadowed_app is not None and not hasattr(shadowed_app, "__path__"):
    sys.modules.pop("app", None)

from app.components.theme import apply_theme, render_hero
from app.views import case_queue, evidence_trail, flow_map, summary


st.set_page_config(page_title="Revenue Assurance Agent", layout="wide")
apply_theme()
render_hero(
    "Revenue Assurance Investigation Agent",
    "Evidence-backed Q3 billing integrity review for finance triage.",
)

tab_summary, tab_queue, tab_evidence, tab_flow = st.tabs(["Summary", "Case Queue", "Evidence Trail", "Flow Map"])
with tab_summary:
    summary.render()
with tab_queue:
    case_queue.render()
with tab_evidence:
    evidence_trail.render()
with tab_flow:
    flow_map.render()
