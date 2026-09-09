from __future__ import annotations

import html
from dataclasses import dataclass
from decimal import Decimal

import streamlit as st

from app.components.formatting import format_money, format_status
from app.services.local_engine import InvestigationCase


@dataclass(frozen=True)
class FlowMapNode:
    case_id: str
    customer_name: str
    status: str
    amount: Decimal | None
    evidence_count: int


def flow_map_nodes(cases: tuple[InvestigationCase, ...] | list[InvestigationCase]) -> list[FlowMapNode]:
    return [
        FlowMapNode(
            case_id=case.case_id or case.identity_key(),
            customer_name=case.customer_name,
            status=case.status,
            amount=case.gross_variance,
            evidence_count=len(case.evidence),
        )
        for case in cases
    ]


def _active_path(status: str) -> tuple[str, ...]:
    if status == "suspected_leakage":
        return ("signal", "pricing", "exception", "negative", "leakage")
    if status == "explained_variance":
        return ("signal", "pricing", "exception", "approval", "explained")
    if status == "evidence_conflict":
        return ("signal", "pricing", "exception", "approval", "conflict")
    if status == "insufficient_data":
        return ("signal", "usage", "blocked")
    return ("signal",)


def _node(
    node_id: str,
    stage: str,
    title: str,
    detail: str,
    active_path: tuple[str, ...],
    tone: str = "neutral",
) -> str:
    classes = ["ra-agent-node", f"ra-agent-node--{tone}"]
    if node_id in active_path:
        classes.append("is-active")
        step = active_path.index(node_id) + 1
        classes.append(f"is-step-{step}")
    else:
        classes.append("is-dimmed")
    return (
        f'<div class="{" ".join(classes)}" data-node="{html.escape(node_id)}">'
        f'<div class="ra-agent-node__stage">{html.escape(stage)}</div>'
        f'<div class="ra-agent-node__title">{html.escape(title)}</div>'
        f'<div class="ra-agent-node__detail">{html.escape(detail)}</div>'
        '<div class="ra-agent-node__pulse"></div>'
        '</div>'
    )


def _edge(name: str, from_id: str, to_id: str, active_path: tuple[str, ...]) -> str:
    active = from_id in active_path and to_id in active_path and active_path.index(to_id) == active_path.index(from_id) + 1
    classes = f'ra-agent-edge ra-agent-edge--{name}' + (" is-active" if active else "")
    delay_step = active_path.index(to_id) if active else 0
    return (
        f'<div class="{classes}" style="--edge-delay:{delay_step};">'
        '<span class="ra-agent-edge__track"></span><span class="ra-agent-edge__signal"></span>'
        '</div>'
    )


def _evidence_cards(case: InvestigationCase) -> str:
    evidence = tuple(getattr(case, "evidence", ()) or ())
    if not evidence:
        return '<div class="ra-evidence-card ra-evidence-card--empty">No evidence attached</div>'
    cards: list[str] = []
    for index, item in enumerate(evidence[:4], start=1):
        label = item.evidence_type.replace("_", " ").title()
        cards.append(
            f'<div class="ra-evidence-card" style="--evidence-index:{index};">'
            '<div class="ra-evidence-card__beam"></div>'
            f'<span>{html.escape(label)}</span>'
            f'<strong>{html.escape(item.evidence_id)}</strong>'
            f'<small>{html.escape(item.source_tool)}</small>'
            '</div>'
        )
    return "".join(cards)


def _reasoning_state(case: InvestigationCase) -> tuple[str, str, str]:
    status = case.status
    if status == "suspected_leakage":
        return (
            "No approved exception explains the variance.",
            "Negative commercial evidence confirmed",
            "Escalate suspected leakage for finance confirmation.",
        )
    if status == "explained_variance":
        return (
            "An approved commercial exception may cover the variance.",
            "Approval document matches structured exception",
            "Classify as explained variance; preserve evidence trail.",
        )
    if status == "evidence_conflict":
        return (
            "Structured approval and source evidence disagree.",
            "Source document introduces a conflicting condition",
            "Stop automatic resolution and route evidence conflict to finance.",
        )
    if status == "insufficient_data":
        return (
            "Source usage cannot support safe monetary calculation.",
            "Conflicting usage records detected",
            "Stop calculation and request human reconciliation.",
        )
    return ("Investigation in progress.", "No decisive evidence yet", "Continue evidence retrieval.")


def build_agent_graph_html(case: InvestigationCase, replay_token: int = 0) -> str:
    active_path = _active_path(case.status)
    verdict = format_status(case.status)
    amount = format_money(case.gross_variance)
    trace_count = len(getattr(case, "investigation_trace", ()) or ())
    hypothesis, evidence_state, next_action = _reasoning_state(case)
    evidence_cards = _evidence_cards(case)
    replay_class = " is-replay" if replay_token else ""

    return f'''
<div class="ra-agent-stage{replay_class}" data-replay="{replay_token}">
<style>
@keyframes raGraphEnter {{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes raNodeVisit {{0%{{opacity:.2;transform:scale(.97);box-shadow:none}}55%{{opacity:1;transform:scale(1.015);box-shadow:0 0 0 1px rgba(125,211,252,.18),0 0 32px rgba(56,189,248,.16)}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes raSignal {{0%{{offset-distance:0%;opacity:0}}12%{{opacity:1}}88%{{opacity:1}}100%{{offset-distance:100%;opacity:0}}}}
@keyframes raPulse {{0%,100%{{transform:scale(.7);opacity:.2}}50%{{transform:scale(1.7);opacity:.72}}}}
@keyframes raEvidenceFly {{0%{{opacity:0;transform:translate(-34px,12px) scale(.9)}}55%{{opacity:1;transform:translate(3px,-2px) scale(1.02)}}100%{{opacity:1;transform:none}}}}
@keyframes raVerdictReveal {{0%,72%{{opacity:0;transform:translateY(8px) scale(.98)}}100%{{opacity:1;transform:none}}}}
@keyframes raStateSweep {{0%{{background-position:120% 0}}100%{{background-position:-120% 0}}}}

.ra-agent-stage{{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(270px,.68fr);gap:14px;margin:4px 0 18px;animation:raGraphEnter .45s ease both}}
.ra-agent-graph{{position:relative;overflow:hidden;background:radial-gradient(circle at 18% 18%,rgba(14,165,233,.12),transparent 28%),radial-gradient(circle at 85% 10%,rgba(99,102,241,.12),transparent 27%),linear-gradient(180deg,#091321,#0d1b2c 64%,#0b1726);border:1px solid #253851;border-radius:16px;padding:18px;color:#f8fafc;box-shadow:0 22px 54px rgba(15,23,42,.22)}}
.ra-agent-graph::before{{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(148,163,184,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(148,163,184,.035) 1px,transparent 1px);background-size:28px 28px;pointer-events:none}}
.ra-agent-graph__top{{position:relative;z-index:2;display:flex;justify-content:space-between;align-items:flex-start;gap:18px;margin-bottom:12px}}
.ra-agent-graph__eyebrow{{font-size:.68rem;font-weight:900;letter-spacing:.12em;color:#7dd3fc}}
.ra-agent-graph__title{{font-size:1.08rem;font-weight:850;margin-top:4px}}
.ra-agent-graph__meta{{font-size:.74rem;color:#94a3b8;margin-top:5px;line-height:1.4}}
.ra-agent-graph__verdict{{text-align:right;background:rgba(18,35,58,.88);border:1px solid #31445f;border-radius:11px;padding:9px 11px;min-width:190px;animation:raVerdictReveal 4.1s ease both}}
.ra-agent-graph__verdict span{{display:block;color:#93c5fd;font-size:.65rem;font-weight:900;text-transform:uppercase;letter-spacing:.08em}}
.ra-agent-graph__verdict strong{{display:block;font-size:.96rem;margin-top:2px}}
.ra-agent-graph__verdict small{{color:#94a3b8;font-size:.7rem}}

.ra-agent-canvas{{position:relative;z-index:2;display:grid;grid-template-columns:1fr 62px 1fr 62px 1fr;grid-template-rows:auto 70px auto;align-items:center;gap:10px 6px;min-height:330px}}
.ra-agent-node{{position:relative;background:linear-gradient(180deg,#101f31,#0f1a2a);border:1px solid #2a3e58;border-radius:12px;padding:12px 13px;min-height:88px;opacity:.24;filter:saturate(.45);transition:.2s ease}}
.ra-agent-node.is-active{{filter:none;border-color:#4f83c2}}
.ra-agent-node.is-step-1{{animation:raNodeVisit .65s .15s both}}
.ra-agent-node.is-step-2{{animation:raNodeVisit .65s 1.0s both}}
.ra-agent-node.is-step-3{{animation:raNodeVisit .65s 1.85s both}}
.ra-agent-node.is-step-4{{animation:raNodeVisit .65s 2.7s both}}
.ra-agent-node.is-step-5{{animation:raNodeVisit .65s 3.55s both}}
.ra-agent-node__stage{{color:#60a5fa;font-size:.61rem;font-weight:900;letter-spacing:.1em;text-transform:uppercase}}
.ra-agent-node__title{{font-size:.87rem;font-weight:850;margin-top:3px}}
.ra-agent-node__detail{{color:#94a3b8;font-size:.69rem;line-height:1.35;margin-top:4px}}
.ra-agent-node__pulse{{display:none;position:absolute;width:8px;height:8px;border-radius:999px;background:#38bdf8;right:10px;top:10px}}
.ra-agent-node.is-active .ra-agent-node__pulse{{display:block;animation:raPulse 1.6s ease-in-out infinite}}
.ra-agent-node--danger.is-active{{border-color:#fb7185}} .ra-agent-node--success.is-active{{border-color:#34d399}} .ra-agent-node--warning.is-active{{border-color:#fbbf24}} .ra-agent-node--neutral.is-active{{border-color:#94a3b8}}

.ra-agent-edge{{height:3px;position:relative;background:#21354a;border-radius:999px;overflow:visible;opacity:.28}}
.ra-agent-edge.is-active{{opacity:1;background:#294b68}}
.ra-agent-edge__track{{position:absolute;inset:-3px 0;background:linear-gradient(90deg,transparent,rgba(125,211,252,.16),transparent);background-size:180% 100%;animation:raStateSweep 1.8s linear infinite}}
.ra-agent-edge__signal{{display:none;position:absolute;top:-4px;left:-2px;width:11px;height:11px;border-radius:999px;background:#7dd3fc;box-shadow:0 0 18px rgba(125,211,252,.9)}}
.ra-agent-edge.is-active .ra-agent-edge__signal{{display:block;offset-path:path("M 0 5 L 62 5");animation:raSignal .8s calc(.35s + (var(--edge-delay) * .85s)) linear both}}

.n-signal{{grid-column:1;grid-row:2}} .e-signal-pricing{{grid-column:2;grid-row:2}} .n-pricing{{grid-column:3;grid-row:2}} .e-pricing-exception{{grid-column:4;grid-row:2}} .n-exception{{grid-column:5;grid-row:2}}
.n-usage{{grid-column:3;grid-row:1}} .n-approval{{grid-column:5;grid-row:1}} .n-negative{{grid-column:3;grid-row:3}} .n-leakage{{grid-column:1;grid-row:3}} .n-explained{{grid-column:1;grid-row:1}} .n-conflict{{grid-column:5;grid-row:3}} .n-blocked{{grid-column:3;grid-row:1}}

.ra-evidence-dock{{position:relative;z-index:2;margin-top:10px;border-top:1px solid rgba(148,163,184,.16);padding-top:12px}}
.ra-evidence-dock__label{{font-size:.62rem;font-weight:900;letter-spacing:.1em;color:#7dd3fc;text-transform:uppercase;margin-bottom:8px}}
.ra-evidence-dock__cards{{display:flex;flex-wrap:wrap;gap:8px}}
.ra-evidence-card{{position:relative;overflow:hidden;background:#122239;border:1px solid #2d4561;border-radius:10px;padding:8px 10px;min-width:132px;opacity:0;animation:raEvidenceFly .55s calc(.7s + (var(--evidence-index) * .62s)) ease both}}
.ra-evidence-card__beam{{position:absolute;inset:0;background:linear-gradient(105deg,transparent 30%,rgba(125,211,252,.12),transparent 70%);transform:translateX(-120%);animation:raStateSweep 1.8s calc(1s + (var(--evidence-index) * .55s)) ease both}}
.ra-evidence-card span{{display:block;color:#7dd3fc;font-size:.58rem;font-weight:900;text-transform:uppercase;letter-spacing:.07em}}
.ra-evidence-card strong{{display:block;font-size:.72rem;margin-top:2px;color:#e5eef8}}
.ra-evidence-card small{{display:block;font-size:.61rem;color:#7f93aa;margin-top:2px}}
.ra-evidence-card--empty{{opacity:1;animation:none;color:#94a3b8;font-size:.72rem}}
.ra-agent-legend{{position:relative;z-index:2;display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}} .ra-agent-legend span{{font-size:.64rem;color:#cbd5e1;background:#122037;border:1px solid #293b54;border-radius:999px;padding:5px 8px}} .ra-agent-legend b{{color:#7dd3fc}}

.ra-agent-state{{background:#fff;border:1px solid #d9e2ea;border-radius:14px;overflow:hidden;box-shadow:0 12px 34px rgba(16,24,40,.07)}}
.ra-agent-state__head{{padding:14px 15px;background:linear-gradient(135deg,#f8fafc,#eef4ff);border-bottom:1px solid #e4e7ec}}
.ra-agent-state__eyebrow{{color:#155eef;font-size:.65rem;font-weight:900;letter-spacing:.09em;text-transform:uppercase}}
.ra-agent-state__title{{font-size:.96rem;font-weight:850;color:#111827;margin-top:3px}}
.ra-agent-state__sub{{font-size:.72rem;color:#667085;margin-top:4px;line-height:1.35}}
.ra-agent-state__body{{padding:14px 15px}}
.ra-agent-state__block{{padding:11px 0;border-bottom:1px solid #eef1f4;animation:raEvidenceFly .48s ease both}} .ra-agent-state__block:nth-child(1){{animation-delay:.55s}} .ra-agent-state__block:nth-child(2){{animation-delay:1.9s}} .ra-agent-state__block:nth-child(3){{animation-delay:3.2s}} .ra-agent-state__block:last-child{{border-bottom:0}}
.ra-agent-state__label{{font-size:.62rem;font-weight:900;letter-spacing:.07em;text-transform:uppercase;color:#667085}}
.ra-agent-state__value{{font-size:.82rem;font-weight:800;color:#182230;line-height:1.38;margin-top:4px}}
.ra-agent-state__status{{display:inline-flex;align-items:center;gap:6px;margin-top:6px;background:#eff8ff;color:#175cd3;border-radius:999px;padding:4px 8px;font-size:.66rem;font-weight:800}}
.ra-agent-state__dot{{width:6px;height:6px;border-radius:50%;background:#2e90fa;animation:raPulse 1.5s ease-in-out infinite}}
.ra-agent-state__boundary{{margin-top:10px;background:#f8fafc;border:1px solid #e4e7ec;border-radius:9px;padding:9px 10px;font-size:.69rem;line-height:1.4;color:#475467}}

@media(max-width:900px){{.ra-agent-stage{{grid-template-columns:1fr}}}}
@media(max-width:760px){{.ra-agent-graph__top{{display:block}}.ra-agent-graph__verdict{{text-align:left;margin-top:10px;min-width:0}}.ra-agent-canvas{{display:flex;flex-direction:column;min-height:0}}.ra-agent-edge{{width:3px;height:20px}}.ra-agent-edge__signal{{display:none!important}}.ra-agent-node{{width:100%}}.ra-agent-node.is-dimmed{{display:none}}.ra-evidence-card{{min-width:calc(50% - 4px);flex:1}}}}
@media(prefers-reduced-motion:reduce){{.ra-agent-stage *{{animation:none!important;transition:none!important}}.ra-agent-node.is-active,.ra-evidence-card,.ra-agent-graph__verdict{{opacity:1!important}}}}
</style>

<div class="ra-agent-graph">
  <div class="ra-agent-graph__top">
    <div>
      <div class="ra-agent-graph__eyebrow">LIVE AGENT REPLAY</div>
      <div class="ra-agent-graph__title">{html.escape(case.customer_name)} · {html.escape(case.case_id or case.identity_key())}</div>
      <div class="ra-agent-graph__meta">{trace_count} executed decisions · {len(case.evidence)} evidence items touched · replay is reconstructed from auditable runtime state</div>
    </div>
    <div class="ra-agent-graph__verdict">
      <span>Final verdict</span>
      <strong>{html.escape(verdict)}</strong>
      <small>{html.escape(amount)} gross variance</small>
    </div>
  </div>

  <div class="ra-agent-canvas">
    <div class="n-signal">{_node("signal", "Observe", "Variance signal", "Invoice or source-data anomaly enters investigation.", active_path)}</div>
    <div class="e-signal-pricing">{_edge("signal-pricing", "signal", "pricing", active_path)}</div>
    <div class="n-pricing">{_node("pricing", "Check", "Pricing evidence", "Validate contract term, effective dates and expected billing.", active_path)}</div>
    <div class="e-pricing-exception">{_edge("pricing-exception", "pricing", "exception", active_path)}</div>
    <div class="n-exception">{_node("exception", "Check", "Commercial exception", "Look for an approved concession covering the variance.", active_path)}</div>
    <div class="n-usage">{_node("usage", "Guardrail", "Usage integrity", "Conflicting usage stops financial calculation.", active_path)}</div>
    <div class="n-approval">{_node("approval", "Resolve", "Approval document", "Inspect source approval evidence, not only structured flags.", active_path)}</div>
    <div class="n-negative">{_node("negative", "Resolve", "Negative evidence", "No valid exception or approval supports the variance.", active_path)}</div>
    <div class="n-leakage">{_node("leakage", "Decide", "Suspected leakage", "Escalate for finance confirmation; no automatic correction.", active_path, "danger")}</div>
    <div class="n-explained">{_node("explained", "Decide", "Explained variance", "Approved commercial evidence explains the variance.", active_path, "success")}</div>
    <div class="n-conflict">{_node("conflict", "Decide", "Evidence conflict", "Structured status and source document disagree.", active_path, "warning")}</div>
    <div class="n-blocked">{_node("blocked", "Decide", "Insufficient data", "Human reconciliation required before any financial amount.", active_path, "neutral")}</div>
  </div>

  <div class="ra-evidence-dock">
    <div class="ra-evidence-dock__label">Evidence entering decision context</div>
    <div class="ra-evidence-dock__cards">{evidence_cards}</div>
  </div>
  <div class="ra-agent-legend"><span><b>Pulse</b> visited node</span><span><b>Signal</b> executed transition</span><span>Dimmed branch not taken</span><span>Human review remains final authority</span></div>
</div>

<div class="ra-agent-state">
  <div class="ra-agent-state__head">
    <div class="ra-agent-state__eyebrow">Agent state</div>
    <div class="ra-agent-state__title">Auditable decision context</div>
    <div class="ra-agent-state__sub">This panel exposes reconstructable investigation state, not hidden chain-of-thought.</div>
  </div>
  <div class="ra-agent-state__body">
    <div class="ra-agent-state__block">
      <div class="ra-agent-state__label">Current hypothesis</div>
      <div class="ra-agent-state__value">{html.escape(hypothesis)}</div>
      <div class="ra-agent-state__status"><span class="ra-agent-state__dot"></span>investigating evidence</div>
    </div>
    <div class="ra-agent-state__block">
      <div class="ra-agent-state__label">Evidence state</div>
      <div class="ra-agent-state__value">{html.escape(evidence_state)}</div>
    </div>
    <div class="ra-agent-state__block">
      <div class="ra-agent-state__label">Selected next action</div>
      <div class="ra-agent-state__value">{html.escape(next_action)}</div>
    </div>
    <div class="ra-agent-state__boundary"><strong>Decision boundary:</strong> deterministic monetary logic and human finance approval remain outside autonomous agent action.</div>
  </div>
</div>
</div>
'''


def build_flow_map_html(cases: tuple[InvestigationCase, ...] | list[InvestigationCase]) -> str:
    nodes = []
    for node in flow_map_nodes(cases):
        nodes.append(
            f'<div class="ra-flow-node ra-flow-node--{html.escape(node.status)}">'
            f'<div class="ra-flow-node__customer">{html.escape(node.customer_name)}</div>'
            f'<div class="ra-flow-node__case">{html.escape(node.case_id)}</div>'
            f'<div class="ra-flow-node__outcome">{html.escape(format_status(node.status))}</div>'
            f'<div class="ra-flow-node__meta">{html.escape(format_money(node.amount))} | {node.evidence_count} evidence items</div>'
            '</div>'
        )
    return '<div class="ra-flow-map"><div class="ra-flow-map__nodes">' + ''.join(nodes) + '</div></div>'


def render_agent_graph(case: InvestigationCase, replay_token: int = 0) -> None:
    st.markdown(build_agent_graph_html(case, replay_token=replay_token), unsafe_allow_html=True)


def render_flow_map(cases: tuple[InvestigationCase, ...] | list[InvestigationCase]) -> None:
    st.markdown(build_flow_map_html(cases), unsafe_allow_html=True)
