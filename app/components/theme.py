from __future__ import annotations

import streamlit as st


THEME_CSS = """
<style>
:root {
  --ra-ink: #111827;
  --ra-muted: #667085;
  --ra-line: #d9e2ea;
  --ra-panel: #ffffff;
  --ra-soft: #f6f8fb;
  --ra-wash: #eef4f8;
  --ra-red: #b42318;
  --ra-red-bg: #fff1f0;
  --ra-green: #067647;
  --ra-green-bg: #ecfdf3;
  --ra-amber: #b54708;
  --ra-amber-bg: #fffaeb;
  --ra-blue: #155eef;
  --ra-blue-bg: #eff4ff;
  --ra-navy: #182230;
}

.stApp {
  background:
    linear-gradient(180deg, #eef4f8 0, #f7f9fb 280px, #f7f9fb 100%);
}

.stMainBlockContainer,
.block-container {
  padding-top: 0.95rem;
  padding-bottom: 2.4rem;
  max-width: 1240px;
}

h1, h2, h3 {
  color: var(--ra-ink);
  letter-spacing: 0;
}

.ra-section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin: 4px 0 14px;
}

.ra-section-header__eyebrow {
  color: var(--ra-blue);
  font-size: 0.76rem;
  font-weight: 900;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.ra-section-header__title {
  color: var(--ra-ink);
  font-size: 1.25rem;
  font-weight: 850;
  margin-top: 2px;
}

.ra-section-header__copy {
  color: var(--ra-muted);
  font-size: 0.9rem;
  line-height: 1.35;
  margin-top: 4px;
  max-width: 780px;
}

section[data-testid="stSidebar"],
div[data-testid="stSidebarCollapsedControl"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
footer {
  display: none !important;
}

header[data-testid="stHeader"] {
  background: transparent;
  height: 0;
}

div[data-testid="stTabs"] button {
  border-radius: 6px;
  color: #475467;
  font-weight: 700;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
  background: #ffffff;
  color: var(--ra-blue);
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.08);
}

div[data-testid="stTabs"] div[role="tablist"] {
  background: rgba(255, 255, 255, 0.72);
  border: 1px solid rgba(216, 224, 230, 0.95);
  border-radius: 8px;
  padding: 4px;
  gap: 4px;
  margin-bottom: 1.1rem;
}

div[data-testid="stMetric"] {
  background: var(--ra-panel);
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  padding: 14px 16px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

div[data-testid="stMetricLabel"] p {
  color: var(--ra-muted);
  font-size: 0.82rem;
}

div[data-testid="stMetricValue"] {
  color: var(--ra-ink);
  font-size: 1.55rem;
}

.ra-metric-card {
  background: var(--ra-panel);
  border: 1px solid var(--ra-line);
  border-top: 4px solid #d0d5dd;
  border-radius: 8px;
  padding: 14px 15px;
  min-height: 116px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.ra-metric-card--blue { border-top-color: var(--ra-blue); }
.ra-metric-card--danger { border-top-color: var(--ra-red); }
.ra-metric-card--success { border-top-color: var(--ra-green); }
.ra-metric-card--warning { border-top-color: var(--ra-amber); }
.ra-metric-card--neutral { border-top-color: #667085; }

.ra-metric-card__label {
  color: var(--ra-muted);
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
}

.ra-metric-card__value {
  color: var(--ra-ink);
  font-size: 1.7rem;
  font-weight: 800;
  margin-top: 4px;
}

.ra-metric-card__helper {
  color: var(--ra-muted);
  font-size: 0.78rem;
  line-height: 1.25;
  margin-top: 6px;
}

.ra-hero {
  border: 1px solid rgba(255, 255, 255, 0.28);
  background:
    linear-gradient(135deg, rgba(24, 34, 48, 0.96) 0%, rgba(26, 64, 91, 0.94) 56%, rgba(21, 94, 239, 0.82) 100%);
  border-radius: 8px;
  padding: 22px 24px;
  margin-bottom: 16px;
  box-shadow: 0 18px 38px rgba(24, 34, 48, 0.14);
}

.ra-hero__eyebrow {
  color: #b2ddff;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.ra-hero__title {
  color: #ffffff;
  font-size: 1.55rem;
  font-weight: 800;
  margin-bottom: 4px;
}

.ra-hero__copy {
  color: #d1e9ff;
  font-size: 0.96rem;
}

.ra-hero__chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

.ra-hero__chips span {
  color: #e0f2fe;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 999px;
  padding: 5px 10px;
  font-size: 0.78rem;
  font-weight: 800;
}

.ra-note {
  color: var(--ra-muted);
  background: var(--ra-soft);
  border-left: 4px solid var(--ra-blue);
  border-radius: 6px;
  padding: 10px 12px;
  margin: 10px 0 18px;
}

.ra-panel-label {
  color: var(--ra-muted);
  font-size: 0.78rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin: 2px 0 8px;
}

.ra-status-strip {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1px;
  overflow: hidden;
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  background: var(--ra-line);
  margin-bottom: 14px;
}

.ra-status-strip div {
  background: #ffffff;
  color: var(--ra-muted);
  font-size: 0.84rem;
  line-height: 1.35;
  padding: 11px 12px;
}

.ra-status-strip strong {
  color: var(--ra-ink);
}

.ra-outcome-mix {
  background: #ffffff;
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  padding: 14px 16px;
  margin: 14px 0;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.ra-outcome-mix__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 12px;
}

.ra-outcome-mix__eyebrow {
  color: var(--ra-blue);
  font-size: 0.74rem;
  font-weight: 900;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.ra-outcome-mix__title {
  color: var(--ra-ink);
  font-size: 1rem;
  font-weight: 850;
  margin-top: 1px;
}

.ra-outcome-mix__total {
  color: var(--ra-ink);
  font-size: 1.1rem;
  font-weight: 900;
}

.ra-outcome-mix__bar {
  display: flex;
  height: 12px;
  overflow: hidden;
  border-radius: 999px;
  background: #e4e7ec;
}

.ra-outcome-mix__seg {
  display: block;
  height: 100%;
}

.ra-outcome-mix__seg--danger { background: var(--ra-red); }
.ra-outcome-mix__seg--success { background: var(--ra-green); }
.ra-outcome-mix__seg--warning { background: var(--ra-amber); }

.ra-outcome-mix__legend {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  color: var(--ra-muted);
  font-size: 0.82rem;
  margin-top: 10px;
}

.ra-outcome-mix__legend span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.ra-outcome-mix__legend i {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  display: inline-block;
}

.ra-outcome-mix__legend .danger { background: var(--ra-red); }
.ra-outcome-mix__legend .success { background: var(--ra-green); }
.ra-outcome-mix__legend .warning { background: var(--ra-amber); }

div[data-testid="stExpander"] {
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.72);
}

.ra-pill {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 700;
  padding: 3px 9px;
  border: 1px solid transparent;
  white-space: nowrap;
}

.ra-pill--danger {
  color: var(--ra-red);
  background: var(--ra-red-bg);
  border-color: #fecdca;
}

.ra-pill--success {
  color: var(--ra-green);
  background: var(--ra-green-bg);
  border-color: #abefc6;
}

.ra-pill--warning {
  color: var(--ra-amber);
  background: var(--ra-amber-bg);
  border-color: #fedf89;
}

.ra-pill--neutral {
  color: #344054;
  background: #f2f4f7;
  border-color: #eaecf0;
}

.ra-branch-card {
  background: var(--ra-panel);
  border: 1px solid var(--ra-line);
  border-left: 5px solid #d0d5dd;
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 12px;
  min-height: 176px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.ra-branch-card--suspected_leakage { border-left-color: var(--ra-red); }
.ra-branch-card--explained_variance { border-left-color: var(--ra-green); }
.ra-branch-card--evidence_conflict { border-left-color: var(--ra-amber); }
.ra-branch-card--insufficient_data { border-left-color: #667085; }

.ra-branch-card__top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  color: var(--ra-ink);
}

.ra-branch-card__amount {
  color: var(--ra-ink);
  font-size: 1.35rem;
  font-weight: 800;
  margin-top: 8px;
}

.ra-branch-card__meta {
  color: var(--ra-muted);
  font-size: 0.82rem;
  margin-top: 2px;
}

.ra-branch-card__copy {
  color: var(--ra-muted);
  font-size: 0.86rem;
  line-height: 1.35;
  margin-top: 10px;
}

.ra-branch-card__action {
  display: inline-flex;
  color: var(--ra-ink);
  background: #f9fafb;
  border: 1px solid #eaecf0;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 900;
  padding: 4px 9px;
  margin-top: 12px;
}

.ra-detail-panel {
  background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.ra-detail-panel__header {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  align-items: flex-start;
  margin-bottom: 14px;
}

.ra-detail-panel__eyebrow {
  color: var(--ra-muted);
  font-size: 0.76rem;
  font-weight: 700;
  text-transform: uppercase;
}

.ra-detail-panel__title {
  color: var(--ra-ink);
  font-size: 1.25rem;
  font-weight: 800;
}

.ra-detail-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}

.ra-detail-grid div {
  background: var(--ra-soft);
  border-radius: 6px;
  padding: 10px;
}

.ra-detail-grid span {
  display: block;
  color: var(--ra-muted);
  font-size: 0.76rem;
  margin-bottom: 2px;
}

.ra-detail-grid strong {
  color: var(--ra-ink);
  font-size: 0.9rem;
}

.ra-detail-panel__summary {
  color: var(--ra-muted);
  font-size: 0.9rem;
  line-height: 1.4;
}

.ra-timeline {
  border-left: 2px solid #b8c7d4;
  margin-left: 13px;
  padding-left: 18px;
}

.ra-evidence-summary {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin: 4px 0 14px;
}

.ra-evidence-summary div {
  background: #ffffff;
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  padding: 11px 12px;
}

.ra-evidence-summary span {
  color: var(--ra-muted);
  display: block;
  font-size: 0.75rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.ra-evidence-summary strong {
  color: var(--ra-ink);
  display: block;
  font-size: 1rem;
  margin-top: 2px;
}

.ra-timeline-item {
  position: relative;
  margin-bottom: 14px;
}

.ra-timeline-item__index {
  position: absolute;
  left: -33px;
  top: 0;
  width: 26px;
  height: 26px;
  border-radius: 999px;
  background: var(--ra-navy);
  color: #ffffff;
  border: 2px solid #ffffff;
  box-shadow: 0 0 0 2px #b8c7d4;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.78rem;
  font-weight: 800;
}

.ra-timeline-item__body {
  background: var(--ra-panel);
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  padding: 12px 14px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.ra-timeline-item__type {
  color: var(--ra-muted);
  font-size: 0.76rem;
  font-weight: 800;
  text-transform: uppercase;
}

.ra-timeline-item__id {
  color: var(--ra-ink);
  font-weight: 800;
  margin-top: 2px;
}

.ra-timeline-item__excerpt {
  color: var(--ra-ink);
  font-size: 0.9rem;
  line-height: 1.35;
  margin-top: 6px;
}

.ra-timeline-item__source {
  display: inline-flex;
  gap: 6px;
  align-items: center;
  color: var(--ra-blue);
  background: var(--ra-blue-bg);
  border: 1px solid #c7d7fe;
  border-radius: 999px;
  padding: 3px 8px;
  font-size: 0.78rem;
  margin-top: 8px;
}

.ra-timeline-item__source span {
  color: #344054;
  font-weight: 800;
}

.ra-classification-panel {
  background: var(--ra-panel);
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 14px;
}

.ra-classification-panel__label {
  color: var(--ra-muted);
  font-size: 0.76rem;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 8px;
}

.ra-classification-panel__title {
  color: var(--ra-ink);
  font-size: 1.25rem;
  font-weight: 800;
  margin-top: 10px;
}

.ra-classification-panel__copy {
  color: var(--ra-muted);
  font-size: 0.9rem;
  line-height: 1.4;
  margin-top: 8px;
}

.ra-safety-panel {
  background: var(--ra-blue-bg);
  color: #1849a9;
  border: 1px solid #b2ddff;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 0.86rem;
  line-height: 1.35;
  margin-bottom: 12px;
}

div[data-testid="stButton"] button {
  width: 100%;
  border-radius: 7px;
  border: 1px solid #cdd7e1;
  font-weight: 800;
}

div[data-testid="stButton"] button:hover {
  border-color: var(--ra-blue);
  color: var(--ra-blue);
}

div[data-baseweb="select"] > div,
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
  border-radius: 7px;
  border-color: #cdd7e1;
  background: #ffffff;
}

div[data-testid="stTextInput"] label,
div[data-testid="stTextArea"] label,
div[data-testid="stSelectbox"] label {
  color: var(--ra-muted);
  font-size: 0.78rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

div[data-testid="stDataFrame"] {
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  overflow: hidden;
}

.ra-action-panel {
  background: #ffffff;
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  padding: 14px 16px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

.ra-action-panel__label {
  color: var(--ra-blue);
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.ra-action-panel__copy {
  color: var(--ra-ink);
  font-size: 0.93rem;
  line-height: 1.45;
}

.ra-case-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  background: var(--ra-panel);
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  padding: 12px 14px;
  margin-bottom: 8px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
  transition: transform 120ms ease, box-shadow 120ms ease, border-color 120ms ease;
}

.ra-case-row:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 24px rgba(16, 24, 40, 0.08);
}

.ra-case-row--suspected_leakage { border-left: 5px solid var(--ra-red); }
.ra-case-row--explained_variance { border-left: 5px solid var(--ra-green); }
.ra-case-row--evidence_conflict { border-left: 5px solid var(--ra-amber); }
.ra-case-row--insufficient_data { border-left: 5px solid #667085; }

.ra-case-row__customer {
  color: var(--ra-ink);
  font-weight: 800;
}

.ra-case-row__meta {
  color: var(--ra-muted);
  font-size: 0.78rem;
  margin-top: 2px;
}

.ra-case-row__side {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 6px;
}

.ra-case-row__amount {
  color: var(--ra-ink);
  font-weight: 800;
}
</style>
"""


def apply_theme() -> None:
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def render_hero(title: str, copy: str, eyebrow: str = "Revenue Assurance") -> None:
    st.markdown(
        f"""
        <div class="ra-hero">
          <div class="ra-hero__eyebrow">{eyebrow}</div>
          <div class="ra-hero__title">{title}</div>
          <div class="ra-hero__copy">{copy}</div>
          <div class="ra-hero__chips">
            <span>Q3 2026 review</span>
            <span>Offline synthetic fixtures</span>
            <span>Snowflake validation pending</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
