from warehouse_ai_agent.core.factory import LLMFactory
from warehouse_ai_agent.utils.prompt_manager import PromptManager
from warehouse_ai_agent.agents.dispatcher import DispatcherAgent

# Injection
# Ensure warehouse_ai_agent/utils/prompt_manager.py has package_name = 'warehouse_ai_agent'
llm_strategy = LLMFactory.get_provider()
p_mgr = PromptManager() 
dispatcher = DispatcherAgent(llm_strategy, p_mgr)

def dispatch_node(state):
    print("--- [NODE] DISPATCHING TO COORDINATES ---", flush=True)
    
    try:
        # The Agent returns a 'DispatchSchema' instance
        data = dispatcher.get_coordinates(state["user_input"])
        
        print(f"--- TARGET IDENTIFIED: {data.location} at {data.coords} ---", flush=True)
        
        return {
            "location": data.location,
            "target_pose": data.coords, 
            "nav_status": f"Goal: {data.location}",
            "intent": "nav"
        }
        
    except Exception as e:
        print(f"Dispatcher Error: {e}", flush=True)
        return {"nav_status": f"Dispatch Failed: {e}", "target_pose": None}