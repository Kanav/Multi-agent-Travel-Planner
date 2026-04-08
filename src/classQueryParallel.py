from src.classificationResult import ClassificationResult
from src.llm import get_llm
from src.state import TravelPlannerState


def classify_query_parallel(state: TravelPlannerState) -> dict:
    """
    Updated router that can dispatch to MULTIPLE agents.
    """
    router_llm = get_llm()
    structured_llm = router_llm.with_structured_output(ClassificationResult)

    result = structured_llm.invoke([
        {
            "role": "system",
            "content": """
            You are a Travel Request Router that can dispatch to MULTIPLE agents in parallel.

            AVAILABLE AGENTS:
            1. search_agent_node - Flight searches, hotel searches, pricing, availability
            2. planner_agent_node - Itineraries, travel tips, weather, visas, activities, general guidance

            ROUTING RULES:

            SINGLE AGENT (requires_synthesis = false):
            - Flight/hotel ONLY → search_agent_node
            - Itinerary/planning ONLY → planner_agent_node
            - General travel questions → planner_agent_node

            MULTIPLE AGENTS (requires_synthesis = true):
            - "Plan a trip AND find flights/hotels" → BOTH agents
            - "Find hotels and create itinerary" → BOTH agents
            - Requests mentioning BOTH booking AND planning → BOTH agents

            When dispatching to BOTH agents:
            1. Create a focused sub-query for each agent
            2. search_agent_node query should focus on flights/hotels/pricing
            3. planner_agent_node query should focus on itinerary/activities/tips

            EXAMPLES:

            Query: "Find flights from DEL to DXB"
            → tasks: [{"source": "search_agent_node", "user_query": "Find flights from DEL to DXB"}]
            → requires_synthesis: false

            Query: "Plan a 5-day trip to Paris"
            → tasks: [{"source": "planner_agent_node", "user_query": "Plan a 5-day trip to Paris"}]
            → requires_synthesis: false

            Query: "Plan a week in London and find me hotels under $200/night"
            → tasks: [
                {"source": "search_agent_node", "user_query": "Find hotels in London under $200/night for 1 week", "focus": "hotel search and pricing"},
                {"source": "planner_agent_node", "user_query": "Plan a week-long itinerary for London", "focus": "daily activities and attractions"}
              ]
            → requires_synthesis: true

            Query: "I want to visit Tokyo - book flights from NYC and create a 5-day itinerary"
            → tasks: [
                {"source": "search_agent_node", "user_query": "Find flights from NYC to Tokyo", "focus": "flight options and prices"},
                {"source": "planner_agent_node", "user_query": "Create a 5-day itinerary for Tokyo", "focus": "daily schedule and activities"}
              ]
            → requires_synthesis: true
            """
        },
        {"role": "user", "content": state["user_query"]}
    ])

    return {
        "tasks": result.tasks,
        "requires_synthesis": result.requires_synthesis
    }
