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


def _active_path(status: str) -> set[str]:
    common = {"signal", "pricing", "exception"}
    if status == "suspected_leakage":
        return common | {"negative", "leakage"}
    if status == "explained_variance":
        return common | {"approval", "explained"}
    if status == "evidence_conflict":
        return common | {"approval", "conflict", "conflict_outcome"}
    if status == "insufficient_data":
        return {"signal", "usage", "blocked"}
    return {"signal"}


def _node(node_id: str, stage: str, title: str, detail: str, active: set[str], tone: str = "neutral") -> str:
    classes = ["ra-agent-node", f"ra-agent-node--{tone}"]
    if node_id in active:
        classes.append("is-active")
    return (
        f'<div class="{" ".join(classes)}" data-node="{html.escape(node_id)}">'
        f'<div class="ra-agent-node__stage">{html.escape(stage)}</div>'
        f'<div class="ra-agent-node__title">{html.escape(title)}</div>'
        f'<div class="ra-agent-node__detail">{html.escape(detail)}</div>'
        '<div class="ra-agent-node__pulse"></div>'
        '</div>'
    )


def _edge(name: str, active: bool) -> str:
    return f'<div class="ra-agent-edge ra-agent-edge--{name}{" is-active" if active else ""}"><span></span></div>'


def build_agent_graph_html(case: InvestigationCase) -> str:
    active = _active_path(case.status)
    verdict = format_status(case.status)
    amount = format_money(case.gross_variance)
    trace_count = len(getattr(case, "investigation_trace", ()) or ())

    graph = (
        '<div class="ra-agent-graph">'
        '<style>'
        '@keyframes raSignal{0%{transform:translateX(-12px);opacity:0}35%{opacity:1}100%{transform:translateX(112px);opacity:0}}'
        '@keyframes raPulse{0%,100%{transform:scale(.65);opacity:.18}50%{transform:scale(1.35);opacity:.58}}'
        '@keyframes raReveal{from{opacity:.35;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}'
        '.ra-agent-graph{position:relative;overflow:hidden;background:linear-gradient(180deg,#0d1726,#111f33);border:1px solid #26364c;border-radius:14px;padding:18px;color:#f8fafc;box-shadow:0 18px 48px rgba(15,23,42,.16)}'
        '.ra-agent-graph__top{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;margin-bottom:16px}.ra-agent-graph__eyebrow{font-size:.7rem;font-weight:900;letter-spacing:.11em;color:#7dd3fc}.ra-agent-graph__title{font-size:1.08rem;font-weight:850;margin-top:3px}.ra-agent-graph__meta{font-size:.77rem;color:#94a3b8;margin-top:4px}.ra-agent-graph__verdict{text-align:right;background:#14233a;border:1px solid #31445f;border-radius:10px;padding:9px 11px;min-width:185px}.ra-agent-graph__verdict span{display:block;color:#93c5fd;font-size:.67rem;font-weight:900;text-transform:uppercase;letter-spacing:.08em}.ra-agent-graph__verdict strong{display:block;font-size:.95rem;margin-top:2px}.ra-agent-graph__verdict small{color:#94a3b8;font-size:.72rem}'
        '.ra-agent-canvas{display:grid;grid-template-columns:1.05fr .2fr 1.05fr .2fr 1.05fr;grid-template-rows:auto 22px auto 22px auto;align-items:center;gap:7px 8px;min-height:440px}.ra-agent-node{position:relative;background:#111c2e;border:1px solid #2b3b53;border-radius:11px;padding:12px 13px;min-height:82px;opacity:.38;filter:saturate(.55);transition:.2s ease}.ra-agent-node.is-active{opacity:1;filter:none;border-color:#4f83c2;box-shadow:0 0 0 1px rgba(96,165,250,.12),0 10px 28px rgba(2,8,23,.18);animation:raReveal .55s ease both}.ra-agent-node__stage{color:#60a5fa;font-size:.62rem;font-weight:900;letter-spacing:.09em;text-transform:uppercase}.ra-agent-node__title{font-size:.86rem;font-weight:850;margin-top:3px}.ra-agent-node__detail{color:#94a3b8;font-size:.7rem;line-height:1.3;margin-top:4px}.ra-agent-node__pulse{display:none;position:absolute;width:8px;height:8px;border-radius:999px;background:#38bdf8;right:10px;top:10px}.ra-agent-node.is-active .ra-agent-node__pulse{display:block;animation:raPulse 1.8s ease-in-out infinite}.ra-agent-node--danger.is-active{border-color:#fb7185}.ra-agent-node--success.is-active{border-color:#34d399}.ra-agent-node--warning.is-active{border-color:#fbbf24}.ra-agent-node--neutral.is-active{border-color:#94a3b8}'
        '.ra-agent-edge{position:relative;height:3px;background:#24364c;border-radius:999px;overflow:hidden}.ra-agent-edge span{position:absolute;inset:0 auto 0 -24px;width:26px;background:linear-gradient(90deg,transparent,#7dd3fc,transparent);opacity:0}.ra-agent-edge.is-active{background:#315071}.ra-agent-edge.is-active span{opacity:1;animation:raSignal 1.65s linear infinite}'
        '.ra-agent-legend{display:flex;flex-wrap:wrap;gap:7px;margin-top:14px}.ra-agent-legend span{font-size:.67rem;color:#cbd5e1;background:#132036;border:1px solid #293b54;border-radius:999px;padding:5px 8px}.ra-agent-legend b{color:#7dd3fc}'
        '.n-signal{grid-column:1;grid-row:3}.e-signal-pricing{grid-column:2;grid-row:3}.n-pricing{grid-column:3;grid-row:3}.e-pricing-exception{grid-column:4;grid-row:3}.n-exception{grid-column:5;grid-row:3}.n-usage{grid-column:3;grid-row:1}.e-signal-usage{grid-column:1/3;grid-row:2}.n-negative{grid-column:3;grid-row:5}.n-approval{grid-column:5;grid-row:1}.n-conflict{grid-column:5;grid-row:5}.n-leakage{grid-column:1;grid-row:5}.n-explained{grid-column:1;grid-row:1}.n-conflict-outcome{grid-column:5;grid-row:5}.n-blocked{grid-column:3;grid-row:1}'
        '@media(max-width:760px){.ra-agent-graph__top{display:block}.ra-agent-graph__verdict{text-align:left;margin-top:10px}.ra-agent-canvas{display:flex;flex-direction:column;min-height:0}.ra-agent-edge{width:3px;height:24px}.ra-agent-edge span{display:none}.ra-agent-node{width:100%}.ra-agent-canvas .is-inactive-mobile{display:none}}'
        '</style>'
        '<div class="ra-agent-graph__top">'
        '<div><div class="ra-agent-graph__eyebrow">LIVE INVESTIGATION GRAPH</div>'
        f'<div class="ra-agent-graph__title">{html.escape(case.customer_name)} · {html.escape(case.case_id or case.identity_key())}</div>'
        f'<div class="ra-agent-graph__meta">{trace_count} executed decisions · {len(case.evidence)} evidence items touched · deterministic finance boundary preserved</div></div>'
        '<div class="ra-agent-graph__verdict"><span>Current verdict</span>'
        f'<strong>{html.escape(verdict)}</strong><small>{html.escape(amount)} gross variance</small></div></div>'
        '<div class="ra-agent-canvas">'
        f'<div class="n-signal">{_node("signal", "Observe", "Variance signal", "Invoice or source-data anomaly enters investigation.", active)}</div>'
        f'<div class="e-signal-pricing">{_edge("signal-pricing", "pricing" in active)}</div>'
        f'<div class="n-pricing">{_node("pricing", "Check", "Pricing evidence", "Validate contract term, effective dates and expected billing.", active)}</div>'
        f'<div class="e-pricing-exception">{_edge("pricing-exception", "exception" in active)}</div>'
        f'<div class="n-exception">{_node("exception", "Check", "Commercial exception", "Look for an approved concession covering the variance.", active)}</div>'
        f'<div class="n-usage">{_node("usage", "Guardrail", "Usage integrity", "Conflicting usage stops financial calculation.", active)}</div>'
        f'<div class="n-approval">{_node("approval", "Resolve", "Approval document", "Inspect source approval evidence, not only structured flags.", active)}</div>'
        f'<div class="n-negative">{_node("negative", "Resolve", "Negative evidence", "No valid exception or approval supports the variance.", active)}</div>'
        f'<div class="n-leakage">{_node("leakage", "Decide", "Suspected leakage", "Escalate for finance confirmation; no automatic correction.", active, "danger")}</div>'
        f'<div class="n-explained">{_node("explained", "Decide", "Explained variance", "Approved commercial evidence explains the variance.", active, "success")}</div>'
        f'<div class="n-conflict">{_node("conflict", "Resolve", "Evidence conflict", "Structured status and source document disagree.", active, "warning")}</div>'
        f'<div class="n-blocked">{_node("blocked", "Decide", "Insufficient data", "Human reconciliation required before any financial amount.", active, "neutral")}</div>'
        '</div>'
        '<div class="ra-agent-legend"><span><b>Pulse</b> = visited node</span><span><b>Moving signal</b> = executed path</span><span>Dimmed = branch not taken</span><span>Human review remains final authority</span></div>'
        '</div>'
    )
    return graph


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


def render_agent_graph(case: InvestigationCase) -> None:
    st.markdown(build_agent_graph_html(case), unsafe_allow_html=True)


def render_flow_map(cases: tuple[InvestigationCase, ...] | list[InvestigationCase]) -> None:
    st.markdown(build_flow_map_html(cases), unsafe_allow_html=True)
