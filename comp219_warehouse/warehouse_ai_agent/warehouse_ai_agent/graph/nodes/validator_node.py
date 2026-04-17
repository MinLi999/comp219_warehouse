from ...core.factory import LLMFactory
from ...agents.validator import ValidatorAgent
from .dispatch_node import p_mgr # Keep the shared PromptManager instance

# Instantiate the Validator Agent
llm_strategy = LLMFactory.get_provider()
validator_agent = ValidatorAgent(llm_strategy)

def validator_node(state):
    print("--- [NODE] VALIDATING MISSION SAFETY ---")
    
    location_name = state.get("location", "unknown")
    llm_coords = state.get("target_pose")
    
    # 1. Quick Check
    ground_truth = p_mgr.locations.get(location_name.lower())
    if not ground_truth:
        return {
            "final_decision": "ABORT", # Changed from nav_status
            "reasoning": f"Room '{location_name}' not in YAML map.",
            "target_pose": None
        }

    # 2. Delegate to Validator Agent
    try:
        audit = validator_agent.verify_safety(
            location_name=location_name,
            proposed_coords=llm_coords,
            ground_truth=ground_truth
        )
        
        print(f"--- CRITIC REASONING: {audit.reasoning} ---")

        # Use the specific keys expected by your main_agent_node
        if audit.is_safe:
            result = {
                "final_decision": "PROCEED", 
                "reasoning": audit.reasoning,
                "location_name": location_name,
                "coords": llm_coords 
            }
            print(f"DEBUG [validator_node]: Returning state update: {result}")
            return result
        else:
            return {
                "final_decision": "ABORT",
                "reasoning": audit.reasoning,
                "target_pose": None
            }
            
    except Exception as e:
        print(f"Validation Error: {e}")
        return {
            "final_decision": "ABORT",
            "reasoning": f"Validation Error: {e}", 
            "target_pose": None
        }