"""Abstract inference backend."""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Tuple

log = logging.getLogger(__name__)


class BaseInferenceBackend(ABC):
    """Contract for any text-generation backend."""
    name: str = "base"

    def warmup(self) -> None:
        log.info("Backend '%s' ready (no warmup needed).", self.name)

    @abstractmethod
    def generate(self, prompt: str) -> Tuple[str, float]:
        """Return (response_text, latency_ms)."""
        raise NotImplementedError
