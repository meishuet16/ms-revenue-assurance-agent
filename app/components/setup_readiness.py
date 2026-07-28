from __future__ import annotations

import html
import os
from collections.abc import Mapping

import streamlit as st

from app.config import Settings, settings
from scripts.validate_environment import missing_environment_variables


def readiness_items(active_settings: Settings, env: Mapping[str, str] = os.environ) -> list[tuple[str, str, str]]:
    missing = missing_environment_variables(env)
    env_status = "Ready" if not missing else f"Missing {len(missing)}"
    mode_status = "Live requested" if active_settings.live_dashboard_requested else "Fixture mode"
    auth_status = "Configured" if active_settings.has_snowflake_credentials else "Pending"
    return [
        ("Dashboard mode", mode_status, "fixture is safest until live validation passes"),
        ("Snowflake env", env_status, "run validate_environment.py for redacted details"),
        ("Authentication", auth_status, "password or external browser auth"),
    ]


def next_command(active_settings: Settings) -> str:
    if not active_settings.has_snowflake_credentials:
        return "python scripts\\validate_environment.py"
    if active_settings.live_dashboard_requested:
        return "python scripts\\verify_database.py"
    return "python scripts\\setup_project.py --warehouse COMPUTE_WH"


def build_setup_readiness_html(active_settings: Settings = settings, env: Mapping[str, str] = os.environ) -> str:
    cards = []
    for label, value, detail in readiness_items(active_settings, env):
        cards.append(
            '<div class="ra-readiness-card">'
            f'<div class="ra-readiness-card__label">{html.escape(label)}</div>'
            f'<strong>{html.escape(value)}</strong>'
            f'<span>{html.escape(detail)}</span>'
            "</div>"
        )
    command = html.escape(next_command(active_settings))
    return (
        '<div class="ra-readiness">'
        '<div class="ra-readiness__head">'
        '<div><div class="ra-readiness__eyebrow">Setup readiness</div>'
        '<div class="ra-readiness__title">Live demo controls</div></div>'
        f'<code>{command}</code>'
        "</div>"
        f'<div class="ra-readiness__grid">{"".join(cards)}</div>'
        "</div>"
    )


def render_setup_readiness() -> None:
    st.markdown(build_setup_readiness_html(), unsafe_allow_html=True)
