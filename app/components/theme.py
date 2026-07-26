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
  border-left: 2px solid var(--ra-line);
  margin-left: 13px;
  padding-left: 18px;
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
  background: var(--ra-blue-bg);
  color: var(--ra-blue);
  border: 1px solid #b2ddff;
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
  color: var(--ra-muted);
  font-size: 0.78rem;
  margin-top: 8px;
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
}

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
