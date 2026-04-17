# CHANGE THIS:
# from mistralai.client import MistralClient 
# TO THIS:


import os
from langchain_mistralai import ChatMistralAI

from warehouse_ai_agent.interfaces.llm_interface import LLMInterface


class MistralProvider(LLMInterface):
    def __init__(self):
        # Uses MISTRAL_API_KEY from your .env automatically
        self.llm = ChatMistralAI(model="mistral-small-latest", temperature=0)

    def ask(self, system_prompt: str, user_prompt: str) -> str:
        messages = [("system", system_prompt), ("human", user_prompt)]
        return self.llm.invoke(messages).content

    def ask_structured(self, system_prompt: str, user_prompt: str, schema):
        # This is the LangChain 'Magic' for Pydantic objects
        structured_llm = self.llm.with_structured_output(schema)
        messages = [("system", system_prompt), ("human", user_prompt)]
        return structured_llm.invoke(messages)