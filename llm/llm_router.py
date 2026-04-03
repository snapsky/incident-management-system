from __future__ import annotations

from typing import Any

from llm.base import BaseLLM


class LLMRouter(BaseLLM):
    """Routes text generation requests to a selected provider."""

    def __init__(self, llms: dict[str, BaseLLM], default_provider: str) -> None:
        if not llms:
            raise ValueError("At least one LLM implementation must be provided.")
        if default_provider not in llms:
            raise ValueError(
                f"Default provider '{default_provider}' is not available in the router."
            )

        self.llms = llms
        self.default_provider = default_provider

    def get_llm(self, provider: str | None = None) -> BaseLLM:
        selected_provider = provider or self.default_provider
        try:
            return self.llms[selected_provider]
        except KeyError as exc:
            available = ", ".join(sorted(self.llms))
            raise ValueError(
                f"Unknown LLM provider '{selected_provider}'. Available providers: {available}"
            ) from exc

    def generate_text(self, prompt: str, **kwargs: Any) -> str:
        provider = kwargs.pop("provider", None)
        llm = self.get_llm(provider=provider)
        return llm.generate_text(prompt=prompt, **kwargs)
