"""Prompt / response sanitisation helpers."""
from __future__ import annotations

import re

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_MAX_PROMPT = 4000
_MAX_LOG_FIELD = 2000


def sanitize_for_model(text: str) -> str:
    cleaned = _CONTROL_CHARS.sub("", text or "").strip()
    return cleaned[:_MAX_PROMPT]


def sanitize_for_log(text: str) -> str:
    cleaned = (text or "").replace("\r", " ").replace("\n", " ")
    cleaned = _CONTROL_CHARS.sub("", cleaned).strip()
    return cleaned[:_MAX_LOG_FIELD]
