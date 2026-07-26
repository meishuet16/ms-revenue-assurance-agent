from __future__ import annotations

import streamlit as st


THEME_CSS = """
<style>
:root {
  --ra-ink: #172026;
  --ra-muted: #63717a;
  --ra-line: #d8e0e6;
  --ra-panel: #ffffff;
  --ra-soft: #f5f8fa;
  --ra-red: #b42318;
  --ra-red-bg: #fff1f0;
  --ra-green: #067647;
  --ra-green-bg: #ecfdf3;
  --ra-amber: #b54708;
  --ra-amber-bg: #fffaeb;
  --ra-blue: #175cd3;
  --ra-blue-bg: #eff8ff;
}

.block-container {
  padding-top: 1.4rem;
  padding-bottom: 2.5rem;
  max-width: 1180px;
}

h1, h2, h3 {
  color: var(--ra-ink);
  letter-spacing: 0;
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
  border-radius: 8px;
  padding: 14px 15px;
  min-height: 116px;
  box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
}

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
  border: 1px solid var(--ra-line);
  background: linear-gradient(180deg, #ffffff 0%, #f8fbfd 100%);
  border-radius: 8px;
  padding: 18px 20px;
  margin-bottom: 18px;
}

.ra-hero__eyebrow {
  color: var(--ra-blue);
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  margin-bottom: 6px;
}

.ra-hero__title {
  color: var(--ra-ink);
  font-size: 1.35rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.ra-hero__copy {
  color: var(--ra-muted);
  font-size: 0.96rem;
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
  border-radius: 8px;
  padding: 14px 16px;
  margin-bottom: 12px;
}

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
  background: var(--ra-panel);
  border: 1px solid var(--ra-line);
  border-radius: 8px;
  padding: 16px;
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
        </div>
        """,
        unsafe_allow_html=True,
    )
