import os
from dotenv import load_dotenv

# Load once at the start of the application
load_dotenv()

class Config:
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mistral")
    
    @staticmethod
    def validate():
        if not Config.MISTRAL_API_KEY:
            raise ValueError("MISTRAL_API_KEY not found in environment variables!")