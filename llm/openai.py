from __future__ import annotations

from copy import deepcopy
from typing import Any

from llm.base import BaseLLM

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover - depends on local environment
    OpenAI = None
    OPENAI_IMPORT_ERROR = exc
else:
    OPENAI_IMPORT_ERROR = None


class OpenAILLM(BaseLLM):
    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> None:
        if OpenAI is None:
            raise ImportError(
                "The 'openai' package is required to use OpenAILLM."
            ) from OPENAI_IMPORT_ERROR

        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI(api_key=api_key)

    @staticmethod
    def _supports_temperature(model: str) -> bool:
        normalized_model = model.lower()
        unsupported_prefixes = (
            "gpt-5",
            "o1",
            "o3",
            "o4",
        )
        return not normalized_model.startswith(unsupported_prefixes)

    @staticmethod
    def _extract_output_text(response: Any) -> str:
        output_text = getattr(response, "output_text", None)
        if output_text:
            return output_text

        collected_text: list[str] = []

        for output_item in getattr(response, "output", []) or []:
            if getattr(output_item, "type", None) != "message":
                continue

            for content_item in getattr(output_item, "content", []) or []:
                content_type = getattr(content_item, "type", None)
                if content_type == "output_text":
                    text = getattr(content_item, "text", None)
                    if text:
                        collected_text.append(text)
                elif content_type == "refusal":
                    refusal = getattr(content_item, "refusal", None)
                    if refusal:
                        collected_text.append(refusal)

        if collected_text:
            return "\n".join(collected_text).strip()

        raise ValueError("OpenAI response did not contain any text output.")

    @staticmethod
    def _get_incomplete_reason(response: Any) -> str | None:
        incomplete_details = getattr(response, "incomplete_details", None)
        if incomplete_details is None:
            return None
        return getattr(incomplete_details, "reason", None)

    @classmethod
    def _prepare_json_schema(cls, schema: dict[str, Any]) -> dict[str, Any]:
        prepared_schema = deepcopy(schema)
        cls._close_object_schemas(prepared_schema)
        return prepared_schema

    @classmethod
    def _close_object_schemas(cls, node: Any) -> None:
        if isinstance(node, dict):
            if node.get("type") == "object" or "properties" in node:
                node["additionalProperties"] = False

            for value in node.values():
                cls._close_object_schemas(value)
        elif isinstance(node, list):
            for item in node:
                cls._close_object_schemas(item)

    def generate_text(self, prompt: str, **kwargs: Any) -> str:
        model = kwargs.get("model", self.model)
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        json_schema = kwargs.get("json_schema")
        retry_max_tokens = kwargs.get(
            "retry_max_tokens",
            max(max_tokens * 4, 12000),
        )
        current_max_tokens = max_tokens

        while True:
            request_kwargs = {
                "model": model,
                "input": prompt,
                "max_output_tokens": current_max_tokens,
            }

            if json_schema:
                request_kwargs["text"] = {
                    "format": {
                        "type": "json_schema",
                        "name": kwargs.get("schema_name", "structured_output"),
                        "schema": self._prepare_json_schema(json_schema),
                        "strict": kwargs.get("strict_json_schema", True),
                    }
                }

            if self._supports_temperature(model):
                request_kwargs["temperature"] = kwargs.get(
                    "temperature",
                    self.temperature,
                )

            response = self.client.responses.create(**request_kwargs)
            incomplete_reason = self._get_incomplete_reason(response)

            if incomplete_reason == "max_output_tokens":
                next_max_tokens = min(current_max_tokens * 2, retry_max_tokens)
                if next_max_tokens > current_max_tokens:
                    current_max_tokens = next_max_tokens
                    continue

                raise ValueError(
                    "OpenAI response was truncated because max_output_tokens was too low."
                )

            if incomplete_reason:
                raise ValueError(
                    f"OpenAI response was incomplete: {incomplete_reason}."
                )

            return self._extract_output_text(response)
