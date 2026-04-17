from ..core.schemas import DispatchSchema
from ..utils.prompt_manager import PromptManager

class DispatcherAgent:
    def __init__(self, llm_strategy, prompt_manager: PromptManager):
        self.llm = llm_strategy
        self.prompt_manager = prompt_manager

    def get_coordinates(self, user_request: str) -> DispatchSchema:
        # Get the standard prompt (which already contains your map coordinates)
        system_prompt = self.prompt_manager.get_dispatcher_prompt()
        
        # LangChain handles the JSON extraction and Pydantic validation automatically
        return self.llm.ask_structured(
            system_prompt=system_prompt,
            user_prompt=user_request,
            schema=DispatchSchema
        )