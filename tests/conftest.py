"""Shared pytest fixtures."""
from __future__ import annotations

import tempfile
from pathlib import Path

import pytest


@pytest.fixture()
def tmp_log_path(monkeypatch: pytest.MonkeyPatch) -> Path:
    tmp = Path(tempfile.mkdtemp()) / "chat.csv"
    monkeypatch.setenv("AMPLIFY_LOG_PATH", str(tmp))
    return tmp
