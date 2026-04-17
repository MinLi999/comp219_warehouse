from warehouse_ai_agent.core.schemas import ClassificationSchema
from ..interfaces.i_provider import ILLMProvider

class ClassifierAgent:
    def __init__(self, llm: ILLMProvider):
        self.llm = llm
        self.system_prompt = """
        You are a triage assistant for a hospital robot. 
        Categorize the user's input into one of three labels:
        1. 'nav': If the user wants the robot to move or deliver something.
        2. 'info': If the user is asking a question about the hospital.
        3. 'off_topic': For everything else (greetings, jokes, etc.).
        Respond ONLY with the label name.
        """

    def classify(self, user_input: str) -> ClassificationSchema:
        # Use the structured method from our new LangChainMistralProvider
        return self.llm.ask_structured(
            system_prompt=self.system_prompt,
            user_prompt=user_input,
            schema=ClassificationSchema
        )