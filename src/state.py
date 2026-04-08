from typing import TypedDict, Annotated, List, Optional
import operator
from pydantic import BaseModel, Field
from langchain.messages import AnyMessage
from typing import TypedDict, Literal, Annotated

class AgentTask(BaseModel):
    """A single agent task with targeted query."""
    source: Literal["search_agent_node", "planner_agent_node"]
    user_query: str
    focus: str = ""  # What aspect this agent should focus on


##### Main Graph State ######

# TypedDict - defines a structural type for dictionaries with a fixed set of string keys and specific value types,
# enabling static type checking for JSON-like structures
# no runtime validation like Pydantic (used in tools)

class TravelPlannerState(TypedDict):
    """Enhanced state for parallel execution."""

    # Conversation history
    messages: Annotated[List[AnyMessage], operator.add]

    # Current user query
    user_query: str

    # Tasks from router (replaces single classification)
    tasks: List[AgentTask]

    # Flag for synthesis
    requires_synthesis: bool

    # Parallel agent results - KEY: uses operator.add for concurrent writes
    agent_results: Annotated[List[dict], operator.add]

    # Final synthesized answer
    final_answer: str

    search_messages: Annotated[List[AnyMessage], operator.add]
    planner_messages: Annotated[List[AnyMessage], operator.add]