from __future__ import annotations

from app.services.local_engine import run_q3_golden_investigation


def run_offline_demo_summary() -> str:
    result = run_q3_golden_investigation()
    lines = ["Revenue Assurance Investigation", "Review period: 2026-07-01 to 2026-09-30", "", "Executed investigation paths:"]
    for case in result.cases:
        lines.append(f"\n{case.customer_name} -> {case.status}")
        lines.extend(f"  {index}. {step}" for index, step in enumerate(case.investigation_trace, start=1))
    summary = result.summary
    lines += ["", "Final summary:", f"Gross variance detected: ${summary.gross_variance_detected:,.0f}", f"Explained variance: ${summary.explained_variance:,.0f}", f"Suspected leakage: ${summary.suspected_leakage:,.0f}", f"Evidence conflict: ${summary.evidence_conflict:,.0f}", f"Data-quality cases: {summary.insufficient_data_cases}"]
    return "\n".join(lines)
