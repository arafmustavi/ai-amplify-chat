"""Centralised, type-safe configuration."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BackendName = Literal["hf", "lmstudio", "termux"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8",
        env_prefix="AMPLIFY_", extra="ignore",
    )

    BACKEND: BackendName = Field(default="hf")
    HOST: str = "0.0.0.0"
    PORT: int = 5000
    DEBUG: bool = False

    MODEL_ID: str = "Rta-AILabs/Nandi-Mini-150M-Instruct"
    MAX_NEW_TOKENS: int = 256
    TEMPERATURE: float = 0.7

    LM_STUDIO_URL: str = "http://host.docker.internal:1234/v1/chat/completions"
    TERMUX_URL: str = "http://127.0.0.1:8080/v1/chat/completions"

    LOG_PATH: Path = Path("data/amplify_chat_history.csv")
    DASHBOARD_PASSWORD: str = "changeme"


settings = Settings()
