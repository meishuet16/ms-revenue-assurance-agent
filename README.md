# 💸 Revenue Assurance Investigation Agent

> **Find the billing variance. Check the commercial evidence. Show finance exactly why it matters — without letting an AI touch the ledger.**

A Snowflake + CoCo CLI revenue assurance workflow for investigating Q3 billing discrepancies. It combines deterministic financial reconciliation, evidence-aware investigation, and an interactive Streamlit review experience so finance teams can move from **“there is a variance”** to **“here is what happened, what evidence supports it, and what a human should review next.”**

**Hackathon track:** Problem Statement 1 — Intelligent Workflow Automation Agent  
**Data:** 100% synthetic — no real customer, contract, invoice, employee, payment, or PII data.

---

## 🎯 Problem Statement

Finance teams can usually see that two numbers do not match. The harder part is answering **why**.

A billing variance might be:

- 💰 real revenue leakage that needs investigation;
- ✅ an approved discount or commercial concession;
- ⚠️ a conflict between structured records and the source approval document; or
- 🧩 a data-quality problem where there is not enough trustworthy information to calculate anything safely.

That investigation is often spread across pricing tables, usage records, invoice lines, exception records, and approval documents. If finance acts too early, it can create a false correction. If it acts too late, genuine leakage stays unresolved.

### The challenge

**How can an intelligent workflow agent investigate billing variances end-to-end, explain the evidence behind its conclusion, and reduce manual review work without giving the AI authority to make financial changes?**

---

## ✨ Our Solution

The **Revenue Assurance Investigation Agent** separates what machines are good at from what humans must still own.

| Layer | What it does |
| --- | --- |
| 🧮 **Deterministic finance logic** | Calculates expected billing, actual billing, date boundaries, usage and monetary variance using SQL/Python — not LLM arithmetic. |
| 🔎 **Evidence-aware investigation** | Checks pricing terms, commercial exceptions and supporting approval evidence before deciding what the variance means. |
| 🧠 **Agent workflow** | Chooses the appropriate investigation branch and records the checks it executed. |
| 🖥️ **Finance review UI** | Turns findings into a case queue, evidence trail and replayable investigation graph. |
| 👤 **Human decision boundary** | Finance remains responsible for confirming leakage and approving any real-world correction. |

The result is not just a red number on a dashboard. Each case carries its **classification, amount, evidence, confidence, investigation path, and recommended human next action**.

### Four possible outcomes

`Suspected leakage` · `Explained variance` · `Evidence conflict` · `Insufficient data`

And importantly, the agent **does not** create invoices, update ledgers, trigger payments, contact customers, change balances, or automatically close finance cases.

---

## 🧭 User Flow — what actually happens?

```text
Q3 billing + usage + pricing data
              │
              ▼
      1. Detect variance
              │
              ▼
      2. Check data integrity ──────── bad/conflicting usage
              │                              │
              │                              └──► 🧩 Insufficient data
              ▼
      3. Validate pricing terms
              │
              ▼
      4. Look for commercial exception
          │                 │
       none              exception exists
          │                 │
          ▼                 ▼
   💰 Suspected       Check approval evidence
      leakage           │             │
                     matches       conflicts
                        │             │
                        ▼             ▼
                  ✅ Explained   ⚠️ Evidence
                     variance       conflict
                         \           /
                          \         /
                           ▼       ▼
                    5. Prepare review case
                              │
                              ▼
                    👤 Finance reviews
```

### From the finance user's point of view

1. **Open Summary** → see the Q3 exposure and how cases are distributed.
2. **Open Case Queue** → choose the customer/variance that needs attention.
3. **Inspect Evidence Trail** → see pricing, invoice, exception/document evidence and the runtime investigation trace.
4. **Open Agent Investigation Graph** → press **▶ Replay Investigation** to watch the executed branch step-by-step, including evidence entering the decision context and the final verdict.
5. **Review the recommended action** → the system prepares the case; the human decides what happens next.

The replay shows **auditable runtime state and evidence-backed transitions**, not hidden model chain-of-thought.

---

## 🖥️ Dashboard Experience

The Streamlit app is organized around the way a reviewer would investigate a case rather than around backend tables.

### 📊 Summary
High-level Q3 metrics and decision outcomes — useful for answering “how much exposure are we looking at?”

### 📋 Case Queue
The working list for finance. Select a case, inspect its amount/status/confidence, and focus on what needs review.

### 🔍 Evidence Trail
A case-level investigation record containing supporting evidence, runtime decision trace, classification and recommended human action.

### 🕸️ Agent Investigation Graph
The demo-friendly view: select a customer and replay the investigation from the original variance signal through the checks that were actually relevant to that outcome. Executed nodes animate, untaken branches stay dim, evidence is surfaced beside the decision, and the replay ends with an explicit human-review boundary.

---

## 🧪 Synthetic Demo Scenario

The bundled Q3 dataset intentionally contains different failure modes so the workflow has to take different paths instead of returning one canned answer.

| Q3 result | Amount |
| --- | ---: |
| Gross variance detected | **$16,000** |
| Explained variance | **$6,000** |
| Suspected leakage pending finance confirmation | **$9,000** |
| Evidence conflict requiring resolution | **$1,000** |
| Data-quality cases | **1 case** |

For example, the BrightFarm scenario changes classification when its approval evidence changes: conditional/conflicting evidence produces `evidence_conflict`, matching approval evidence produces `explained_variance`, and removing the exception produces `suspected_leakage`. The same underlying variance therefore does **not** simply map to a fixed demo answer.

---

## 🏗️ How It Is Built

```text
Synthetic billing / pricing / usage / approval data
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Snowflake SQL          Approval documents
   deterministic finance      Cortex Search-ready
       reconciliation              evidence
              │                     │
              └──────────┬──────────┘
                         ▼
                 Investigation logic
               + modular Agent Skills
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Audit/evaluation       Streamlit review UI
                                   │
                                   ▼
                            👤 Human finance review
```

### Agent Skills

- `detect-billing-variances`
- `validate-commercial-evidence`
- `prepare-finance-review-case`

### Main stack

**Snowflake SQL** · **CoCo CLI / Cortex Code prompts & skills** · **Python** · **Streamlit** · **Cortex Search-ready document evidence**

There is also a deterministic local Python investigation engine, so the complete synthetic workflow can be demonstrated and evaluated without Snowflake credentials.

---

## 🚀 Run It Locally

### 1. Install

```bash
python -m venv .venv
pip install -r requirements.txt
```

Activate the environment first if needed (`.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on macOS/Linux).

### 2. Launch the dashboard

```bash
streamlit run app/app.py
```

Fixture mode is the default, so **you do not need Snowflake credentials just to explore the demo**.

Windows helper:

```powershell
scripts\run_dashboard.ps1
```

macOS/Linux helper:

```bash
bash scripts/run_dashboard.sh
```

### 3. Run the offline checks

```bash
python scripts/run_tests.py
python scripts/run_evaluation.py
```

The evaluation contains 12 synthetic cases and checks classification, monetary calculation, evidence citation and unsafe-action behavior. Mutation-style tests also verify that changing evidence can change the runtime classification.

---

## ❄️ Connect the Snowflake Path

Create `.env` from `.env.example` and add your Snowflake credentials. Then:

```bash
python scripts/validate_environment.py
python scripts/setup_project.py --dry-run
python scripts/setup_project.py
python scripts/verify_database.py
```

The setup creates the required warehouse/database objects, executes the SQL files in dependency order, loads synthetic approval documents, and attempts to create the Cortex Search service.

### Snowflake trial limitation

The project has successfully validated the core Snowflake database path, but the current trial environment reports:

```text
AI function EMBED_TEXT_768 is not available for trial accounts
```

So Cortex Search is implemented/configured but may be unavailable depending on account entitlement. To validate the rest of the live path without it:

```bash
python scripts/setup_project.py --warehouse COMPUTE_WH --skip-search
python scripts/verify_database.py --allow-missing-search
```

### CoCo CLI investigation

Once CoCo CLI/Cortex Code is installed and the account is entitled:

```bash
cortex -c hackathon -w . -f prompts/run_q3_investigation.md
```

The prompt and modular skills are part of the repo; actual Cortex Code execution still depends on the Snowflake account/profile available to the machine running the demo.

---

## 🌐 Deployment

The repo includes a `render.yaml` Blueprint for deploying the Streamlit dashboard to **Render**.

### Option A — Fixture deployment ⭐ easiest public demo

Use:

```text
SNOWFLAKE_DASHBOARD_MODE=fixture
```

This is the safest public judging/demo mode: no Snowflake secret is needed on Render, the synthetic cases remain deterministic, and reviewers can explore the complete dashboard and investigation replay.

### Option B — Live Snowflake-backed dashboard

Use:

```text
SNOWFLAKE_DASHBOARD_MODE=live
SNOWFLAKE_ACCOUNT=<account>
SNOWFLAKE_USER=<user>
SNOWFLAKE_PASSWORD=<secret>
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=REVENUE_ASSURANCE
SNOWFLAKE_SCHEMA=PUBLIC
```

Store secrets in Render environment variables — **never commit Snowflake passwords to GitHub**.

### Deploy with the Render Blueprint

Open Render's Blueprint creation page and point it at this repository:

```text
https://dashboard.render.com/blueprints/new?repo=https://github.com/meishuet16/ms-revenue-assurance-agent
```

Render will build with `pip install -r requirements.txt` and launch `streamlit run app/app.py`. After creation, use the generated `.onrender.com` service URL as the public prototype link.

For the full live/fixture switching guide, see [`docs/deployment.md`](docs/deployment.md).

---

## 🎬 2-Minute Demo Path

If you are presenting this project, the shortest story is:

1. **Summary** — “We detected $16K gross Q3 variance, but not all of it is leakage.”
2. **Case Queue** — open one suspicious case.
3. **Evidence Trail** — show that the conclusion is backed by actual evidence records and an auditable runtime trace.
4. **Agent Investigation Graph** — hit **▶ Replay Investigation** and show how a different evidence situation takes a different branch.
5. **Safety boundary** — finish with the important bit: *the agent prepares the finance case; a human still owns the financial decision.*

A longer presenter sequence is available in [`docs/demo-script.md`](docs/demo-script.md).

---

## 📁 Repository Guide

| Path | Purpose |
| --- | --- |
| `app/` | Streamlit dashboard, investigation UI and local/live service layer |
| `sql/` | Snowflake schema, seed data, reconciliation and investigation SQL |
| `skills/` | Modular agent skills used by the investigation workflow |
| `prompts/` | CoCo CLI / Cortex Code investigation prompt |
| `tests/` | Runtime, evaluation, evidence, graph and safety checks |
| `scripts/` | Setup, verification, evaluation and dashboard helpers |
| `docs/architecture.md` | System boundaries and architecture |
| `docs/deployment.md` | Render + Snowflake deployment guide |
| `docs/evaluation-plan.md` | Synthetic evaluation design |
| `docs/evaluation-report.md` | Evaluation result documentation |
| `docs/known-limitations.md` | MVP and live-environment limitations |
| `docs/dataset-declaration.md` | Synthetic dataset declaration |

---

## 🛡️ Safety by Design

This is a **revenue assurance investigation agent**, not an autonomous billing bot.

It may detect, reconcile, investigate, classify, cite evidence and recommend a next step. It may **not**:

- create or modify invoices;
- update the accounting ledger;
- trigger a payment or refund;
- contact a customer;
- change a customer balance; or
- silently decide that a financial case is closed.

> **Automation stops where financial authority begins.**

That boundary is visible in both the investigation logic and the reviewer-facing UI.
