from __future__ import annotations

from llm.gemini import GeminiLLM
from llm.llm_router import LLMRouter
from llm.openai import OpenAILLM


def build_llm(config: dict) -> LLMRouter:
    llm_config = config.get("llm")
    if not llm_config:
        raise ValueError("Missing 'llm' configuration.")

    default_provider = llm_config.get("default_provider")
    if not default_provider:
        raise ValueError("Missing 'llm.default_provider' configuration.")

    providers = llm_config.get("providers")
    if not providers:
        raise ValueError("Missing 'llm.providers' configuration.")

    llms = {}

    for provider_name, provider_config in providers.items():
        api_key = provider_config.get("api_key")
        model = provider_config.get("model")
        temperature = provider_config.get("temperature", 0.7)
        max_tokens = provider_config.get("max_tokens", 512)

        if not api_key:
            raise ValueError(f"Missing 'api_key' for LLM provider '{provider_name}'.")
        if not model:
            raise ValueError(f"Missing 'model' for LLM provider '{provider_name}'.")

        if provider_name == "openai":
            llms[provider_name] = OpenAILLM(
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        elif provider_name == "gemini":
            llms[provider_name] = GeminiLLM(
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        else:
            raise ValueError(f"Unsupported LLM provider '{provider_name}'.")

    return LLMRouter(llms=llms, default_provider=default_provider)
