"""HTTP Basic Auth helper."""
from __future__ import annotations

from functools import wraps
from flask import Response, request

from amplify.config import settings


def _check(user: str, pwd: str) -> bool:
    return user == "admin" and pwd == settings.DASHBOARD_PASSWORD


def _challenge() -> Response:
    return Response("Auth required.", 401,
                    {"WWW-Authenticate": 'Basic realm="AMPLIFY Analytics"'})


def requires_basic_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not _check(auth.username or "", auth.password or ""):
            return _challenge()
        return fn(*args, **kwargs)
    return wrapper
