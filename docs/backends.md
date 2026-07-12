# Adding a new backend

1. Create `amplify/backends/<name>.py` with a class extending `BaseInferenceBackend`.
2. Implement `generate(self, prompt: str) -> tuple[str, float]`.
3. Register it in `amplify/backends/__init__.py::_REGISTRY`.
4. Add any new settings to `amplify/config.py`.
5. Add tests in `tests/test_backends.py`.

## Contract

- Inputs come pre-sanitised — do not re-strip.
- Always return latency in **milliseconds** (use `LatencyTimer`).
- Raise `RuntimeError` with a user-friendly message on failure.
