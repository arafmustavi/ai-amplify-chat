"""Thread-safe CSV chat logger."""
from __future__ import annotations

import csv
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger(__name__)

_FIELDS = ["timestamp", "backend", "prompt", "response", "latency_ms"]


class ChatLogger:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        if not self.path.exists():
            with self.path.open("w", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(_FIELDS)
            log.info("Created chat log at %s", self.path)

    def log(self, *, prompt: str, response: str, latency_ms: float, backend: str) -> None:
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        row = [ts, backend, prompt, response, f"{latency_ms:.2f}"]
        with self._lock, self.path.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(row)

    def stats(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"total": 0, "avg_latency_ms": 0.0}
        total = 0
        latency_sum = 0.0
        with self.path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                total += 1
                try:
                    latency_sum += float(row["latency_ms"])
                except (KeyError, ValueError):
                    pass
        return {"total": total,
                "avg_latency_ms": round(latency_sum / total, 2) if total else 0.0}
