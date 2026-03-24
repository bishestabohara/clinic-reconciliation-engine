from __future__ import annotations

import logging
from typing import Any

from openai import OpenAI

from app.core.config import get_openai_api_key, get_openai_model
from app.services.cache_service import cache

logger = logging.getLogger(__name__)


def _extract_output_text(response: Any) -> str:
    output_text = getattr(response, "output_text", "")
    if output_text:
        return output_text.strip()
    return ""


def _generate_with_openai(system_prompt: str, user_prompt: str) -> str | None:
    api_key = get_openai_api_key()
    if not api_key:
        return None

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=get_openai_model(),
            input=[
                {
                    "role": "system",
                    "content": [{"type": "input_text", "text": system_prompt}],
                },
                {
                    "role": "user",
                    "content": [{"type": "input_text", "text": user_prompt}],
                },
            ],
        )
        return _extract_output_text(response) or None
    except Exception as exc:  # noqa: BLE001
        logger.warning("LLM reasoning fallback triggered: %s", exc)
        return None


def generate_reconciliation_reasoning(payload: dict[str, Any], fallback_reasoning: str) -> str:
    cached = cache.get({"type": "reconciliation", "payload": payload})
    if cached:
        return cached

    system_prompt = (
        "You are assisting with clinical medication reconciliation. "
        "Base your answer only on the provided data, do not invent facts, "
        "and keep the explanation concise and clinician-friendly."
    )
    user_prompt = (
        "Review the following reconciliation payload and produce 2 to 3 sentences "
        "explaining the most likely active medication, why it was chosen, and any "
        f"safety nuance.\n\nPayload:\n{payload}"
    )
    reasoning = _generate_with_openai(system_prompt, user_prompt) or fallback_reasoning
    return cache.set({"type": "reconciliation", "payload": payload}, reasoning)


def generate_quality_summary(payload: dict[str, Any], issue_count: int) -> str:
    cached = cache.get({"type": "quality", "payload": payload})
    if cached:
        return cached

    system_prompt = (
        "You review patient record data quality. Summarize the issues clearly, without "
        "inventing missing context."
    )
    user_prompt = (
        f"Summarize the quality risks in this patient payload. There are {issue_count} known "
        f"issues.\n\nPayload:\n{payload}"
    )
    summary = _generate_with_openai(system_prompt, user_prompt) or (
        f"Detected {issue_count} data quality issue(s). Review the flagged fields before "
        "using this record for clinical decision support."
    )
    return cache.set({"type": "quality", "payload": payload}, summary)
