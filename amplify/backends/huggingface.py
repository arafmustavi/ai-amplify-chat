"""HuggingFace Transformers backend."""
from __future__ import annotations

import logging
from typing import Tuple

from amplify.config import settings
from amplify.utils.latency import LatencyTimer
from .base import BaseInferenceBackend

log = logging.getLogger(__name__)


class HuggingFaceBackend(BaseInferenceBackend):
    name = "hf"

    def __init__(self) -> None:
        self._tokenizer = None
        self._model = None

    def warmup(self) -> None:
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer  # type: ignore
        except ImportError as e:
            raise RuntimeError(
                "transformers not installed. Run: pip install -r requirements-hf.txt"
            ) from e

        log.info("Loading model '%s' ...", settings.MODEL_ID)
        self._tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_ID)
        self._model = AutoModelForCausalLM.from_pretrained(settings.MODEL_ID)
        log.info("Model loaded.")

    def generate(self, prompt: str) -> Tuple[str, float]:
        if self._model is None or self._tokenizer is None:
            self.warmup()
        assert self._tokenizer is not None and self._model is not None

        with LatencyTimer() as t:
            inputs = self._tokenizer(prompt, return_tensors="pt")
            outputs = self._model.generate(
                **inputs,
                max_new_tokens=settings.MAX_NEW_TOKENS,
                temperature=settings.TEMPERATURE,
                do_sample=True,
                pad_token_id=self._tokenizer.eos_token_id,
            )
            text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
            if text.startswith(prompt):
                text = text[len(prompt):].lstrip()

        return text.strip(), t.elapsed_ms
