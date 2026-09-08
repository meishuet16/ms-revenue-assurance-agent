from __future__ import annotations

from html import escape

import streamlit as st


_STATUS_LABELS = {
    "suspected_leakage": "Suspected leakage",
    "explained_variance": "Explained variance",
    "evidence_conflict": "Evidence conflict",
    "insufficient_data": "Insufficient data",
}


def _timeline_item(index: int, title: str, detail: str, source: str) -> str:
    return (
        '<div class="ra-timeline-item">'
        f'<div class="ra-timeline-item__index">{index}</div>'
        '<div class="ra-timeline-item__body">'
        f'<div class="ra-timeline-item__type">{escape(title)}</div>'
        f'<div class="ra-timeline-item__excerpt">{escape(detail)}</div>'
        f'<div class="ra-timeline-item__source"><span>Source</span>{escape(source)}</div>'
        '</div></div>'
    )


def _trace_stage(step: str, index: int, total: int) -> tuple[str, str]:
    lowered = step.lower()
    if index == total or any(token in lowered for token in ("classif", "route", "escalat", "stop", "conclude")):
        return "DECIDE", "Decision"
    if any(token in lowered for token in ("document", "approval", "exception", "conflict", "evidence")):
        return "RESOLVE", "Evidence reasoning"
    if any(token in lowered for token in ("pricing", "usage", "invoice", "term", "check", "search")):
        return "CHECK", "Evidence retrieval"
    return "OBSERVE", "Signal detection"


def build_investigation_trace_html(case) -> str:
    trace = tuple(getattr(case, "investigation_trace", ()) or ())
    if not trace:
        return '<div class="ra-note">No runtime investigation trace is available for this persisted case.</div>'

    status = getattr(case, "status", "unknown")
    status_label = _STATUS_LABELS.get(status, status.replace("_", " ").title())
    evidence = tuple(getattr(case, "evidence", ()) or ())
    confidence = str(getattr(case, "confidence_tier", "not set")).replace("_", " ").title()

    cards: list[str] = []
    total = len(trace)
    for index, step in enumerate(trace, start=1):
        stage, stage_label = _trace_stage(step, index, total)
        state = "is-final" if index == total else ""
        cards.append(
            f'<div class="ra-trace-step {state}">'
            '<div class="ra-trace-rail">'
            f'<div class="ra-trace-index">{index:02d}</div>'
            '<div class="ra-trace-line"></div>'
            '</div>'
            '<div class="ra-trace-card">'
            '<div class="ra-trace-card__top">'
            f'<span class="ra-trace-stage ra-trace-stage--{stage.lower()}">{stage}</span>'
            f'<span class="ra-trace-kind">{escape(stage_label)}</span>'
            '</div>'
            f'<div class="ra-trace-card__copy">{escape(step)}</div>'
            '</div>'
            '</div>'
        )

    evidence_chips = "".join(
        f'<span>{escape(item.evidence_type.replace("_", " ").title())}</span>' for item in evidence
    ) or '<span>No evidence attached</span>'

    return f'''
<style>
.ra-investigation-console {{
  border: 1px solid #d9e2ea; border-radius: 10px; overflow: hidden; background: #fff;
  box-shadow: 0 8px 24px rgba(16,24,40,.06); margin: 4px 0 18px;
}}
.ra-console-head {{
  display:flex; justify-content:space-between; gap:18px; align-items:flex-start;
  padding:16px 18px; border-bottom:1px solid #e4e7ec;
  background:linear-gradient(135deg,#f8fafc 0%,#eef4ff 100%);
}}
.ra-console-eyebrow {{font-size:.7rem;font-weight:900;letter-spacing:.08em;color:#155eef;text-transform:uppercase;}}
.ra-console-title {{font-size:1rem;font-weight:850;color:#111827;margin-top:3px;}}
.ra-console-sub {{font-size:.8rem;color:#667085;margin-top:4px;line-height:1.4;max-width:680px;}}
.ra-console-verdict {{min-width:180px;text-align:right;}}
.ra-console-verdict small {{display:block;color:#667085;font-size:.68rem;text-transform:uppercase;font-weight:800;letter-spacing:.06em;}}
.ra-console-verdict strong {{display:block;color:#111827;font-size:.92rem;margin-top:3px;}}
.ra-console-verdict span {{display:block;color:#667085;font-size:.75rem;margin-top:2px;}}
.ra-console-grid {{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(230px,.75fr);gap:0;}}
.ra-trace-stream {{padding:18px 18px 10px;}}
.ra-trace-step {{display:grid;grid-template-columns:34px 1fr;gap:10px;min-height:86px;}}
.ra-trace-rail {{display:flex;flex-direction:column;align-items:center;}}
.ra-trace-index {{width:28px;height:28px;border-radius:50%;background:#eff4ff;border:1px solid #b2ccff;color:#155eef;display:flex;align-items:center;justify-content:center;font-size:.68rem;font-weight:900;}}
.ra-trace-line {{width:2px;flex:1;background:#d9e2ea;margin-top:5px;}}
.ra-trace-step.is-final .ra-trace-index {{background:#182230;border-color:#182230;color:#fff;}}
.ra-trace-step.is-final .ra-trace-line {{display:none;}}
.ra-trace-card {{border:1px solid #e4e7ec;border-radius:8px;padding:11px 12px;margin-bottom:12px;background:#fff;}}
.ra-trace-step.is-final .ra-trace-card {{border-color:#b2ccff;background:#f8faff;}}
.ra-trace-card__top {{display:flex;align-items:center;gap:8px;margin-bottom:6px;}}
.ra-trace-stage {{font-size:.63rem;font-weight:900;letter-spacing:.07em;border-radius:999px;padding:3px 7px;}}
.ra-trace-stage--observe {{background:#f2f4f7;color:#344054;}}
.ra-trace-stage--check {{background:#eff8ff;color:#175cd3;}}
.ra-trace-stage--resolve {{background:#fffaeb;color:#b54708;}}
.ra-trace-stage--decide {{background:#ecfdf3;color:#067647;}}
.ra-trace-kind {{color:#667085;font-size:.72rem;font-weight:700;}}
.ra-trace-card__copy {{color:#182230;font-size:.86rem;line-height:1.45;}}
.ra-console-side {{border-left:1px solid #e4e7ec;background:#fbfcfe;padding:16px;}}
.ra-console-side__label {{color:#667085;font-size:.67rem;font-weight:900;text-transform:uppercase;letter-spacing:.06em;margin-bottom:7px;}}
.ra-console-side__block {{margin-bottom:17px;}}
.ra-console-side__value {{color:#111827;font-size:.88rem;font-weight:800;line-height:1.35;}}
.ra-console-chips {{display:flex;flex-wrap:wrap;gap:6px;}}
.ra-console-chips span {{border:1px solid #d0d5dd;background:#fff;border-radius:999px;padding:4px 7px;color:#475467;font-size:.69rem;font-weight:700;}}
@media (max-width: 760px) {{
  .ra-console-head {{display:block;}}
  .ra-console-verdict {{text-align:left;margin-top:12px;min-width:0;}}
  .ra-console-grid {{grid-template-columns:1fr;}}
  .ra-console-side {{border-left:0;border-top:1px solid #e4e7ec;}}
}}
</style>
<div class="ra-investigation-console">
  <div class="ra-console-head">
    <div>
      <div class="ra-console-eyebrow">Runtime investigation</div>
      <div class="ra-console-title">Decision path reconstructed from executed checks</div>
      <div class="ra-console-sub">The investigator moves from signal detection to evidence retrieval, resolves commercial context, then stops at a finance-safe classification.</div>
    </div>
    <div class="ra-console-verdict">
      <small>Final verdict</small>
      <strong>{escape(status_label)}</strong>
      <span>{escape(confidence)} confidence</span>
    </div>
  </div>
  <div class="ra-console-grid">
    <div class="ra-trace-stream">{''.join(cards)}</div>
    <div class="ra-console-side">
      <div class="ra-console-side__block">
        <div class="ra-console-side__label">Evidence touched</div>
        <div class="ra-console-chips">{evidence_chips}</div>
      </div>
      <div class="ra-console-side__block">
        <div class="ra-console-side__label">Decision boundary</div>
        <div class="ra-console-side__value">Human finance review remains required before any financial action.</div>
      </div>
      <div class="ra-console-side__block">
        <div class="ra-console-side__label">Execution mode</div>
        <div class="ra-console-side__value">Deterministic local investigation runtime</div>
      </div>
    </div>
  </div>
</div>
'''


def build_evidence_timeline_html(case) -> str:
    items: list[str] = []
    for index, item in enumerate(case.evidence, start=1):
        items.append(
            _timeline_item(
                index,
                item.evidence_type.replace("_", " ").title(),
                f"{item.evidence_id}: {item.evidence_excerpt}",
                item.source_tool,
            )
        )
    return f'<div class="ra-timeline">{"".join(items)}</div>'


def render_investigation_trace(case) -> None:
    st.markdown(build_investigation_trace_html(case), unsafe_allow_html=True)


def render_evidence_timeline(case) -> None:
    st.markdown(build_evidence_timeline_html(case), unsafe_allow_html=True)
