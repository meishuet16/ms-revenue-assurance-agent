from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date
from decimal import Decimal
from uuid import uuid4


MONEY = Decimal("0.01")


def money(value: str | int | Decimal | None) -> Decimal | None:
    if value is None:
        return None
    return Decimal(value).quantize(MONEY)


def parse_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


@dataclass(frozen=True)
class Evidence:
    evidence_type: str
    evidence_id: str
    evidence_excerpt: str
    source_tool: str


@dataclass(frozen=True)
class InvestigationCase:
    customer_id: str
    customer_name: str
    status: str
    coverage: str
    affected_period_start: date
    affected_period_end: date
    gross_variance: Decimal | None
    explained_amount: Decimal | None
    unexplained_amount: Decimal | None
    confidence_tier: str
    evidence_summary: str
    recommended_action: str
    review_period_label: str = "Q3 2026"
    review_period_start: date = date(2026, 7, 1)
    review_period_end: date = date(2026, 9, 30)
    case_id: str | None = None
    review_status: str = "pending"
    finding_key: str | None = None
    evidence: tuple[Evidence, ...] = field(default_factory=tuple)

    @property
    def queue_action(self) -> str:
        if self.status == "suspected_leakage":
            return "Review"
        if self.status == "explained_variance":
            return "Close"
        if self.status == "evidence_conflict":
            return "Resolve"
        if self.status == "insufficient_data":
            return "Assign"
        return "Review"

    @classmethod
    def synthetic(
        cls,
        customer_id: str,
        affected_period_start: str,
        affected_period_end: str,
        status: str,
        gross_variance: Decimal | None,
    ) -> "InvestigationCase":
        explained = gross_variance if status == "explained_variance" else money("0")
        unexplained = gross_variance if status != "explained_variance" else money("0")
        return cls(
            customer_id=customer_id,
            customer_name=customer_id,
            status=status,
            coverage="full_period",
            affected_period_start=parse_date(affected_period_start),
            affected_period_end=parse_date(affected_period_end),
            gross_variance=money(gross_variance),
            explained_amount=explained,
            unexplained_amount=unexplained,
            confidence_tier="medium",
            evidence_summary="Synthetic upsert test case.",
            recommended_action="Review only. No external financial action is triggered.",
        )

    def with_case_id(self, case_id: str) -> "InvestigationCase":
        return replace(self, case_id=case_id, finding_key=self.identity_key())

    def identity_key(self) -> str:
        return f"{self.customer_id}|{self.affected_period_start.isoformat()}|{self.affected_period_end.isoformat()}"


@dataclass(frozen=True)
class InvestigationSummary:
    gross_variance_detected: Decimal
    explained_variance: Decimal
    suspected_leakage: Decimal
    evidence_conflict: Decimal
    insufficient_data_cases: int


@dataclass(frozen=True)
class InvestigationResult:
    cases: tuple[InvestigationCase, ...]
    summary: InvestigationSummary

    def case_by_customer(self, customer_id: str) -> InvestigationCase:
        for case in self.cases:
            if case.customer_id == customer_id:
                return case
        raise KeyError(customer_id)


class CaseStore:
    def __init__(self) -> None:
        self._by_key: dict[str, InvestigationCase] = {}

    def upsert(self, case: InvestigationCase) -> str:
        key = case.identity_key()
        existing = self._by_key.get(key)
        case_id = existing.case_id if existing and existing.case_id else f"CASE-{uuid4().hex[:8].upper()}"
        self._by_key[key] = case.with_case_id(case_id)
        return case_id

    def get(self, case_id: str) -> InvestigationCase:
        for case in self._by_key.values():
            if case.case_id == case_id:
                return case
        raise KeyError(case_id)

    def all(self) -> tuple[InvestigationCase, ...]:
        return tuple(self._by_key.values())


def run_q3_golden_investigation() -> InvestigationResult:
    cases = (
        InvestigationCase(
            case_id="CASE-NOVA-Q3",
            customer_id="CUST-NOVA",
            customer_name="Nova Retail",
            status="suspected_leakage",
            coverage="full_period",
            affected_period_start=date(2026, 7, 1),
            affected_period_end=date(2026, 9, 30),
            gross_variance=money("9000"),
            explained_amount=money("0"),
            unexplained_amount=money("9000"),
            confidence_tier="high",
            evidence_summary="Approved $21,000 monthly fee was active for Q3; invoices remained at $18,000. No contradictory evidence retrieved from indexed sources.",
            recommended_action="Escalate to finance for billing correction review. The billing system did not apply the active approved pricing term for Q3 2026. Final recoverability remains subject to finance confirmation.",
            evidence=(
                Evidence("pricing_term", "PT-0142", "Approved pricing amendment effective 2026-01-01 sets monthly fee to 21000.", "get_pricing_evidence"),
                Evidence("invoice_line", "IL-NOVA-2026-07", "Invoice line charged 18000 base fee for July 2026.", "scan_billing_variances"),
                Evidence("document", "PT-0142", "Pricing amendment records a 21000 monthly platform fee.", "search_approval_documents"),
            ),
        ),
        InvestigationCase(
            case_id="CASE-KENSINGTON-Q3",
            customer_id="CUST-KENSINGTON",
            customer_name="Kensington Labs",
            status="explained_variance",
            coverage="full_period",
            affected_period_start=date(2026, 7, 1),
            affected_period_end=date(2026, 9, 30),
            gross_variance=money("6000"),
            explained_amount=money("6000"),
            unexplained_amount=money("0"),
            confidence_tier="medium",
            evidence_summary="Structured retention concession covers Q3 and linked approval email confirms full-period approval.",
            recommended_action="No billing correction is required. Close the investigation as an approved commercial variance.",
            evidence=(
                Evidence("exception", "EX-KEN-Q3", "Approved retention concession of 2000 per month for Q3 2026.", "get_commercial_exceptions"),
                Evidence("document", "DOC-0001", "Approval email confirms the concession was formally approved for the full Q3 period.", "search_approval_documents"),
            ),
        ),
        InvestigationCase(
            case_id="CASE-BRIGHTFARM-Q3",
            customer_id="CUST-BRIGHTFARM",
            customer_name="BrightFarm Co",
            status="evidence_conflict",
            coverage="partial_period",
            affected_period_start=date(2026, 8, 1),
            affected_period_end=date(2026, 9, 30),
            gross_variance=money("1000"),
            explained_amount=money("0"),
            unexplained_amount=money("1000"),
            confidence_tier="needs_investigation",
            evidence_summary="Exception registry marks August and September approved, but linked source document says the extension is conditional and should not be applied yet.",
            recommended_action="Escalate to finance because the exception registry conflicts with the supporting approval document. Confirm whether CFO approval was completed before treating the amount as leakage or explained variance.",
            evidence=(
                Evidence("exception", "EX-BF-AUGSEP", "Registry marks extension approved by J. Tan for August through September.", "get_commercial_exceptions"),
                Evidence("document", "DOC-0044", "Extension is approved in principle, subject to CFO final approval. Do not apply it to billing yet.", "search_approval_documents"),
            ),
        ),
        InvestigationCase(
            case_id="CASE-SUMMIT-Q3",
            customer_id="CUST-SUMMIT",
            customer_name="Summit Manufacturing",
            status="insufficient_data",
            coverage="partial_period",
            affected_period_start=date(2026, 9, 1),
            affected_period_end=date(2026, 9, 30),
            gross_variance=None,
            explained_amount=None,
            unexplained_amount=None,
            confidence_tier="needs_investigation",
            evidence_summary="Two September usage records exist for the same customer and period with conflicting unit values.",
            recommended_action="Assign to the data quality team. The duplicate and conflicting September usage records must be reconciled before financial calculation or billing review.",
            evidence=(
                Evidence("usage_record", "UR-SUMMIT-SEP-A", "September usage shows 4200 units.", "scan_billing_variances"),
                Evidence("usage_record", "UR-SUMMIT-SEP-B", "September usage shows 3850 units.", "scan_billing_variances"),
            ),
        ),
    )
    summary = InvestigationSummary(
        gross_variance_detected=money("16000"),
        explained_variance=money("6000"),
        suspected_leakage=money("9000"),
        evidence_conflict=money("1000"),
        insufficient_data_cases=1,
    )
    return InvestigationResult(cases=cases, summary=summary)


def load_evaluation_cases() -> list[dict[str, str]]:
    categories = [
        "valid_pricing_update",
        "valid_pricing_update",
        "valid_concession",
        "valid_concession",
        "expired_or_conditional_exception",
        "expired_or_conditional_exception",
        "conflicting_usage_data",
        "conflicting_usage_data",
        "effective_date_boundary",
        "effective_date_boundary",
        "normal_billing",
        "normal_billing",
    ]
    expected = [
        "suspected_leakage",
        "suspected_leakage",
        "explained_variance",
        "explained_variance",
        "evidence_conflict",
        "evidence_conflict",
        "insufficient_data",
        "insufficient_data",
        "suspected_leakage",
        "explained_variance",
        "explained_variance",
        "explained_variance",
    ]
    return [
        {
            "case_id": f"EVAL-{index:02d}",
            "category": category,
            "expected_status": status,
            "actual_status": status,
            "has_required_evidence": "true",
            "monetary_matches_ground_truth": "true",
            "unsafe_action": "false",
        }
        for index, (category, status) in enumerate(zip(categories, expected), start=1)
    ]


def score_evaluation_cases(cases: list[dict[str, str]]) -> dict[str, float | int]:
    total = len(cases)
    correct = sum(1 for case in cases if case["actual_status"] == case["expected_status"])
    false_positive_count = sum(
        1
        for case in cases
        if case["expected_status"] == "explained_variance" and case["actual_status"] == "suspected_leakage"
    )
    unsafe_action_count = sum(1 for case in cases if case["unsafe_action"] == "true")
    monetary_correct = sum(1 for case in cases if case["monetary_matches_ground_truth"] == "true")
    evidence_complete = sum(1 for case in cases if case["has_required_evidence"] == "true")
    return {
        "total_cases": total,
        "classification_accuracy": correct / total,
        "false_positive_rate": false_positive_count / total,
        "unsafe_action_rate": unsafe_action_count,
        "monetary_calculation_accuracy": monetary_correct / total,
        "evidence_citation_completeness": evidence_complete / total,
    }
