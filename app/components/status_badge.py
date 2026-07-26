from __future__ import annotations

from app.components.formatting import format_status, status_tone


def status_badge(status: str) -> str:
    tone = status_tone(status)
    label = format_status(status)
    return f'<span class="ra-pill ra-pill--{tone}">{label}</span>'


def confidence_badge(confidence: str) -> str:
    tone = "warning" if confidence == "needs_investigation" else "neutral"
    label = confidence.replace("_", " ").title()
    return f'<span class="ra-pill ra-pill--{tone}">{label}</span>'
