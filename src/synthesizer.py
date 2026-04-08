from langchain_core.messages import AIMessage, HumanMessage

from src.llm import get_llm
from src.state import TravelPlannerState


def synthesizer_node(state: TravelPlannerState) -> dict:
    """
    Combines results from parallel agents into a unified response.
    Only called when requires_synthesis is True.
    """

    agent_results = state.get("agent_results", [])

    if not agent_results:
        return {
            "final_answer": "I couldn't process your request.",
            "messages": [AIMessage(content="I couldn't process your request.")]
        }

    # If only one result, no synthesis needed
    if len(agent_results) == 1:
        result = agent_results[0]["result"]
        return {
            "final_answer": result,
            "messages": [AIMessage(content=result)]
        }

    # Format results for synthesis
    results_formatted = "\n\n" + "="*50 + "\n\n".join([
        f"**{r['agent'].upper()}**\nFocus: {r.get('focus', 'N/A')}\n\n{r['result']}"
        for r in agent_results
    ])

    #     ==================================================
    # **SEARCH_AGENT**
    # Focus: hotels
    # Top hotels in Madrid...

    # **PLANNER_AGENT**
    # Focus: 3 day itinerary
    # Day 1: Prado museum...

    synthesis_prompt = """
    You are a Travel Response Synthesizer. Combine multiple agent outputs into a single, well-organized, comprehensive response.

    RULES:
    1. Organize logically (e.g., Flights → Hotels → Itinerary → Tips)
    2. Don't repeat information
    3. Highlight key recommendations
    4. Note any conflicts or alternatives
    5. Create clear sections with headers
    6. End with actionable next steps

    Original Query: {query}

    Agent Results:
    {results}

    Create a unified, helpful response:
    """

    response = get_llm().invoke([
        HumanMessage(content=synthesis_prompt.format(
            query=state["user_query"],
            results=results_formatted
        ))
    ])

    return {
        "final_answer": response.content,
        "messages": [AIMessage(content=response.content)]
    }