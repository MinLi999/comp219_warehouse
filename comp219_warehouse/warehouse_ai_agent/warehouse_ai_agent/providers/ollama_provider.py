import requests
import json
from ..interfaces.i_provider import ILLMProvider

import requests
from ..interfaces.i_provider import ILLMProvider

class OllamaProvider(ILLMProvider):
    def __init__(self, model: str = "deepseek-r1:7b"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model

    def ask(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"<|system|>{system_prompt}<|user|>{user_prompt}<|assistant|>",
            "stream": False
        }
        try:
            response = requests.post(self.url, json=payload, timeout=180)
            return response.json().get("response", "Error: Empty response")
        except Exception as e:
            return f"Ollama Connection Error: {e}"