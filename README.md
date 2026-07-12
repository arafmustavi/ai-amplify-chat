<div align="center">

# ⚡ AMPLIFY

**A local-first Small Language Model chat platform with a pluggable inference backend and a private analytics plane.**

[![CI](https://github.com/arafmustavi/amplify/actions/workflows/ci.yml/badge.svg)](https://github.com/arafmustavi/amplify/actions)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-compose-blue?logo=docker)](docker-compose.yml)

*Runs 100% offline · Deployable in 2 commands · Portfolio-ready*

</div>

---

## ✨ Why AMPLIFY

Most "local LLM" projects lock you into one inference stack. AMPLIFY treats the
inference engine as a **plug-in**: switch from HuggingFace Transformers to
LM Studio to on-device Termux/llama.cpp by changing **one environment variable**.

- 🧠 **Pluggable backends** — HF · LM Studio · Termux (llama.cpp)
- 🔒 **Local-first** — no data leaves your box
- 📊 **Private analytics** — Streamlit dashboard, password-gated
- 🐳 **One-command deploy** — `docker compose up`
- 🏠 **Homelab-ready** — designed to run on an 8 GB laptop / mini-PC

---

## 🏗️ Architecture

```
                    ┌─────────────────────────────────────┐
                    │            nginx :80                │
                    │   /  → app   /analytics → dashboard │
                    └───────┬────────────────────┬────────┘
                            │                    │
                 ┌──────────▼───────┐   ┌────────▼─────────┐
                 │  Flask app :5000 │   │ Streamlit :8501  │
                 │  ┌────────────┐  │   │  Plotly charts   │
                 │  │ Strategy:  │  │   └────────┬─────────┘
                 │  │  hf │ lm  │  │            │
                 │  │  studio   │  │            │
                 │  │  termux   │  │            │
                 │  └────────────┘  │            │
                 └───────┬──────────┘            │
                         │                       │
                         ▼                       ▼
                ┌────────────────────────────────────────┐
                │  ./data/amplify_chat_history.csv       │
                └────────────────────────────────────────┘
```

See [`docs/architecture.md`](docs/architecture.md) for the sequence diagram.

---

## 🔌 Backend matrix

| Backend      | Env value      | Best for                       | Deps |
|--------------|----------------|--------------------------------|------|
| HuggingFace  | `hf`           | Fully local, offline homelab   | `requirements-hf.txt` (torch) |
| LM Studio    | `lmstudio`     | Desktop GPU users              | requests only |
| Termux       | `termux`       | On-device Android inference    | requests only |

---

## 🚀 Quickstart

```bash
cp .env.example .env
docker compose up -d --build
```

Then open:
- Chat UI → <http://localhost/>
- Analytics → <http://localhost/analytics/> (basic auth)

Local dev (no Docker):

```bash
make install
make run          # chat on :5000
make dashboard    # analytics on :8501
```

---

## 🧪 Tests & Quality

```bash
make test    # pytest + coverage
make lint    # ruff + black --check
make format  # auto-fix
```

CI runs on every PR: Ruff, Black, Pytest with coverage, and a Docker build check.

---

## 📜 License

MIT © 2026 [Araf Mustavi](https://www.linkedin.com/in/arafmustavi/)
