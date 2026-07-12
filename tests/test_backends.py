"""Backend factory + base contract tests."""
from __future__ import annotations

import pytest

from amplify.backends import get_backend
from amplify.backends.base import BaseInferenceBackend


def test_base_is_abstract() -> None:
    with pytest.raises(TypeError):
        BaseInferenceBackend()  # type: ignore[abstract]


def test_factory_unknown() -> None:
    with pytest.raises(ValueError):
        get_backend("does-not-exist")


@pytest.mark.parametrize("name", ["lmstudio", "termux"])
def test_factory_returns_instance(name: str) -> None:
    b = get_backend(name)
    assert isinstance(b, BaseInferenceBackend)
    assert b.name == name
