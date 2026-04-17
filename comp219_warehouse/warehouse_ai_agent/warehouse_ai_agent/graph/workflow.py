from langgraph.graph import StateGraph, END
from .state import AgentState
from warehouse_ai_agent.graph.nodes.classification_node import classification_node
from warehouse_ai_agent.graph.nodes.dispatch_node import dispatch_node
from .nodes.validator_node import validator_node # Import the Critic
import base64
import requests

def create_hospital_graph():
    workflow = StateGraph(AgentState)

    # 1. Add all nodes
    workflow.add_node("classify", classification_node)
    workflow.add_node("dispatch", dispatch_node)
    workflow.add_node("validate", validator_node) # New Critic Node

    # 2. Define flow starting point
    workflow.set_entry_point("classify")

    # 3. Define Conditional Logic
    workflow.add_conditional_edges(
        "classify",
        lambda x: x["intent"],
        {
            "nav": "dispatch",
            "info": END,        
            "off_topic": END    
        }
    )

    # 4. Reroute flow: dispatch -> validate -> END
    workflow.add_edge("dispatch", "validate")
    workflow.add_edge("validate", END)

    app = workflow.compile()

    # --- VISUALIZATION BLOCK ---
    try:
        mermaid_str = app.get_graph().draw_mermaid()
        print("\n--- MERMAID GRAPH DEFINITION ---")
        print(mermaid_str)
        
        graphbytes = mermaid_str.encode("utf-8")
        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")
        
        url = f"https://mermaid.ink/img/{base64_string}"
        response = requests.get(url)
        
        if response.status_code == 200:
            with open("hospital_graph.png", "wb") as f:
                f.write(response.content)
            print("Success: Graph saved as 'hospital_graph.png'")
        else:
            print(f"API Error: {response.status_code}")

    except Exception as e:
        print(f"Could not generate visual graph: {e}")
    
    return app