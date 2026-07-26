from __future__ import annotations

from app.services.local_engine import run_q3_golden_investigation


def run_offline_demo_summary() -> str:
    result = run_q3_golden_investigation()
    summary = result.summary
    return "\n".join(
        [
            "Revenue Assurance Investigation",
            "Review period: 2026-07-01 to 2026-09-30",
            "",
            "Skill: detect-billing-variances",
            "- 4 findings identified",
            "- 1 source-data conflict detected",
            "",
            "Skill: validate-commercial-evidence",
            "- Nova Retail: no valid exception found",
            "- Kensington Labs: structured exception matches approval document",
            "- BrightFarm Co: structured exception conflicts with approval document",
            "- Summit Manufacturing: conflicting usage records",
            "",
            "Skill: prepare-finance-review-case",
            "- 4 cases created or updated",
            "",
            "Final summary:",
            f"Gross variance detected: ${summary.gross_variance_detected:,.0f}",
            f"Explained variance: ${summary.explained_variance:,.0f}",
            f"Suspected leakage: ${summary.suspected_leakage:,.0f}",
            f"Evidence conflict: ${summary.evidence_conflict:,.0f}",
            f"Data-quality cases: {summary.insufficient_data_cases}",
        ]
    )

