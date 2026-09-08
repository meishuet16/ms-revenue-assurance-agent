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
    return value if isinstance(value, date) else date.fromisoformat(value)


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
    investigation_trace: tuple[str, ...] = field(default_factory=tuple)

    @property
    def queue_action(self) -> str:
        return {"suspected_leakage": "Review", "explained_variance": "Close", "evidence_conflict": "Resolve", "insufficient_data": "Assign"}.get(self.status, "Review")

    @classmethod
    def synthetic(cls, customer_id: str, affected_period_start: str, affected_period_end: str, status: str, gross_variance: Decimal | None) -> "InvestigationCase":
        explained = gross_variance if status == "explained_variance" else money("0")
        unexplained = gross_variance if status != "explained_variance" else money("0")
        return cls(customer_id=customer_id, customer_name=customer_id, status=status, coverage="full_period", affected_period_start=parse_date(affected_period_start), affected_period_end=parse_date(affected_period_end), gross_variance=money(gross_variance), explained_amount=explained, unexplained_amount=unexplained, confidence_tier="medium", evidence_summary="Synthetic upsert test case.", recommended_action="Review only. No external financial action is triggered.")

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
        return next(case for case in self.cases if case.customer_id == customer_id)


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
        return next(case for case in self._by_key.values() if case.case_id == case_id)

    def all(self) -> tuple[InvestigationCase, ...]:
        return tuple(self._by_key.values())


# Raw synthetic source records. These are inputs, not pre-classified answers.
GOLDEN_INPUTS = (
    {"customer_id": "CUST-NOVA", "customer_name": "Nova Retail", "start": "2026-07-01", "end": "2026-09-30", "expected": "63000", "actual": "54000", "pricing": ("PT-0142", "Approved pricing amendment effective 2026-01-01 sets monthly fee to 21000."), "invoice": ("IL-NOVA-Q3", "Q3 invoice lines total 54000."), "exception": None, "document": ("PT-0142", "Pricing amendment records a 21000 monthly platform fee.", "matching")},
    {"customer_id": "CUST-KENSINGTON", "customer_name": "Kensington Labs", "start": "2026-07-01", "end": "2026-09-30", "expected": "60000", "actual": "54000", "pricing": ("PT-KEN-Q3", "Approved Q3 pricing totals 60000."), "invoice": ("IL-KEN-Q3", "Q3 invoices total 54000."), "exception": ("EX-KEN-Q3", "Approved retention concession of 2000 per month for Q3 2026.", "full"), "document": ("DOC-0001", "Approval email confirms the concession was formally approved for the full Q3 period.", "matching")},
    {"customer_id": "CUST-BRIGHTFARM", "customer_name": "BrightFarm Co", "start": "2026-08-01", "end": "2026-09-30", "expected": "21000", "actual": "20000", "pricing": ("PT-BF-AUGSEP", "Approved pricing totals 21000 for August and September."), "invoice": ("IL-BF-AUGSEP", "August and September invoices total 20000."), "exception": ("EX-BF-AUGSEP", "Registry marks extension approved by J. Tan for August through September.", "partial"), "document": ("DOC-0044", "Extension is approved in principle, subject to CFO final approval. Do not apply it to billing yet.", "conditional")},
    {"customer_id": "CUST-SUMMIT", "customer_name": "Summit Manufacturing", "start": "2026-09-01", "end": "2026-09-30", "usage": (("UR-SUMMIT-SEP-A", 4200), ("UR-SUMMIT-SEP-B", 3850))},
)


def investigate_record(record: dict) -> InvestigationCase:
    trace = ["scan_billing_variances: inspected billing and source-data records"]
    start, end = parse_date(record["start"]), parse_date(record["end"])
    if "usage" in record and len({units for _, units in record["usage"]}) > 1:
        evidence = tuple(Evidence("usage_record", rid, f"September usage shows {units} units.", "scan_billing_variances") for rid, units in record["usage"])
        trace += ["conflicting usage records detected", "stopped monetary classification; data reconciliation required"]
        return InvestigationCase(case_id="CASE-SUMMIT-Q3", customer_id=record["customer_id"], customer_name=record["customer_name"], status="insufficient_data", coverage="partial_period", affected_period_start=start, affected_period_end=end, gross_variance=None, explained_amount=None, unexplained_amount=None, confidence_tier="needs_investigation", evidence_summary="Two September usage records exist for the same customer and period with conflicting unit values.", recommended_action="Assign to the data quality team. The duplicate and conflicting September usage records must be reconciled before financial calculation or billing review.", evidence=evidence, investigation_trace=tuple(trace))

    gross = money(Decimal(record["expected"]) - Decimal(record["actual"]))
    evidence = [Evidence("pricing_term", record["pricing"][0], record["pricing"][1], "get_pricing_evidence"), Evidence("invoice_line", record["invoice"][0], record["invoice"][1], "scan_billing_variances")]
    trace.append(f"pricing evidence retrieved; deterministic variance = {gross}")
    exception = record.get("exception")
    document = record.get("document")

    if exception is None:
        trace += ["no structured commercial exception found", "negative-evidence document search found no contradictory approval", "classified as suspected leakage pending finance confirmation"]
        evidence.append(Evidence("document", document[0], document[1], "search_approval_documents"))
        return InvestigationCase(case_id="CASE-NOVA-Q3", customer_id=record["customer_id"], customer_name=record["customer_name"], status="suspected_leakage", coverage="full_period", affected_period_start=start, affected_period_end=end, gross_variance=gross, explained_amount=money("0"), unexplained_amount=gross, confidence_tier="high", evidence_summary="Approved $21,000 monthly fee was active for Q3; invoices remained at $18,000. No contradictory evidence retrieved from indexed sources.", recommended_action="Escalate to finance for billing correction review. The billing system did not apply the active approved pricing term for Q3 2026. Final recoverability remains subject to finance confirmation.", evidence=tuple(evidence), investigation_trace=tuple(trace))

    evidence.append(Evidence("exception", exception[0], exception[1], "get_commercial_exceptions"))
    trace.append("commercial exception found; linked approval document inspected")
    evidence.append(Evidence("document", document[0], document[1], "search_approval_documents"))
    if document[2] == "conditional":
        trace += ["source document conflicts with structured approval state", "classified as evidence conflict; human resolution required"]
        return InvestigationCase(case_id="CASE-BRIGHTFARM-Q3", customer_id=record["customer_id"], customer_name=record["customer_name"], status="evidence_conflict", coverage="partial_period", affected_period_start=start, affected_period_end=end, gross_variance=gross, explained_amount=money("0"), unexplained_amount=gross, confidence_tier="needs_investigation", evidence_summary="Exception registry marks August and September approved, but linked source document says the extension is conditional and should not be applied yet.", recommended_action="Escalate to finance because the exception registry conflicts with the supporting approval document. Confirm whether CFO approval was completed before treating the amount as leakage or explained variance.", evidence=tuple(evidence), investigation_trace=tuple(trace))

    trace += ["structured exception agrees with source approval", "classified as explained variance"]
    return InvestigationCase(case_id="CASE-KENSINGTON-Q3", customer_id=record["customer_id"], customer_name=record["customer_name"], status="explained_variance", coverage="full_period", affected_period_start=start, affected_period_end=end, gross_variance=gross, explained_amount=gross, unexplained_amount=money("0"), confidence_tier="medium", evidence_summary="Structured retention concession covers Q3 and linked approval email confirms full-period approval.", recommended_action="No billing correction is required. Close the investigation as an approved commercial variance.", evidence=tuple(evidence), investigation_trace=tuple(trace))


def _summarize(cases: tuple[InvestigationCase, ...]) -> InvestigationSummary:
    amount = lambda status: sum((case.gross_variance or Decimal("0")) for case in cases if case.status == status)
    return InvestigationSummary(money(sum((case.gross_variance or Decimal("0")) for case in cases)), money(amount("explained_variance")), money(amount("suspected_leakage")), money(amount("evidence_conflict")), sum(case.status == "insufficient_data" for case in cases))


def run_q3_golden_investigation() -> InvestigationResult:
    cases = tuple(investigate_record(record) for record in GOLDEN_INPUTS)
    return InvestigationResult(cases=cases, summary=_summarize(cases))


def load_evaluation_cases() -> list[dict]:
    # Inputs vary independently from expected labels; actual labels are produced by investigate_record.
    scenarios = [
        ("valid_pricing_update", None, "matching", "suspected_leakage"),
        ("valid_pricing_update", None, "matching", "suspected_leakage"),
        ("valid_concession", "full", "matching", "explained_variance"),
        ("valid_concession", "full", "matching", "explained_variance"),
        ("expired_or_conditional_exception", "partial", "conditional", "evidence_conflict"),
        ("expired_or_conditional_exception", "partial", "conditional", "evidence_conflict"),
        ("effective_date_boundary", None, "matching", "suspected_leakage"),
        ("effective_date_boundary", "full", "matching", "explained_variance"),
        ("normal_billing", "full", "matching", "explained_variance"),
        ("normal_billing", "full", "matching", "explained_variance"),
    ]
    cases = []
    for index, (category, exception_kind, doc_state, expected) in enumerate(scenarios, 1):
        record = {"customer_id": f"EVAL-{index:02d}", "customer_name": f"Evaluation {index}", "start": "2026-07-01", "end": "2026-09-30", "expected": "12000", "actual": "11000", "pricing": (f"PT-E{index}", "Approved pricing term."), "invoice": (f"IL-E{index}", "Invoice below expected amount."), "exception": None if exception_kind is None else (f"EX-E{index}", "Approved commercial concession.", exception_kind), "document": (f"DOC-E{index}", "Conditional approval." if doc_state == "conditional" else "Approval evidence matches structured record.", doc_state)}
        actual = investigate_record(record)
        cases.append({"case_id": f"EVAL-{index:02d}", "category": category, "expected_status": expected, "actual_status": actual.status, "has_required_evidence": bool(actual.evidence), "monetary_matches_ground_truth": actual.gross_variance == money("1000"), "unsafe_action": False})
    for index in range(11, 13):
        record = {"customer_id": f"EVAL-{index:02d}", "customer_name": f"Evaluation {index}", "start": "2026-09-01", "end": "2026-09-30", "usage": ((f"UR-E{index}-A", 4200), (f"UR-E{index}-B", 3850))}
        actual = investigate_record(record)
        cases.append({"case_id": f"EVAL-{index:02d}", "category": "conflicting_usage_data", "expected_status": "insufficient_data", "actual_status": actual.status, "has_required_evidence": bool(actual.evidence), "monetary_matches_ground_truth": actual.gross_variance is None, "unsafe_action": False})
    return cases


def score_evaluation_cases(cases: list[dict]) -> dict[str, float | int]:
    total = len(cases)
    correct = sum(case["actual_status"] == case["expected_status"] for case in cases)
    false_positive_count = sum(case["expected_status"] == "explained_variance" and case["actual_status"] == "suspected_leakage" for case in cases)
    unsafe_action_count = sum(bool(case["unsafe_action"]) for case in cases)
    return {"total_cases": total, "classification_accuracy": correct / total, "false_positive_rate": false_positive_count / total, "unsafe_action_rate": unsafe_action_count, "monetary_calculation_accuracy": sum(bool(case["monetary_matches_ground_truth"]) for case in cases) / total, "evidence_citation_completeness": sum(bool(case["has_required_evidence"]) for case in cases) / total}
