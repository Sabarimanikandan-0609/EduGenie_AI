import json
import re
from functools import lru_cache

from .config import get_settings


class GeminiConfigurationError(RuntimeError):
    """Raised when Gemini cannot be configured."""


@lru_cache
def get_client():
    from google import genai

    settings = get_settings()

    if not settings.gemini_api_key:
        raise GeminiConfigurationError(
            "GEMINI_API_KEY is not configured. "
            "Add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=settings.gemini_api_key)


def generate_text(
    prompt: str,
    *,
    temperature: float = 0.4,
    max_output_tokens: int = 1200,
) -> str:

    settings = get_settings()

    from google.genai import types

    client = get_client()

    response = client.models.generate_content(
        model=settings.gemini_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )

    text = getattr(response, "text", None)

    if not text:
        raise RuntimeError("Gemini returned an empty response.")

    return text.strip()


def extract_json(text: str):
    """
    Convert Gemini JSON output into a Python object.

    Handles:
    - normal JSON
    - JSON inside ```json ... ```
    - JSON surrounded by extra text
    """

    cleaned = text.strip()

    # Remove markdown code fences.
    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError:
        # Try to find the first JSON array/object.
        start_candidates = [
            position
            for position in (
                cleaned.find("["),
                cleaned.find("{"),
            )
            if position >= 0
        ]

        if not start_candidates:
            raise

        start = min(start_candidates)

        end = max(
            cleaned.rfind("]"),
            cleaned.rfind("}"),
        )

        if end <= start:
            raise

        return json.loads(
            cleaned[start:end + 1]
        )