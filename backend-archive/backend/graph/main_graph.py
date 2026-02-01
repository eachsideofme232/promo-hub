"""Main LangGraph setup for Promotor multi-agent orchestration."""

from __future__ import annotations

from typing import Any, Literal

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.state import CompiledStateGraph

from backend.graph.routing import (
    classify_task,
    determine_divisions,
    determine_model_tier,
)
from backend.graph.state import Division, PromotorStateDict, TaskType


def create_chief_coordinator_node():
    """Create the chief coordinator node that routes to divisions."""

    async def chief_coordinator(state: PromotorStateDict) -> PromotorStateDict:
        """
        Main supervisor that analyzes requests and routes to appropriate divisions.
        """
        messages = state.get("messages", [])
        if not messages:
            return {**state, "error": "No messages to process"}

        # Get the last user message
        last_message = messages[-1]
        query = (
            last_message.content
            if hasattr(last_message, "content")
            else str(last_message)
        )

        # Classify the task
        task_type = classify_task(query)

        # Determine which divisions should handle this
        divisions = determine_divisions(query, task_type)

        # Determine model tier for cost optimization
        model_tier = determine_model_tier(task_type, query)
        use_mini_model = model_tier == "tier2_cheap"

        # Generate cache key for potential caching
        cache_key = f"{state.get('brand_id', 'default')}:{task_type.value}:{hash(query)}"

        return {
            **state,
            "task_type": task_type.value,
            "next_divisions": [d.value for d in divisions] if divisions else [],
            "use_mini_model": use_mini_model,
            "cache_key": cache_key,
            "current_division": None,
            "current_agent": "chief_coordinator",
        }

    return chief_coordinator


def create_response_aggregator_node():
    """Create the response aggregator that combines results from all divisions."""

    async def response_aggregator(state: PromotorStateDict) -> PromotorStateDict:
        """
        Aggregate results from all divisions into a coherent response.
        """
        division_results = state.get("division_results", {})
        task_type = state.get("task_type", TaskType.GENERAL_QUERY.value)

        # Build aggregated response
        response_parts = []

        if not division_results:
            response_parts.append(
                "I've processed your request but no specific division results were generated."
            )
        else:
            for division_name, result in division_results.items():
                if isinstance(result, dict):
                    summary = result.get("summary", str(result))
                else:
                    summary = str(result)
                response_parts.append(f"**{division_name.replace('_', ' ').title()}**: {summary}")

        # Create aggregated message
        aggregated_response = "\n\n".join(response_parts)

        return {
            **state,
            "messages": [AIMessage(content=aggregated_response)],
            "current_agent": "response_aggregator",
        }

    return response_aggregator


def create_error_handler_node():
    """Create the error handler node."""

    async def error_handler(state: PromotorStateDict) -> PromotorStateDict:
        """Handle errors gracefully."""
        error = state.get("error", "Unknown error occurred")
        retry_count = state.get("retry_count", 0)

        # Could implement retry logic here
        error_message = f"An error occurred while processing your request: {error}"

        return {
            **state,
            "messages": [AIMessage(content=error_message)],
            "current_agent": "error_handler",
        }

    return error_handler


def create_division_supervisor_node(division: Division):
    """Create a supervisor node for a specific division."""

    async def division_supervisor(state: PromotorStateDict) -> PromotorStateDict:
        """
        Division supervisor that coordinates agents within the division.
        This is a placeholder that will be replaced by actual division implementations.
        """
        division_name = division.value

        # Update state to mark this division as being processed
        result = {
            "division": division_name,
            "status": "processed",
            "summary": f"{division_name.replace('_', ' ').title()} division has processed the request.",
        }

        # Add result to division results
        current_results = state.get("division_results", {})
        updated_results = {**current_results, division_name: result}

        # Add this division to completed list
        completed = list(state.get("completed_divisions", []))
        if division_name not in completed:
            completed.append(division_name)

        return {
            **state,
            "current_division": division_name,
            "division_results": updated_results,
            "completed_divisions": completed,
        }

    return division_supervisor


def route_from_coordinator(
    state: PromotorStateDict,
) -> Literal[
    "strategic_planning_supervisor",
    "market_intelligence_supervisor",
    "channel_management_supervisor",
    "analytics_supervisor",
    "operations_supervisor",
    "response_aggregator",
    "error_handler",
]:
    """Route from chief coordinator to appropriate division(s)."""
    error = state.get("error")
    if error:
        return "error_handler"

    next_divisions = state.get("next_divisions", [])
    if not next_divisions:
        return "response_aggregator"

    # For now, route to first division (will be expanded for parallel execution)
    first_division = next_divisions[0]
    return f"{first_division}_supervisor"


def route_from_division(
    state: PromotorStateDict,
) -> Literal[
    "strategic_planning_supervisor",
    "market_intelligence_supervisor",
    "channel_management_supervisor",
    "analytics_supervisor",
    "operations_supervisor",
    "response_aggregator",
]:
    """Route from a division to next division or aggregator."""
    next_divisions = state.get("next_divisions", [])
    completed = state.get("completed_divisions", [])

    # Find pending divisions
    pending = [d for d in next_divisions if d not in completed]

    if not pending:
        return "response_aggregator"

    # Route to next pending division
    return f"{pending[0]}_supervisor"


def create_main_graph() -> CompiledStateGraph:
    """
    Create the main LangGraph for Promotor.

    Graph Structure:
    - Entry: chief_coordinator
    - Divisions: strategic_planning, market_intelligence, channel_management,
                 analytics, operations (each with supervisor)
    - Exit: response_aggregator

    Returns:
        Compiled LangGraph ready for execution
    """
    # Create the graph
    graph = StateGraph(PromotorStateDict)

    # Add nodes
    graph.add_node("chief_coordinator", create_chief_coordinator_node())
    graph.add_node("response_aggregator", create_response_aggregator_node())
    graph.add_node("error_handler", create_error_handler_node())

    # Add division supervisor nodes
    for division in Division:
        node_name = f"{division.value}_supervisor"
        graph.add_node(node_name, create_division_supervisor_node(division))

    # Set entry point
    graph.set_entry_point("chief_coordinator")

    # Add conditional edges from chief coordinator
    graph.add_conditional_edges(
        "chief_coordinator",
        route_from_coordinator,
        {
            "strategic_planning_supervisor": "strategic_planning_supervisor",
            "market_intelligence_supervisor": "market_intelligence_supervisor",
            "channel_management_supervisor": "channel_management_supervisor",
            "analytics_supervisor": "analytics_supervisor",
            "operations_supervisor": "operations_supervisor",
            "response_aggregator": "response_aggregator",
            "error_handler": "error_handler",
        },
    )

    # Add edges from each division to router
    for division in Division:
        node_name = f"{division.value}_supervisor"
        graph.add_conditional_edges(
            node_name,
            route_from_division,
            {
                "strategic_planning_supervisor": "strategic_planning_supervisor",
                "market_intelligence_supervisor": "market_intelligence_supervisor",
                "channel_management_supervisor": "channel_management_supervisor",
                "analytics_supervisor": "analytics_supervisor",
                "operations_supervisor": "operations_supervisor",
                "response_aggregator": "response_aggregator",
            },
        )

    # Add edges to END
    graph.add_edge("response_aggregator", END)
    graph.add_edge("error_handler", END)

    # Compile and return
    return graph.compile()


# Convenience function for running the graph
async def process_request(
    query: str,
    user_id: str = "default_user",
    brand_id: str = "default_brand",
    active_channels: list[str] | None = None,
) -> dict[str, Any]:
    """
    Process a user request through the Promotor system.

    Args:
        query: User's request
        user_id: User identifier
        brand_id: Brand identifier
        active_channels: List of active channels

    Returns:
        Final state after processing
    """
    from backend.graph.state import create_initial_state

    # Create initial state
    initial_state = create_initial_state(
        user_id=user_id,
        brand_id=brand_id,
        active_channels=active_channels,
    )

    # Add user message
    initial_state["messages"] = [HumanMessage(content=query)]

    # Create and run graph
    graph = create_main_graph()
    result = await graph.ainvoke(initial_state)

    return result
