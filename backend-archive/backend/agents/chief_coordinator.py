"""Chief Coordinator - Main supervisor agent that routes requests to divisions."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.tools import BaseTool

from backend.agents.base import BaseAgent, BaseDivisionSupervisor, agent_registry
from backend.graph.routing import (
    classify_task,
    determine_divisions,
    determine_model_tier,
    get_agent_for_task,
)
from backend.graph.state import Division, PromotorStateDict, TaskType


class ChiefCoordinator(BaseAgent):
    """
    Chief Coordinator - The main supervisor agent.

    Responsibilities:
    - Analyze incoming requests
    - Classify task types
    - Route to appropriate division(s)
    - Coordinate multi-division workflows
    - Aggregate final responses
    """

    name = "chief_coordinator"
    role = "Chief Coordinator"
    description = "Main supervisor that orchestrates all divisions and agents"
    division = None  # Chief coordinator is above divisions

    def __init__(
        self,
        llm: BaseChatModel,
        mini_llm: BaseChatModel | None = None,
        tools: Sequence[BaseTool] | None = None,
    ):
        """
        Initialize the Chief Coordinator.

        Args:
            llm: Main language model (for complex tasks)
            mini_llm: Smaller model for classification (cost optimization)
            tools: Tools available to the coordinator
        """
        super().__init__(llm, tools)
        self.mini_llm = mini_llm or llm

    @property
    def system_prompt(self) -> str:
        return """You are the Chief Coordinator of Promotor, a Bloomberg Terminal-style promotion management system for beauty brands.

Your role is to:
1. Understand user requests about beauty brand promotions
2. Route requests to the appropriate division(s)
3. Coordinate multi-division workflows
4. Synthesize responses from multiple divisions

Available Divisions:
- Strategic Planning: Promotion calendars, timelines, budgets
- Market Intelligence: Industry news, competitor analysis, trends
- Channel Management: Oliveyoung, Coupang, Naver, Kakao channels
- Analytics: Sentiment, performance, margins, forecasts
- Operations: Inventory, price monitoring, checklists

When responding:
- Be concise and professional (Bloomberg terminal style)
- Use data-driven language
- Highlight key metrics and insights
- Format information clearly

For Korean users, respond in Korean when the query is in Korean."""

    async def analyze_request(
        self,
        query: str,
        state: PromotorStateDict,
    ) -> dict[str, Any]:
        """
        Analyze a user request and determine routing.

        Args:
            query: User's input query
            state: Current state

        Returns:
            Analysis results including task type and target divisions
        """
        # Classify the task
        task_type = classify_task(query)

        # Determine divisions
        divisions = determine_divisions(query, task_type)

        # Determine model tier
        model_tier = determine_model_tier(task_type, query)

        # Generate cache key
        brand_id = state.get("brand_id", "default")
        cache_key = f"{brand_id}:{task_type.value}:{hash(query)}"

        return {
            "task_type": task_type,
            "divisions": divisions,
            "model_tier": model_tier,
            "use_mini_model": model_tier == "tier2_cheap",
            "cache_key": cache_key,
            "is_multi_division": len(divisions) > 1,
        }

    async def route_request(
        self,
        state: PromotorStateDict,
    ) -> PromotorStateDict:
        """
        Route a request to appropriate division(s).

        Args:
            state: Current graph state

        Returns:
            Updated state with routing information
        """
        messages = state.get("messages", [])
        if not messages:
            return {
                **state,
                "error": "No messages to process",
            }

        # Get the query
        last_message = messages[-1]
        query = (
            last_message.content
            if hasattr(last_message, "content")
            else str(last_message)
        )

        # Analyze the request
        analysis = await self.analyze_request(query, state)

        # Update state with routing information
        return {
            **state,
            "task_type": analysis["task_type"].value,
            "next_divisions": [d.value for d in analysis["divisions"]],
            "use_mini_model": analysis["use_mini_model"],
            "cache_key": analysis["cache_key"],
            "current_agent": self.name,
        }

    async def aggregate_responses(
        self,
        state: PromotorStateDict,
    ) -> PromotorStateDict:
        """
        Aggregate responses from all divisions.

        Args:
            state: State with division results

        Returns:
            State with aggregated response
        """
        division_results = state.get("division_results", {})
        task_type = state.get("task_type", TaskType.GENERAL_QUERY.value)

        if not division_results:
            response = "Request processed. No specific division results to aggregate."
        else:
            # Build structured response
            sections = []

            for division_name, result in division_results.items():
                title = division_name.replace("_", " ").title()

                if isinstance(result, dict):
                    content = result.get("summary") or result.get("content") or str(result)
                else:
                    content = str(result)

                sections.append(f"## {title}\n{content}")

            response = "\n\n".join(sections)

            # Add summary if multiple divisions
            if len(division_results) > 1:
                response = f"**Multi-Division Analysis Complete**\n\n{response}"

        return {
            **state,
            "messages": [AIMessage(content=response)],
            "current_agent": self.name,
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """
        Process a request through the Chief Coordinator.

        This is the main entry point for handling user requests.

        Args:
            state: Current graph state
            messages: Optional additional messages

        Returns:
            Processing results
        """
        # Route the request
        routed_state = await self.route_request(state)

        # If there's an error, return early
        if routed_state.get("error"):
            return {
                "error": routed_state["error"],
                "agent_name": self.name,
            }

        return {
            "agent_name": self.name,
            "task_type": routed_state.get("task_type"),
            "divisions": routed_state.get("next_divisions", []),
            "routed": True,
        }


def create_chief_coordinator(
    llm: BaseChatModel,
    mini_llm: BaseChatModel | None = None,
) -> ChiefCoordinator:
    """
    Factory function to create and register the Chief Coordinator.

    Args:
        llm: Main language model
        mini_llm: Optional smaller model for cost optimization

    Returns:
        Configured ChiefCoordinator instance
    """
    coordinator = ChiefCoordinator(llm, mini_llm)
    agent_registry.register_agent(coordinator)
    return coordinator
