# Revenue Assurance Investigation Agent
## Final Implementation Specification
### Snowflake CoCo CLI Hackathon 2026

**Problem Statement:** Intelligent Workflow Automation Agent  
**Participation Mode:** Solo / One-person team  
**Primary Language:** Python  
**Primary Platform:** Snowflake AI Data Cloud  
**Primary Execution Interface:** Snowflake Cortex Code CLI / CoCo CLI  
**Review Interface:** Streamlit  
**Dataset:** Fully synthetic  

---

# 0. Executive Summary

## 0.1 One-line positioning

> A CoCo CLI–executed, Snowflake-native revenue assurance workflow composed of modular Agent Skills that investigates billing discrepancies across pricing, usage, invoices, commercial exceptions, and supporting approval documents, then separates suspected revenue leakage from legitimate variance and prepares evidence-backed actions for finance review.

## 0.2 Human explanation

Enterprise pricing, usage records, invoices, commercial exceptions, and approval documents often live in separate systems.

When those systems are not synchronized, a company may:

- continue billing an old rate after an approved price increase;
- underbill usage;
- continue applying an expired concession;
- treat an exception as approved even though the source document says it is conditional;
- fail to calculate expected billing because the source data itself is inconsistent.

This system does not assume that every billing variance is an error.

It uses CoCo CLI to orchestrate three modular Agent Skills:

1. detect billing variances;
2. validate commercial evidence;
3. prepare auditable finance review cases.

Every finding is classified as one of:

- `suspected_leakage`
- `explained_variance`
- `evidence_conflict`
- `insufficient_data`

The system never creates invoices, triggers payments, updates the general ledger, or contacts customers automatically. Final financial action always requires human review.

---

# 1. Contest Alignment

## 1.1 Problem Statement alignment

This project targets:

> **Problem Statement 1 — Intelligent Workflow Automation Agent**

The workflow demonstrates:

- understanding of enterprise data;
- multi-step orchestration;
- anomaly detection;
- contextual reasoning;
- decision branches;
- error handling;
- modular Agent Skills;
- end-to-end execution through CoCo CLI;
- minimal manual intervention before human review.

| Contest expectation | Project implementation |
|---|---|
| Understand enterprise data | Contracts, pricing, usage, invoices, exceptions, approval documents |
| Identify anomalies | Pricing mismatch, underbilling, expired exceptions, conflicting usage |
| Multi-step orchestration | Three Agent Skills executed through CoCo CLI |
| Reason over data | Structured records compared with approval documents |
| Trigger contextual actions | Create review cases, close explained variances, assign data issues |
| Handle decision branches | Different evidence produces different classifications |
| CLI end-to-end workflow | Primary demo runs through CoCo CLI |
| Minimal manual intervention | One investigation prompt, followed by human review |

## 1.2 Required technologies

The prototype must use:

- Snowflake Cortex Code CLI / CoCo CLI;
- Snowflake;
- Python;
- a working prototype;
- accessible source code;
- an English presentation and documentation.

This project uses:

```text
CoCo CLI
Python
Snowflake tables
Snowflake SQL stored procedures
Cortex Search
Agent Skills
Streamlit
GitHub
```

## 1.3 Dataset declaration

All project data is fully synthetic.

Use this statement in the submission:

> Dataset type: Fully synthetic.  
> Created specifically for the Snowflake CoCo CLI Hackathon prototype.  
> It contains no real customer, contract, invoice, employee, payment, or personally identifiable information.  
> No third-party dataset or API is required.

---

# 2. Final Architecture

## 2.1 Architecture overview

```text
User / Finance Analyst
        |
        v
Snowflake CoCo CLI
        |
        +-------------------------------+
        |                               |
        v                               v
Skill 1                         Project context
Detect Billing Variances        AGENTS.md / prompts
        |
        v
Deterministic Snowflake SQL tools
        |
        v
Skill 2
Validate Commercial Evidence
        |
        +---------------+
        |               |
        v               v
Structured data     Cortex Search
exceptions          approval emails
pricing terms       amendment texts
        \               /
         +-------------+
                |
                v
Skill 3
Prepare Finance Review Case
                |
                v
investigation_cases
case_evidence
investigation_runs
agent_tool_calls
                |
                v
Streamlit Review Interface
        |
        +-- Summary
        +-- Case Queue
        +-- Evidence Trail
        +-- Accept / Dismiss / Assign
```

## 2.2 Component responsibilities

### CoCo CLI

CoCo CLI is the main workflow execution and orchestration interface.

It is responsible for:

- reading the user's investigation request;
- discovering and invoking project Agent Skills;
- executing Snowflake SQL;
- invoking Cortex Search;
- deciding investigation depth based on intermediate results;
- completing the end-to-end workflow;
- producing the final investigation summary.

### Agent Skills

Agent Skills define reusable investigation stages.

They are responsible for orchestration and business reasoning, not authoritative monetary calculation.

### Stored procedures

Stored procedures perform:

- expected billing calculation;
- effective-date checks;
- variance detection;
- duplicate-data detection;
- deterministic monetary calculation;
- case persistence;
- review-state updates.

### Cortex Search

Cortex Search retrieves:

- approval emails;
- pricing amendments;
- concession approvals;
- supporting exception documents.

### Streamlit

Streamlit is the finance review interface.

It displays persisted findings and supports human review. It is not the sole investigation engine.

---

# 3. Repository Structure

```text
revenue-assurance-agent/
├── AGENTS.md
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
│
├── docs/
│   ├── implementation-spec.md
│   ├── architecture.md
│   ├── official-rules-alignment.md
│   ├── dataset-declaration.md
│   ├── evaluation-plan.md
│   ├── evaluation-report.md
│   ├── demo-script.md
│   └── known-limitations.md
│
├── .snowflake/
│   └── cortex/
│       └── skills/
│           ├── detect-billing-variances/
│           │   ├── SKILL.md
│           │   └── references/
│           ├── validate-commercial-evidence/
│           │   ├── SKILL.md
│           │   └── references/
│           └── prepare-finance-review-case/
│               ├── SKILL.md
│               └── references/
│
├── prompts/
│   ├── run_q3_investigation.md
│   ├── investigate_customer.md
│   └── generate_finance_summary.md
│
├── sql/
│   ├── 001_database_setup.sql
│   ├── 002_schema.sql
│   ├── 003_seed_golden_cases.sql
│   ├── 004_seed_evaluation_cases.sql
│   ├── 005_scan_billing_variances.sql
│   ├── 006_get_pricing_evidence.sql
│   ├── 007_get_commercial_exceptions.sql
│   ├── 008_create_investigation_case.sql
│   ├── 009_case_evidence.sql
│   ├── 010_review_actions.sql
│   ├── 011_run_audit.sql
│   └── 012_ground_truth.sql
│
├── search/
│   ├── documents/
│   │   ├── DOC-0001-kensington-approval.txt
│   │   ├── DOC-0044-brightfarm-conditional.txt
│   │   ├── PT-0142-nova-pricing-amendment.txt
│   │   └── README.md
│   ├── upload_documents.sql
│   └── setup_search_service.sql
│
├── app/
│   ├── app.py
│   ├── config.py
│   ├── pages/
│   │   ├── summary.py
│   │   ├── case_queue.py
│   │   └── evidence_trail.py
│   ├── components/
│   │   ├── metrics.py
│   │   ├── case_table.py
│   │   └── evidence_card.py
│   └── services/
│       ├── snowflake_service.py
│       ├── review_service.py
│       └── investigation_runner.py
│
├── scripts/
│   ├── validate_environment.py
│   ├── setup_project.py
│   ├── run_cli_demo.sh
│   ├── run_cli_demo.ps1
│   ├── run_evaluation.py
│   └── verify_database.py
│
└── tests/
    ├── test_expected_billing.py
    ├── test_date_boundaries.py
    ├── test_variance_detection.py
    ├── test_case_upsert.py
    ├── test_insufficient_data.py
    └── test_evaluation_cases.py
```

---

# 4. Three Modular Agent Skills

## 4.1 Skill 1 — Detect Billing Variances

### Skill name

```text
detect-billing-variances
```

### Purpose

Identify billing discrepancies and source-data anomalies for a requested review period.

### Inputs

```text
period_start DATE
period_end DATE
```

### Tools

```text
scan_billing_variances(period_start, period_end)
get_pricing_evidence(customer_id, period_start, period_end)
```

### Responsibilities

- calculate expected billing;
- aggregate actual invoice lines;
- identify gross variance;
- detect duplicate usage records;
- detect missing invoices;
- detect pricing mismatches;
- output findings requiring investigation.

### Output fields

```text
customer_id
affected_period_start
affected_period_end
variance_type
gross_variance
data_quality_status
pricing_term_ids
invoice_line_ids
```

### Rules

- Do not make the final leakage classification.
- Do not use the LLM for monetary arithmetic.
- If source data is inconsistent, flag a data-quality issue.
- Every amount must come from deterministic SQL output.

---

## 4.2 Skill 2 — Validate Commercial Evidence

### Skill name

```text
validate-commercial-evidence
```

### Purpose

Determine whether a billing variance is explained by a valid commercial exception and verify whether the structured record agrees with its source document.

### Inputs

```text
customer_id
period_start
period_end
gross_variance
```

### Tools

```text
get_commercial_exceptions(
    customer_id,
    period_start,
    period_end
)

search_approval_documents
```

### Responsibilities

- query applicable commercial exceptions;
- validate effective-date coverage;
- inspect approval status;
- retrieve the linked source document;
- compare structured records with document text;
- distinguish explained, partially explained, conflicting, and unsupported findings.

### Decision branches

```text
No exception
→ Run a negative-evidence document search for material variance
→ Candidate suspected_leakage

Valid exception + matching document
→ explained_variance

Exception covers only part of the period
→ Split covered and uncovered sub-periods

Structured record says approved
+ supporting document says conditional
→ evidence_conflict

Conflicting source data
→ insufficient_data
```

### Rules

- A failed document search does not prove that no real-world approval exists.
- Use the wording: "No contradictory evidence retrieved from indexed sources."
- Never use the phrase "confirmed recoverable amount."
- When an exception is marked approved, inspect the linked source document before finalizing.

---

## 4.3 Skill 3 — Prepare Finance Review Case

### Skill name

```text
prepare-finance-review-case
```

### Purpose

Convert an investigation result into an auditable finance review case.

### Tools

```text
create_investigation_case(...)
case evidence persistence
investigation run audit
```

### Responsibilities

- select the primary status;
- select coverage;
- select confidence tier;
- calculate explained and unexplained portions from deterministic outputs;
- generate an evidence summary;
- generate a recommended human action;
- upsert an investigation case;
- persist case evidence;
- produce a CLI summary.

### Primary statuses

```text
suspected_leakage
explained_variance
evidence_conflict
insufficient_data
```

### Coverage

```text
full_period
partial_period
```

### Safety boundary

The Skill must never:

- create an invoice;
- send an email;
- update the general ledger;
- trigger a payment;
- change a customer balance;
- automatically close a finance case.

---

# 5. Deterministic Tools

Use the following description consistently:

> **4 custom deterministic stored-procedure tools + 1 Cortex Search tool**

## Tool 1

```text
scan_billing_variances(
    period_start DATE,
    period_end DATE
)
```

## Tool 2

```text
get_pricing_evidence(
    customer_id STRING,
    period_start DATE,
    period_end DATE
)
```

## Tool 3

```text
get_commercial_exceptions(
    customer_id STRING,
    period_start DATE,
    period_end DATE
)
```

## Tool 4

```text
create_investigation_case(
    run_id STRING,
    customer_id STRING,
    review_period_label STRING,
    review_period_start DATE,
    review_period_end DATE,
    status STRING,
    coverage STRING,
    affected_period_start DATE,
    affected_period_end DATE,
    gross_variance NUMBER,
    explained_amount NUMBER,
    unexplained_amount NUMBER,
    confidence_tier STRING,
    evidence_summary STRING,
    recommended_action STRING
)
```

## Native Tool 5

```text
search_approval_documents
```

Type:

```text
Cortex Search
```

---

# 6. Data Model

## 6.1 Contracts

```sql
CREATE OR REPLACE TABLE contracts (
    contract_id STRING,
    customer_id STRING,
    customer_name STRING,
    billing_model STRING,
    currency STRING DEFAULT 'USD',
    start_date DATE,
    status STRING
);
```

Supported billing models:

```text
flat
usage_based
```

## 6.2 Pricing Terms

```sql
CREATE OR REPLACE TABLE pricing_terms (
    term_id STRING,
    contract_id STRING,
    term_type STRING,
    value NUMBER(18,6),
    value_type STRING,
    effective_start_date DATE,
    effective_end_date DATE,
    approval_status STRING,
    source_document_id STRING
);
```

Supported term types:

```text
flat_fee
usage_rate
```

The MVP does not support:

- tiered pricing;
- proration;
- multiple currencies;
- tax;
- minimum commitments;
- volume bands.

## 6.3 Usage Records

```sql
CREATE OR REPLACE TABLE usage_records (
    usage_id STRING,
    customer_id STRING,
    billing_period_start DATE,
    billing_period_end DATE,
    units_used NUMBER(18,2)
);
```

Usage records contain usage facts only.

Pricing must come from `pricing_terms`.

## 6.4 Invoices

```sql
CREATE OR REPLACE TABLE invoices (
    invoice_id STRING,
    customer_id STRING,
    billing_period_start DATE,
    billing_period_end DATE,
    total_amount NUMBER(18,2)
);
```

## 6.5 Invoice Lines

```sql
CREATE OR REPLACE TABLE invoice_lines (
    invoice_line_id STRING,
    invoice_id STRING,
    charge_type STRING,
    quantity NUMBER(18,2),
    unit_rate NUMBER(18,6),
    net_amount NUMBER(18,2)
);
```

Supported charge types:

```text
base_fee
usage_charge
discount
credit
```

## 6.6 Commercial Exceptions

```sql
CREATE OR REPLACE TABLE commercial_exceptions (
    exception_id STRING,
    customer_id STRING,
    exception_type STRING,
    approved_amount_or_rate NUMBER(18,6),
    effective_start_date DATE,
    effective_end_date DATE,
    approval_status STRING,
    approved_by STRING,
    source_document_id STRING
);
```

Supported exception types:

```text
retention_concession
service_credit
dispute_hold
goodwill_credit
```

Approval statuses:

```text
approved
pending
conditional
expired
```

## 6.7 Investigation Runs

```sql
CREATE OR REPLACE TABLE investigation_runs (
    run_id STRING DEFAULT UUID_STRING(),
    review_period_start DATE,
    review_period_end DATE,
    run_status STRING,
    initiated_by STRING,
    started_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    completed_at TIMESTAMP_NTZ
);
```

Run statuses:

```text
running
completed
failed
```

## 6.8 Investigation Cases

```sql
CREATE OR REPLACE TABLE investigation_cases (
    case_id STRING,
    customer_id STRING,

    review_period_label STRING,
    review_period_start DATE,
    review_period_end DATE,

    status STRING,
    coverage STRING,

    affected_period_start DATE,
    affected_period_end DATE,

    gross_variance NUMBER(18,2),
    explained_amount NUMBER(18,2),
    unexplained_amount NUMBER(18,2),

    confidence_tier STRING,

    evidence_summary STRING,
    recommended_action STRING,

    review_status STRING DEFAULT 'pending',
    reviewed_by STRING,
    reviewed_at TIMESTAMP_NTZ,
    review_comment STRING,

    run_id STRING,
    finding_key STRING,

    updated_at TIMESTAMP_NTZ,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

Review statuses:

```text
pending
accepted_for_billing_review
dismissed
assigned
```

## 6.9 Case Evidence

```sql
CREATE OR REPLACE TABLE case_evidence (
    case_id STRING,
    evidence_type STRING,
    evidence_id STRING,
    evidence_excerpt STRING,
    source_tool STRING,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

Evidence types:

```text
pricing_term
exception
document
invoice_line
usage_record
```

## 6.10 Agent Tool Calls

```sql
CREATE OR REPLACE TABLE agent_tool_calls (
    tool_call_id STRING DEFAULT UUID_STRING(),
    run_id STRING,
    case_id STRING,
    tool_name STRING,
    input_summary STRING,
    output_summary STRING,
    call_status STRING,
    called_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

Do not store hidden chain-of-thought.

Only store:

- tool name;
- safe input summary;
- safe output summary;
- success or failure;
- timestamp.

---

# 7. Investigation Case Upsert

## 7.1 Finding identity

The `finding_key` must not contain `status`, because a classification may change when new evidence is added.

MVP finding key:

```text
customer_id
+ affected_period_start
+ affected_period_end
```

Possible future extension:

```text
customer_id
+ variance_type
+ pricing_term_id
+ affected_period_start
+ affected_period_end
```

## 7.2 Upsert behavior

Repeated execution for the same finding must:

- avoid duplicate cases;
- update classification;
- update amounts;
- update evidence summary;
- update `run_id`;
- update timestamp;
- preserve the same `case_id`.

## 7.3 Procedure

```sql
CREATE OR REPLACE PROCEDURE create_investigation_case(
    run_id STRING,
    customer_id STRING,
    review_period_label STRING,
    review_period_start DATE,
    review_period_end DATE,
    status STRING,
    coverage STRING,
    affected_period_start DATE,
    affected_period_end DATE,
    gross_variance NUMBER,
    explained_amount NUMBER,
    unexplained_amount NUMBER,
    confidence_tier STRING,
    evidence_summary STRING,
    recommended_action STRING
)
RETURNS STRING
LANGUAGE SQL
AS
$$
DECLARE
    v_finding_key STRING;
    v_case_id STRING;
BEGIN
    v_finding_key :=
        :customer_id
        || '|'
        || TO_VARCHAR(:affected_period_start)
        || '|'
        || TO_VARCHAR(:affected_period_end);

    v_case_id := UUID_STRING();

    MERGE INTO investigation_cases AS tgt
    USING (
        SELECT :v_finding_key AS finding_key
    ) AS src
    ON tgt.finding_key = src.finding_key

    WHEN MATCHED THEN UPDATE SET
        status = :status,
        coverage = :coverage,
        gross_variance = :gross_variance,
        explained_amount = :explained_amount,
        unexplained_amount = :unexplained_amount,
        confidence_tier = :confidence_tier,
        evidence_summary = :evidence_summary,
        recommended_action = :recommended_action,
        run_id = :run_id,
        review_period_label = :review_period_label,
        review_period_start = :review_period_start,
        review_period_end = :review_period_end,
        updated_at = CURRENT_TIMESTAMP()

    WHEN NOT MATCHED THEN INSERT (
        case_id,
        run_id,
        customer_id,
        review_period_label,
        review_period_start,
        review_period_end,
        status,
        coverage,
        affected_period_start,
        affected_period_end,
        gross_variance,
        explained_amount,
        unexplained_amount,
        confidence_tier,
        evidence_summary,
        recommended_action,
        finding_key,
        updated_at
    )
    VALUES (
        :v_case_id,
        :run_id,
        :customer_id,
        :review_period_label,
        :review_period_start,
        :review_period_end,
        :status,
        :coverage,
        :affected_period_start,
        :affected_period_end,
        :gross_variance,
        :explained_amount,
        :unexplained_amount,
        :confidence_tier,
        :evidence_summary,
        :recommended_action,
        :v_finding_key,
        CURRENT_TIMESTAMP()
    );

    SELECT MAX(case_id)
    INTO :v_case_id
    FROM investigation_cases
    WHERE finding_key = :v_finding_key;

    RETURN v_case_id;
END;
$$;
```

---

# 8. Q3 2026 Golden Cases

Review period:

```text
2026-07-01 to 2026-09-30
```

Main request:

> Investigate billing integrity from 2026-07-01 to 2026-09-30.

## 8.1 Case 1 — Nova Retail

### Situation

Approved pricing term:

```text
Previous monthly fee: $18,000
New monthly fee: $21,000
Effective date: 2026-01-01
```

Invoices:

```text
July: $18,000
August: $18,000
September: $18,000
```

Variance:

```text
($21,000 - $18,000) × 3 = $9,000
```

Commercial exceptions:

```text
None
```

Document result:

```text
No contradictory evidence retrieved from indexed sources.
```

### Expected output

```text
status = suspected_leakage
coverage = full_period
gross_variance = 9000
explained_amount = 0
unexplained_amount = 9000
confidence_tier = high
```

### Recommended action

> Escalate to finance for billing correction review. The billing system did not apply the active approved pricing term for Q3 2026. Final recoverability remains subject to finance confirmation.

## 8.2 Case 2 — Kensington Labs

### Situation

Invoice variance:

```text
$2,000 per month × 3 months = $6,000
```

Structured exception:

```text
Type: retention_concession
Amount: $2,000 per month
Effective: 2026-07-01 to 2026-09-30
Approval status: approved
Approved by: J. Tan
```

Cortex Search result:

```text
Linked approval email confirms the concession was formally approved
for the full Q3 period.
```

### Expected output

```text
status = explained_variance
coverage = full_period
gross_variance = 6000
explained_amount = 6000
unexplained_amount = 0
```

### Recommended action

> No billing correction is required. Close the investigation as an approved commercial variance.

## 8.3 Case 3 — BrightFarm Co

### Situation

July exception:

```text
Approved and valid
```

August–September structured exception:

```text
approval_status = approved
approved_by = J. Tan
source_document_id = DOC-0044
```

Source document:

> The extension is approved in principle, subject to CFO final approval. Please do not apply it to billing yet.

CFO final approval log:

```text
No corresponding final approval
```

Variance:

```text
$500 × 2 months = $1,000
```

### Expected output

```text
status = evidence_conflict
coverage = partial_period
affected_period = 2026-08-01 to 2026-09-30
gross_variance = 1000
explained_amount = 0
unexplained_amount = 1000
confidence_tier = needs_investigation
```

### Recommended action

> Escalate to finance because the exception registry conflicts with the supporting approval document. Confirm whether CFO approval was completed before treating the amount as leakage or explained variance.

## 8.4 Case 4 — Summit Manufacturing

### Situation

September usage records:

```text
Record A: 4,200 units
Record B: 3,850 units
```

The records have the same customer and billing period but conflicting values.

### Expected output

```text
status = insufficient_data
coverage = partial_period
gross_variance = NULL
explained_amount = NULL
unexplained_amount = NULL
confidence_tier = needs_investigation
```

### Recommended action

> Assign to the data quality team. The duplicate and conflicting September usage records must be reconciled before financial calculation or billing review.

---

# 9. Confidence Rules

## 9.1 Deterministic checks

A `suspected_leakage` finding may receive `high` confidence only when:

1. An active approved pricing term applies to the period.
2. The invoice rate or amount does not match the term.
3. The discrepancy persists for at least two billing periods.
4. No valid structured commercial exception covers the period.

## 9.2 Document check

Record document coverage separately:

```text
Document coverage:
No contradictory evidence retrieved from indexed sources.
```

This does not prove that no other real-world approval exists.

It only means that no contradictory evidence was found in the indexed document collection.

## 9.3 Confidence values

```text
high
medium
needs_investigation
```

Do not generate arbitrary numerical confidence percentages.

---

# 10. End-to-End CLI Workflow

## 10.1 Main prompt file

File:

```text
prompts/run_q3_investigation.md
```

Content:

```text
Investigate billing integrity from 2026-07-01 to 2026-09-30.

Use the available project Agent Skills to:

1. detect billing variances and source-data conflicts;
2. validate pricing terms, commercial exceptions, and supporting approval documents;
3. classify every finding;
4. create or update auditable finance review cases;
5. produce a final summary.

Do not classify a difference as leakage before checking applicable exceptions.

Do not perform financial calculation when source data is internally inconsistent.

Do not trigger invoices, payments, ledger updates, customer notifications, or any other external financial action.

Return:
- suspected leakage amount;
- explained variance amount;
- evidence-conflict amount;
- number of insufficient-data cases;
- created or updated case IDs;
- supporting evidence references.
```

## 10.2 CLI execution

Example:

```bash
cortex -c hackathon -w . -f prompts/run_q3_investigation.md
```

The exact CLI executable and flags must be verified against the installed CoCo CLI version.

The README must document the command that was actually tested.

## 10.3 Expected CLI output

```text
Revenue Assurance Investigation
Review period: 2026-07-01 to 2026-09-30

Skill: detect-billing-variances
- 4 findings identified
- 1 source-data conflict detected

Skill: validate-commercial-evidence
- Nova Retail: no valid exception found
- Kensington Labs: structured exception matches approval document
- BrightFarm Co: structured exception conflicts with approval document
- Summit Manufacturing: conflicting usage records

Skill: prepare-finance-review-case
- 4 cases created or updated

Final summary:
Gross variance detected: $16,000
Explained variance: $6,000
Suspected leakage: $9,000
Evidence conflict: $1,000
Data-quality cases: 1
```

---

# 11. Streamlit Review UI

## 11.1 Screen 1 — Investigation Summary

Display:

```text
Gross variance detected: $16,000
Explained variance: $6,000
Suspected leakage pending finance confirmation: $9,000
Evidence conflict requiring resolution: $1,000
Data-quality cases: 1
```

Do not combine suspected leakage and evidence conflict into one recoverable amount.

## 11.2 Screen 2 — Case Queue

| Customer | Status | Coverage | Amount | Confidence | Action |
|---|---|---|---:|---|---|
| Nova Retail | Suspected leakage | Full | $9,000 | High | Review |
| Kensington Labs | Explained variance | Full | $6,000 | — | Closed |
| BrightFarm Co | Evidence conflict | Partial | $1,000 | Needs investigation | Review |
| Summit Manufacturing | Insufficient data | Partial | — | Needs investigation | Assign |

## 11.3 Screen 3 — Evidence Trail

Display evidence in logical order:

1. Pricing term
2. Invoice line
3. Usage record
4. Commercial exception
5. Cortex Search result
6. Agent classification
7. Recommended action
8. Human review decision

Each evidence item must display:

```text
Evidence type
Evidence ID
Source tool
Relevant excerpt
Timestamp
```

## 11.4 Human actions

Allowed buttons:

```text
Accept finding
Dismiss
Assign to data team
```

### Accept finding

Updates:

```text
review_status = accepted_for_billing_review
reviewed_by
reviewed_at
review_comment
```

It must not:

- create an invoice;
- update billing;
- send an email;
- update the general ledger;
- debit or credit an account;
- contact a customer.

---

# 12. Cortex Agent Position

A separate Cortex Agent API implementation is optional.

It is not a blocking MVP requirement.

## Core MVP

```text
CoCo CLI
+ 3 Agent Skills
+ Snowflake stored procedures
+ Cortex Search
+ Streamlit review UI
```

## Optional enhancement

A Cortex Agent may reuse the same:

- tool definitions;
- investigation rules;
- Cortex Search service;
- stored procedures.

A lack of container runtime or Cortex Agent API permissions must not block the primary CLI workflow.

---

# 13. Streamlit Runtime Strategy

Because the main investigation runs through CoCo CLI, Streamlit only needs to read and update Snowflake tables.

## Preferred

```text
Streamlit in Snowflake warehouse runtime
```

Use it for:

- reading investigation cases;
- displaying evidence;
- updating review status.

## Optional

Container runtime may be used if available, but it is not required for the core workflow.

## Fallback

External Streamlit may connect to Snowflake through environment-based credentials.

No credentials may be committed to GitHub.

---

# 14. Evaluation Set

In addition to the four golden demo cases, create twelve evaluation cases.

## Categories

```text
2 valid pricing updates
2 valid concessions
2 expired or conditional exceptions
2 conflicting usage-data cases
2 effective-date boundary cases
2 fully normal billing cases
```

## Required metrics

### Variance detection recall

```text
Detected known discrepancies / total known discrepancies
```

### Investigation classification accuracy

```text
Correct classifications / total test findings
```

### False-positive rate

Valid billing incorrectly classified as `suspected_leakage`.

Target:

```text
0%
```

### Evidence citation completeness

Percentage of cases containing applicable:

```text
term_id
invoice_line_id
exception_id
source_document_id
```

### Unsafe action rate

Cases where the system produces a financial adjustment recommendation despite insufficient data.

Target:

```text
0%
```

### Monetary calculation accuracy

All values must match deterministic SQL ground truth.

Target:

```text
100%
```

---

# 15. Error Handling

## 15.1 Conflicting usage records

```text
Stop financial calculation
Classify as insufficient_data
Assign to data quality team
```

## 15.2 Missing pricing term

```text
Do not assume a rate
Classify as insufficient_data
```

## 15.3 Missing invoice

```text
Flag as potential missing billing
Require finance review
```

## 15.4 Cortex Search unavailable

```text
Do not silently classify a structured exception as fully validated
Mark document validation as pending
Continue storing deterministic findings
```

## 15.5 CoCo CLI tool failure

```text
Log the tool failure
Set run_status to failed or partial
Do not create unsupported financial conclusions
```

## 15.6 Duplicate execution

```text
Upsert the existing finding
Return the existing case_id
Do not create a duplicate active case
```

---

# 16. AGENTS.md Requirements

`AGENTS.md` must include:

```text
Project purpose
Authoritative specification path
Repository structure
Required test commands
Snowflake setup commands
CoCo CLI demo command
Deterministic financial calculation rule
Human-review boundary
No-secret-commit rule
No silent replacement of SQL calculations with LLM arithmetic
```

Required rule:

> Financial calculations, effective-date comparisons, and variance amounts must be produced by deterministic SQL or Python tests. LLM output may explain results but must not be treated as the source of truth for monetary values.

---

# 17. Implementation Execution Strategy

The project does not need to follow the schedule one day at a time.

The plan represents:

- priority;
- dependency;
- validation gate;
- latest acceptable milestone.

Independent components may be developed in parallel.

## Gate 1 — Account and CLI validation

Confirm:

- Snowflake trial account;
- CoCo CLI installation;
- connection;
- warehouse;
- database;
- schema;
- Cortex Search availability.

## Gate 2 — Minimal vertical workflow

Must run:

```text
CoCo CLI
→ one Skill
→ one SQL tool
→ one Search call
→ one case output
```

## Gate 3 — Complete backend workflow

Must run:

```text
detect
→ validate
→ classify
→ persist
→ audit
```

## Gate 4 — Review UI

Must display and update persisted findings.

## Gate 5 — Evaluation and submission

Must run all evaluation cases and prepare submission artifacts.

---

# 18. Codex Execution Instructions

Implement the complete project described in `docs/implementation-spec.md`.

Treat that document as the authoritative implementation specification.

This is an implementation task, not a planning task. Begin creating the project immediately and continue until all feasible components are complete, tested, documented, and ready for demonstration.

The project must prioritize an end-to-end CoCo CLI workflow composed of three modular Agent Skills:

1. `detect-billing-variances`
2. `validate-commercial-evidence`
3. `prepare-finance-review-case`

The primary demo must run through CoCo CLI. Streamlit is a finance review interface, not the sole investigation engine. A separate Cortex Agent API integration is optional and must not block the core implementation.

The execution schedule in the specification defines dependencies and validation gates. It does not restrict work to one task per day. Work on independent components in parallel.

Implement:

- repository structure;
- `AGENTS.md`;
- Snowflake DDL;
- synthetic golden-case data;
- evaluation data;
- deterministic stored procedures;
- three Agent Skills with `SKILL.md` files;
- Cortex Search fixtures and setup;
- CoCo CLI prompt files and demo scripts;
- case upsert and audit persistence;
- Streamlit summary, queue, and evidence views;
- review-state write-back;
- tests;
- evaluation scripts;
- README;
- deployment and demo documentation.

Use deterministic SQL or Python ground truth for all monetary calculations, date coverage, variance detection, duplicate-data checks, and case persistence.

Do not let an LLM perform authoritative financial arithmetic.

Do not allow the system to automatically create invoices, trigger payments, contact customers, update ledgers, or perform financial transactions.

If Snowflake credentials or account access are not yet available, complete every environment-independent component, provide setup and validation scripts, clearly mark live Snowflake validation as pending, and do not falsely claim Snowflake functionality was executed.

Do not stop after producing a plan or scaffold.

When complete, report:

1. architecture implemented;
2. files created or modified;
3. commands executed;
4. tests passed and failed;
5. Snowflake capabilities actually verified;
6. manual Snowflake setup steps still required;
7. exact CoCo CLI demo command;
8. exact Streamlit launch command;
9. known limitations;
10. deviations from the specification and justification.

---

# 19. Demo Sequence

## Part 1 — Problem

Explain:

> Revenue leakage is often not caused by one obvious billing error. It happens when pricing, usage, invoices, commercial exceptions, and approval documents disagree across systems.

## Part 2 — CLI execution

Run:

```bash
cortex -c hackathon -w . -f prompts/run_q3_investigation.md
```

Show the three Skills being used.

## Part 3 — Decision branches

Highlight:

- Nova: no valid exception;
- Kensington: exception and document agree;
- BrightFarm: exception and document conflict;
- Summit: source-data conflict causes refusal.

## Part 4 — Output

Show:

```text
Suspected leakage: $9,000
Explained variance: $6,000
Evidence conflict: $1,000
Data-quality cases: 1
```

## Part 5 — Streamlit

Open:

- Summary;
- Case Queue;
- Evidence Trail.

## Part 6 — Human review

Click:

```text
Accept finding
Dismiss
Assign to data team
```

Explain that no actual financial action is triggered.

---

# 20. Submission Deliverables

## Idea

Include:

- problem;
- users;
- measurable impact;
- workflow;
- Snowflake usage.

## Prototype

Include:

- functioning CoCo CLI workflow;
- three Agent Skills;
- Snowflake tables;
- deterministic tools;
- Cortex Search;
- Streamlit review UI.

## Presentation deck

Recommended sections:

1. Title
2. Revenue leakage problem
3. Current process failure
4. Proposed solution
5. Agent Skills workflow
6. Snowflake architecture
7. Golden cases
8. Live demo
9. Evaluation results
10. Safety and limitations
11. Business impact
12. Future roadmap

## Source code

Provide a public or judge-accessible GitHub repository.

## Documentation

Include:

- README;
- setup instructions;
- architecture;
- dataset declaration;
- evaluation report;
- known limitations;
- demo runbook.

---

# 21. Known Limitations

The MVP supports:

- flat monthly pricing;
- single-rate usage billing;
- one currency;
- synthetic cleaned text documents;
- manual CLI investigation trigger;
- human review.

The MVP does not support:

- tiered pricing;
- proration;
- multiple currencies;
- tax;
- OCR;
- ERP integration;
- formal invoice generation;
- customer notification;
- automatic payment action;
- full contract lifecycle management;
- legal determination of recoverability.

---

# 22. Future Expansion

Possible future capabilities:

- tiered and usage-band pricing;
- ERP and billing-system connectors;
- scheduled scans;
- role-based approvals;
- customer-level risk scoring;
- multi-currency handling;
- contract PDF extraction;
- finance-system reconciliation;
- workflow notifications;
- Cortex Agent API reuse;
- Marketplace datasets;
- industry-specific billing models.

---

# 23. Final Success Definition

The project is complete when:

1. CoCo CLI executes the full Q3 investigation.
2. Three modular Agent Skills are discovered and used.
3. Snowflake SQL deterministically calculates all monetary values.
4. Cortex Search validates approval documents.
5. All four golden cases produce the expected branches.
6. Investigation cases are persisted without duplication.
7. Evidence references are stored.
8. Streamlit displays results and permits human review.
9. Insufficient data never produces an authoritative monetary recommendation.
10. Evaluation results are reported.
11. README commands are reproducible.
12. No secrets or real confidential data are committed.

---

# 24. Final Project Positioning

> Revenue Assurance Investigation Agent is not a generic finance chatbot and not merely a billing dashboard. It is a CoCo CLI–executed, evidence-aware workflow that combines deterministic financial reconciliation with modular Agent Skills and document validation to investigate discrepancies, explain legitimate variances, surface conflicting approvals, and prepare auditable finance review cases.
