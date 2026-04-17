from abc import ABC, abstractmethod
from typing import Any, Type

class LLMInterface(ABC):
    @abstractmethod
    def ask(self, system_prompt: str, user_prompt: str) -> str:
        """Standard text-in, text-out method."""
        pass

    @abstractmethod
    def ask_structured(self, system_prompt: str, user_prompt: str, schema: Type[Any]) -> Any:
        """Method to return a Pydantic object based on a schema."""
        pass