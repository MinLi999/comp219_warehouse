import os
from .config_loader import Config

class LLMFactory:
    @staticmethod
    def get_provider():
        # Get provider from config (which reads from .env)
        provider_type = Config.LLM_PROVIDER.lower()
        
        if provider_type == "mistral":
            from ..providers.mistral_provider import MistralProvider
            return MistralProvider()
            
        elif provider_type == "ollama":
            from ..providers.ollama_provider import OllamaProvider
            return OllamaProvider()
            
        else:
            # This is where your error was triggered!
            raise ValueError(f"Provider {provider_type} not supported.")