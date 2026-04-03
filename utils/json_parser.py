from __future__ import annotations

import json
import re
from json import JSONDecodeError
from typing import Any


FENCED_BLOCK_PATTERN = re.compile(
    r"```(?:json)?\s*(.*?)\s*```",
    re.DOTALL | re.IGNORECASE,
)


def clean_llm_text(text: str) -> str:
    """Remove common LLM formatting wrappers around JSON output."""
    cleaned = text.strip()

    fenced_match = FENCED_BLOCK_PATTERN.search(cleaned)
    if fenced_match:
        cleaned = fenced_match.group(1).strip()

    return cleaned


def extract_json_string(text: str) -> str:
    """Extract the first valid JSON object or array from text."""
    cleaned = clean_llm_text(text)

    for opener, closer in (("{", "}"), ("[", "]")):
        start = cleaned.find(opener)
        if start == -1:
            continue

        depth = 0
        in_string = False
        escape = False

        for index in range(start, len(cleaned)):
            char = cleaned[index]

            if in_string:
                if escape:
                    escape = False
                elif char == "\\":
                    escape = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
            elif char == opener:
                depth += 1
            elif char == closer:
                depth -= 1
                if depth == 0:
                    candidate = cleaned[start : index + 1]
                    json.loads(candidate)
                    return candidate

    raise ValueError("No valid JSON object or array found in the provided text.")


def parse_llm_json(text: str) -> Any:
    """Parse JSON content from raw LLM-generated text."""
    try:
        return json.loads(clean_llm_text(text))
    except JSONDecodeError:
        return json.loads(extract_json_string(text))
