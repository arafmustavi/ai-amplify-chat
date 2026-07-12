# Changelog

## [0.2.0] — 2026-07-12
### Changed
- 🏗️ Major refactor from flat `app_*.py` scripts to a single `app.py` + `amplify/` package.
- Introduced the **Strategy pattern** via `BaseInferenceBackend`.
- Backends selected at runtime through `AMPLIFY_BACKEND` env var.

### Added
- Pydantic-settings driven configuration.
- Streamlit analytics dashboard (`dashboard.py`).
- Docker Compose stack (app + dashboard + nginx).
- CI workflow (ruff, black, pytest, docker build).
- Test suite with mock backend.

## [0.1.0] — Initial prototype
- Flask chat with HF Transformers.
- Separate scripts for LM Studio and Termux.
