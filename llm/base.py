from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseLLM(ABC):
    """Abstract interface for text generation backends."""

    @abstractmethod
    def generate_text(self, prompt: str, **kwargs: Any) -> str:
        """Generate a text response for the given prompt."""

    def __call__(self, prompt: str, **kwargs: Any) -> str:
        return self.generate_text(prompt=prompt, **kwargs)
