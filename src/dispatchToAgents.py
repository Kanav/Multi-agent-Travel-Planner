from src.state import TravelPlannerState
from langgraph.types import Send

def dispatch_to_agents(state: TravelPlannerState):
    """
    Uses Send API to dispatch tasks to agents in PARALLEL.
    This is the key function that enables concurrent execution.
    """
    tasks = state.get("tasks", [])

    sends = []
    for task in tasks:

        worker_state = {
            "messages": state.get("messages", []),
            "user_query": task.user_query,
            "tasks": state.get("tasks", []),
            "requires_synthesis": state.get("requires_synthesis", False),
            "agent_results": [],  # Each worker starts fresh
            "final_answer": "",
            "search_messages": [],  # Initialize empty for workers
            "planner_messages": [],  # Initialize empty for workers
        }

        if task.source == "search_agent_node":
            sends.append(Send("search_agent_node", worker_state))  # Your existing node
        elif task.source == "planner_agent_node":
            sends.append(Send("planner_agent_node", worker_state))  # Your existing node

    return sends