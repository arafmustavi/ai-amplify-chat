"""Backend factory — the Strategy pattern entry point."""
from __future__ import annotations

from .base import BaseInferenceBackend
from .huggingface import HuggingFaceBackend
from .lm_studio import LMStudioBackend
from .termux import TermuxBackend

_REGISTRY: dict[str, type[BaseInferenceBackend]] = {
    "hf": HuggingFaceBackend,
    "lmstudio": LMStudioBackend,
    "termux": TermuxBackend,
}


def get_backend(name: str) -> BaseInferenceBackend:
    key = name.lower().strip()
    if key not in _REGISTRY:
        raise ValueError(f"Unknown backend '{name}'. Valid: {list(_REGISTRY)}")
    return _REGISTRY[key]()


__all__ = ["get_backend", "BaseInferenceBackend"]
