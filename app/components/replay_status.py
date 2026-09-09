from __future__ import annotations

import html

import streamlit as st

from app.services.local_engine import InvestigationCase


_STEP_LABELS = {
    "signal": "Detecting variance signal",
    "pricing": "Checking pricing evidence",
    "exception": "Searching commercial exceptions",
    "approval": "Validating approval document",
    "negative": "Checking negative evidence",
    "usage": "Reconciling usage integrity",
    "leakage": "Preparing suspected leakage verdict",
    "explained": "Preparing explained variance verdict",
    "conflict": "Preparing evidence conflict verdict",
    "blocked": "Stopping unsafe monetary classification",
}


def replay_steps(case: InvestigationCase) -> tuple[str, ...]:
    if case.status == "suspected_leakage":
        return ("signal", "pricing", "exception", "negative", "leakage")
    if case.status == "explained_variance":
        return ("signal", "pricing", "exception", "approval", "explained")
    if case.status == "evidence_conflict":
        return ("signal", "pricing", "exception", "approval", "conflict")
    if case.status == "insufficient_data":
        return ("signal", "usage", "blocked")
    return ("signal",)


def build_replay_status_html(case: InvestigationCase, replay_token: int = 0) -> str:
    steps = replay_steps(case)
    total = len(steps)
    duration = 0.85
    labels = []
    for index, step in enumerate(steps, start=1):
        delay = (index - 1) * duration
        labels.append(
            f'<div class="ra-replay-message" style="--delay:{delay:.2f}s">'
            f'<strong>Step {index}/{total}</strong><span>{html.escape(_STEP_LABELS[step])}</span>'
            '</div>'
        )
    completion_delay = total * duration
    return f'''
<div class="ra-replay-status" data-replay-status="{replay_token}">
<style>
@keyframes raReplayMessage {{
  0%, 100% {{opacity:0; transform:translateY(4px)}}
  8%, 78% {{opacity:1; transform:none}}
}}
@keyframes raReplayComplete {{
  0%, 88% {{opacity:0; transform:translateY(4px)}}
  100% {{opacity:1; transform:none}}
}}
@keyframes raReplayProgress {{from {{width:0}} to {{width:100%}}}}
.ra-replay-status {{
  position:relative; overflow:hidden; display:flex; justify-content:space-between; align-items:center;
  gap:14px; min-height:58px; margin:2px 0 12px; padding:10px 13px 12px;
  border:1px solid #d9e2ea; border-radius:11px; background:linear-gradient(135deg,#fff,#f7faff);
  box-shadow:0 5px 18px rgba(16,24,40,.045);
}}
.ra-replay-status__copy {{position:relative; min-height:34px; flex:1}}
.ra-replay-message {{position:absolute; inset:0 auto auto 0; display:flex; flex-direction:column; opacity:0; animation:raReplayMessage .82s var(--delay) ease both}}
.ra-replay-message strong {{font-size:.65rem; color:#155eef; font-weight:900; letter-spacing:.07em; text-transform:uppercase}}
.ra-replay-message span {{font-size:.84rem; color:#182230; font-weight:800; margin-top:2px}}
.ra-replay-complete {{opacity:0; display:flex; align-items:center; gap:8px; color:#067647; font-size:.78rem; font-weight:850; animation:raReplayComplete .5s {completion_delay:.2f}s ease forwards}}
.ra-replay-complete__dot {{width:8px; height:8px; border-radius:50%; background:#12b76a; box-shadow:0 0 0 4px #ecfdf3}}
.ra-replay-progress {{position:absolute; left:0; right:0; bottom:0; height:3px; background:#e4e7ec}}
.ra-replay-progress span {{display:block; height:100%; width:0; background:linear-gradient(90deg,#2e90fa,#7f56d9); animation:raReplayProgress {completion_delay:.2f}s linear forwards}}
@media(max-width:700px) {{.ra-replay-status {{align-items:flex-start; flex-direction:column; min-height:82px}} .ra-replay-complete {{align-self:flex-end}}}}
@media(prefers-reduced-motion:reduce) {{.ra-replay-message {{display:none; animation:none}} .ra-replay-message:last-child {{display:flex; opacity:1}} .ra-replay-complete {{opacity:1; animation:none}} .ra-replay-progress span {{width:100%; animation:none}}}}
</style>
<div class="ra-replay-status__copy">{''.join(labels)}</div>
<div class="ra-replay-complete"><span class="ra-replay-complete__dot"></span>Investigation complete</div>
<div class="ra-replay-progress"><span></span></div>
</div>
'''


def render_replay_status(case: InvestigationCase, replay_token: int = 0) -> None:
    st.markdown(build_replay_status_html(case, replay_token=replay_token), unsafe_allow_html=True)
