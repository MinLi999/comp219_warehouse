import re

from warehouse_ai_agent.core.schemas import ClassificationSchema
from ..state import AgentState
from ...agents.classifier import ClassifierAgent
from ...core.factory import LLMFactory

# Logic for instantiating the specific strategy
llm_strategy = LLMFactory.get_provider() 
classifier_agent = ClassifierAgent(llm_strategy)

def classification_node(state):
    # 'flush=True' is CRITICAL when running inside ros2 launch
    print("--- [NODE] CLASSIFYING INTENT ---", flush=True) 
    
    try:
        # This is a network call. It will take 1-2 seconds.
        result = classifier_agent.classify(state["user_input"])
        
        print(f"--- INTENT DETECTED: {result.intent} ---", flush=True)
        return {"intent": result.intent}
    except Exception as e:
        print(f"!!! CLASSIFIER ERROR: {e} !!!", flush=True)
        return {"intent": "info"}