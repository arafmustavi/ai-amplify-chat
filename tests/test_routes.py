"""Flask route tests using a mock backend."""
from __future__ import annotations

from typing import Tuple
from pathlib import Path

import pytest
from flask import Flask

from amplify.backends.base import BaseInferenceBackend
from amplify.routes.chat import build_chat_blueprint
from amplify.services.logger import ChatLogger


class _MockBackend(BaseInferenceBackend):
    name = "mock"
    def generate(self, prompt: str) -> Tuple[str, float]:
        return f"echo: {prompt}", 12.34


@pytest.fixture()
def client(tmp_path: Path):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    logger = ChatLogger(tmp_path / "log.csv")
    app.register_blueprint(build_chat_blueprint(backend=_MockBackend(), chat_logger=logger))
    with app.test_client() as c:
        yield c


def test_health(client) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_chat_ok(client) -> None:
    r = client.post("/chat", json={"message": "hello"})
    assert r.status_code == 200
    body = r.get_json()
    assert "echo: hello" in body["response"]
    assert body["backend"] == "mock"


def test_chat_empty(client) -> None:
    r = client.post("/chat", json={"message": ""})
    assert r.status_code == 400
