from typing import TypedDict, Annotated, List, Union

class AgentState(TypedDict):
    user_input: str
    intent: str
    location: str
    target_pose: List[float]
    nav_status: str
    history: List[str]
    # ADD THESE THREE KEYS:
    final_decision: str  
    coords: List[float]
    reasoning: str