from __future__ import annotations

import os


def get_api_key() -> str:
    return os.getenv("API_KEY", "dev-api-key")


def get_openai_api_key() -> str | None:
    return os.getenv("OPENAI_API_KEY")


def get_openai_model() -> str:
    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
