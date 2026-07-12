"""Chat, health, and metrics routes."""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from flask import Blueprint, jsonify, render_template, request

from amplify import __version__
from amplify.backends.base import BaseInferenceBackend
from amplify.services.logger import ChatLogger
from amplify.services.sanitizer import sanitize_for_model, sanitize_for_log

log = logging.getLogger(__name__)


def build_chat_blueprint(*, backend: BaseInferenceBackend, chat_logger: ChatLogger) -> Blueprint:
    bp = Blueprint("chat", __name__)

    @bp.get("/")
    def index():
        return render_template("index.html", backend=backend.name, version=__version__)

    @bp.get("/health")
    def health():
        return jsonify(status="ok", backend=backend.name, version=__version__,
                       time=datetime.now(timezone.utc).isoformat())

    @bp.get("/metrics")
    def metrics():
        return jsonify(backend=backend.name, **chat_logger.stats())

    @bp.post("/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        raw_prompt = str(payload.get("message", "")).strip()
        if not raw_prompt:
            return jsonify(error="Message cannot be empty."), 400

        prompt = sanitize_for_model(raw_prompt)
        try:
            response, latency_ms = backend.generate(prompt)
        except Exception as e:
            log.exception("Backend generation failed")
            return jsonify(error=str(e)), 500

        chat_logger.log(
            prompt=sanitize_for_log(prompt),
            response=sanitize_for_log(response),
            latency_ms=latency_ms,
            backend=backend.name,
        )
        return jsonify(response=response, latency_ms=round(latency_ms, 2),
                       backend=backend.name)

    return bp
