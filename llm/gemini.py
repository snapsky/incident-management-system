from __future__ import annotations

from typing import Any

from llm.base import BaseLLM

try:
    from google import genai
    from google.genai import types
except ImportError as exc:  # pragma: no cover - depends on local environment
    genai = None
    types = None
    GEMINI_IMPORT_ERROR = exc
else:
    GEMINI_IMPORT_ERROR = None


class GeminiLLM(BaseLLM):
    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> None:
        if genai is None:
            raise ImportError(
                "The 'google-generativeai' package is required to use GeminiLLM."
            ) from GEMINI_IMPORT_ERROR

        self.model_name = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = genai.Client(api_key=api_key)

    def generate_text(self, prompt: str, **kwargs: Any) -> str:
        response = self.client.models.generate_content(
            model=kwargs.get("model", self.model_name),
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=kwargs.get("temperature", self.temperature),
                max_output_tokens=kwargs.get("max_tokens", self.max_tokens),
            ),
        )
        return response.text
