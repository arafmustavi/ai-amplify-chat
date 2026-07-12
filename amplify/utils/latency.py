"""High-resolution latency timer."""
from __future__ import annotations

import time
from types import TracebackType
from typing import Optional, Type


class LatencyTimer:
    def __init__(self) -> None:
        self._start: float = 0.0
        self.elapsed_ms: float = 0.0

    def __enter__(self) -> "LatencyTimer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc: Optional[BaseException], tb: Optional[TracebackType]) -> None:
        self.elapsed_ms = (time.perf_counter() - self._start) * 1000.0
