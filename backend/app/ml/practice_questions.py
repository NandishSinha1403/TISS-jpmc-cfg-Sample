"""LLM-generated practice questions from module content.

Isolated per the project's ML/LLM convention (never imported directly by
routers — go through app/services/practice_question_service.py). Uses the
OpenAI SDK pointed at OpenRouter's OpenAI-compatible endpoint, since
OpenRouter itself is not a distinct SDK — this is the standard pattern for
any OpenAI-API-compatible provider.
"""

import json

from openai import APIError, APITimeoutError, OpenAI, RateLimitError

from app.core.config import settings

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


class PracticeQuestionGenerationError(Exception):
    """Raised on any failure to generate questions — API down, rate limited,
    misconfigured key, or a malformed/unparseable model response. Callers
    should catch this and degrade gracefully, never let it surface as a
    raw 500."""


def _client() -> OpenAI:
    if not settings.openrouter_api_key:
        raise PracticeQuestionGenerationError("OPENROUTER_API_KEY is not configured")
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=settings.openrouter_api_key)


def _build_prompt(module_title: str, module_content: str, count: int) -> str:
    return f"""You are writing practice quiz questions for an adult learner completing a workplace-skills training module.

Module title: {module_title}
Module content:
\"\"\"
{module_content}
\"\"\"

Write exactly {count} multiple-choice practice questions based ONLY on the content above. Each question must have exactly 4 options, exactly one of which is correct. Questions should test understanding of the material, not trivia or wording tricks.

Respond with ONLY a JSON array (no markdown fences, no commentary), where each item has this exact shape:
{{"text": "question text", "options": ["option A", "option B", "option C", "option D"], "correct_index": 0}}

correct_index is the 0-based index of the correct option in the options array."""


def _parse_questions(raw_content: str, expected_count: int) -> list[dict]:
    text = raw_content.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as e:
        raise PracticeQuestionGenerationError(f"Model returned unparseable JSON: {e}") from e

    if not isinstance(parsed, list) or not parsed:
        raise PracticeQuestionGenerationError("Model response was not a non-empty JSON array")

    questions = []
    for item in parsed:
        if (
            not isinstance(item, dict)
            or not isinstance(item.get("text"), str)
            or not item["text"].strip()
            or not isinstance(item.get("options"), list)
            or len(item["options"]) < 2
            or not all(isinstance(o, str) for o in item["options"])
            or not isinstance(item.get("correct_index"), int)
            or not (0 <= item["correct_index"] < len(item["options"]))
        ):
            raise PracticeQuestionGenerationError("Model response contained a malformed question")
        questions.append(
            {"text": item["text"].strip(), "options": item["options"], "correct_index": item["correct_index"]}
        )

    return questions[:expected_count]


def generate_practice_questions(module_title: str, module_content: str, count: int) -> list[dict]:
    if not module_content.strip():
        raise PracticeQuestionGenerationError("Module has no content to generate questions from")

    client = _client()
    try:
        response = client.chat.completions.create(
            model=settings.openrouter_model,
            messages=[{"role": "user", "content": _build_prompt(module_title, module_content, count)}],
            temperature=0.7,
            timeout=20.0,
        )
    except RateLimitError as e:
        raise PracticeQuestionGenerationError("Rate limited by the LLM provider") from e
    except APITimeoutError as e:
        raise PracticeQuestionGenerationError("LLM provider timed out") from e
    except APIError as e:
        raise PracticeQuestionGenerationError(f"LLM provider error: {e}") from e

    content = response.choices[0].message.content if response.choices else None
    if not content:
        raise PracticeQuestionGenerationError("LLM provider returned an empty response")

    return _parse_questions(content, count)
