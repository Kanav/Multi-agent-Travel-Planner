from langgraph.graph import StateGraph, START, END
from src.classQueryParallel import classify_query_parallel
from src.conditionalEdges import should_continue_for_searchAgent, should_continue_for_plannerAgent
from src.dispatchToAgents import dispatch_to_agents
from src.plannerAgentNode import planner_agent_node
from src.plannerToolNode import planner_tool_node
from src.searchAgentNode import search_agent_node
from src.searchToolNode import search_tool_node
from src.state import TravelPlannerState
from src.synthesizer import synthesizer_node
from IPython.display import display, Image


def build_parallel_travel_agent():
    """Build the graph with parallel execution support."""

    builder = StateGraph(TravelPlannerState)
    builder.add_node("orchestrator", classify_query_parallel)
    builder.add_node("search_agent_node", search_agent_node)
    builder.add_node("planner_agent_node", planner_agent_node)
    builder.add_node("search_tool_node", search_tool_node)
    builder.add_node("planner_tool_node", planner_tool_node)
    builder.add_node("synthesizer", synthesizer_node)

    # Connect edges
    builder.add_edge(START, "orchestrator")

    # Router dispatches to agents via Send API (parallel execution)
    builder.add_conditional_edges(
        "orchestrator",
        dispatch_to_agents,
        ["search_agent_node", "planner_agent_node"] # dictionary
    )

    # Search agent tool loop
    builder.add_conditional_edges(
        "search_agent_node",
        should_continue_for_searchAgent,
        ["search_tool_node", "synthesizer"]  # Go to synthesizer instead of END
    )
    builder.add_edge("search_tool_node", "search_agent_node")

    # Planner agent tool loop
    builder.add_conditional_edges(
        "planner_agent_node",
        should_continue_for_plannerAgent,
        ["planner_tool_node", "synthesizer"]  # Go to synthesizer instead of END
    )
    builder.add_edge("planner_tool_node", "planner_agent_node")

    # End after synthesis
    builder.add_edge("synthesizer", END)

    return builder.compile()

if __name__ == "__main__":
    agent = build_parallel_travel_agent()
    # Generate the PNG data
    png_data = agent.get_graph().draw_mermaid_png()

    # Save it to a file
    with open("graph.png", "wb") as f:
        f.write(png_data)

    # Optionally display it in a notebook
    display(Image(filename="graph.png"))