"""AMPLIFY — single entry point.

Chooses the inference backend at runtime via the AMPLIFY_BACKEND env variable
and wires up Flask blueprints. This file stays thin: config → backend → routes.
"""
from __future__ import annotations

import logging
from flask import Flask

from amplify import __version__
from amplify.config import settings
from amplify.backends import get_backend
from amplify.routes.chat import build_chat_blueprint
from amplify.services.logger import ChatLogger


logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
log = logging.getLogger("amplify.app")


def create_app() -> Flask:
    """Application factory."""
    log.info("Booting AMPLIFY v%s (backend=%s)", __version__, settings.BACKEND)

    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["JSON_SORT_KEYS"] = False

    backend = get_backend(settings.BACKEND)
    backend.warmup()

    chat_logger = ChatLogger(settings.LOG_PATH)

    app.register_blueprint(build_chat_blueprint(backend=backend, chat_logger=chat_logger))
    return app


app = create_app()


if __name__ == "__main__":
    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
