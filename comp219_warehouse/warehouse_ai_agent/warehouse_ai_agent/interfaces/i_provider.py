from abc import ABC, abstractmethod

class ILLMProvider(ABC):
    """
    Interface for the Strategy Pattern. 
    Ensures any LLM provider can be swapped into the Agents.
    """
    @abstractmethod
    def ask(self, system_prompt: str, user_input: str) -> str:
        """Sends a request to the LLM and returns the text response."""
        pass