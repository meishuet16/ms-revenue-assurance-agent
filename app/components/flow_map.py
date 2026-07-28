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


def build_flow_map_html(cases: tuple[InvestigationCase, ...] | list[InvestigationCase]) -> str:
    lanes = "".join(
        f'<div class="ra-flow-lane"><span>{label}</span><strong>{detail}</strong></div>'
        for label, detail in [
            ("Detect", "variance and data quality"),
            ("Validate", "pricing, exceptions, documents"),
            ("Prepare", "finance review case"),
        ]
    )
    nodes = []
    for node in flow_map_nodes(cases):
        nodes.append(
            f'<div class="ra-flow-node ra-flow-node--{html.escape(node.status)}">'
            f'<div class="ra-flow-node__customer">{html.escape(node.customer_name)}</div>'
            f'<div class="ra-flow-node__case">{html.escape(node.case_id)}</div>'
            f'<div class="ra-flow-node__outcome">{html.escape(format_status(node.status))}</div>'
            f'<div class="ra-flow-node__meta">{html.escape(format_money(node.amount))} | '
            f'{node.evidence_count} evidence items</div>'
            "</div>"
        )
    return (
        '<div class="ra-flow-map">'
        '<div class="ra-flow-map__lanes">'
        f"{lanes}"
        "</div>"
        '<div class="ra-flow-map__connector"></div>'
        '<div class="ra-flow-map__nodes">'
        f'{"".join(nodes)}'
        "</div>"
        "</div>"
    )


def render_flow_map(cases: tuple[InvestigationCase, ...] | list[InvestigationCase]) -> None:
    st.markdown(build_flow_map_html(cases), unsafe_allow_html=True)
