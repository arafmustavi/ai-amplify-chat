"""LM Studio backend — OpenAI-compatible local server."""
from __future__ import annotations

import logging
from typing import Tuple

import requests

from amplify.config import settings
from amplify.utils.latency import LatencyTimer
from .base import BaseInferenceBackend

log = logging.getLogger(__name__)


class LMStudioBackend(BaseInferenceBackend):
    name = "lmstudio"
    timeout_seconds: int = 120

    def generate(self, prompt: str) -> Tuple[str, float]:
        payload = {
            "model": settings.MODEL_ID,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": settings.TEMPERATURE,
            "max_tokens": settings.MAX_NEW_TOKENS,
        }
        with LatencyTimer() as t:
            try:
                r = requests.post(settings.LM_STUDIO_URL, json=payload,
                                  timeout=self.timeout_seconds)
                r.raise_for_status()
                text = r.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                log.exception("LM Studio call failed")
                raise RuntimeError(f"LM Studio backend error: {e}") from e
        return text, t.elapsed_ms
