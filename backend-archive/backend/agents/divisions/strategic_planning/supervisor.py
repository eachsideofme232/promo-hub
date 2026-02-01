"""Strategic Planning Division Supervisor."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool

from backend.agents.base import BaseAgent, BaseDivisionSupervisor, agent_registry
from backend.agents.divisions.strategic_planning.budget_allocator import BudgetAllocator
from backend.agents.divisions.strategic_planning.promotion_planner import PromotionPlanner
from backend.agents.divisions.strategic_planning.timeline_manager import TimelineManager
from backend.graph.routing import classify_task
from backend.graph.state import Division, PromotorStateDict, TaskType


class StrategicPlanningSupervisor(BaseDivisionSupervisor):
    """
    Strategic Planning Division Supervisor.

    Coordinates:
    - PromotionPlanner: Promotion calendars and strategies
    - TimelineManager: Deadlines and milestones
    - BudgetAllocator: Budget distribution and ROI
    """

    name = "strategic_planning_supervisor"
    role = "Strategic Planning Division Head"
    description = "Coordinates promotion planning, timelines, and budgets"
    division = Division.STRATEGIC_PLANNING

    def __init__(
        self,
        llm: BaseChatModel,
        agents: dict[str, BaseAgent] | None = None,
        tools: Sequence[BaseTool] | None = None,
    ):
        super().__init__(llm, agents, tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Strategic Planning Division Supervisor for Promotor.

Your division handles:
1. Promotion Planning - calendars, campaigns, strategies
2. Timeline Management - deadlines, milestones, scheduling
3. Budget Allocation - distribution, ROI projection, tracking

Your agents:
- promotion_planner: Creates promotion calendars and campaign strategies
- timeline_manager: Tracks deadlines and manages milestones
- budget_allocator: Distributes budgets and projects ROI

Route requests to the appropriate agent:
- Planning/calendar/campaign questions → promotion_planner
- Deadline/schedule/timeline questions → timeline_manager
- Budget/cost/ROI questions → budget_allocator
- Complex requests may need multiple agents

When coordinating:
- Consider dependencies between planning, timeline, and budget
- Ensure timeline aligns with budget cycles
- Verify budgets support planned promotions

Respond in Korean if the user's query is in Korean."""

    async def route_to_agent(
        self,
        state: PromotorStateDict,
    ) -> str:
        """Determine which agent should handle the request."""
        messages = state.get("messages", [])
        if not messages:
            return self.name

        last_message = messages[-1]
        query = (
            last_message.content
            if hasattr(last_message, "content")
            else str(last_message)
        ).lower()

        # Route based on keywords
        if any(kw in query for kw in ["calendar", "plan", "campaign", "promotion", "캘린더", "계획", "캠페인"]):
            return "promotion_planner"
        elif any(kw in query for kw in ["deadline", "timeline", "schedule", "milestone", "마감", "일정"]):
            return "timeline_manager"
        elif any(kw in query for kw in ["budget", "cost", "roi", "spend", "예산", "비용"]):
            return "budget_allocator"

        # Default to promotion planner for general strategic queries
        return "promotion_planner"

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a request through the Strategic Planning division."""
        # Route to appropriate agent
        agent_name = await self.route_to_agent(state)

        agent = self.get_agent(agent_name)
        if agent:
            result = await agent.process(state, messages)
        else:
            result = await super().process(state, messages)

        return {
            "division": self.division.value,
            "supervisor": self.name,
            "routed_to": agent_name,
            "result": result,
            "summary": result.get("content", "Strategic planning request processed."),
        }


def create_strategic_planning_division(
    llm: BaseChatModel,
) -> StrategicPlanningSupervisor:
    """
    Factory function to create the Strategic Planning division.

    Args:
        llm: Language model to use

    Returns:
        Configured StrategicPlanningSupervisor with all agents
    """
    # Create agents
    promotion_planner = PromotionPlanner(llm)
    timeline_manager = TimelineManager(llm)
    budget_allocator = BudgetAllocator(llm)

    # Create supervisor with agents
    supervisor = StrategicPlanningSupervisor(
        llm,
        agents={
            "promotion_planner": promotion_planner,
            "timeline_manager": timeline_manager,
            "budget_allocator": budget_allocator,
        },
    )

    # Register all agents
    agent_registry.register_agent(promotion_planner)
    agent_registry.register_agent(timeline_manager)
    agent_registry.register_agent(budget_allocator)
    agent_registry.register_supervisor(Division.STRATEGIC_PLANNING, supervisor)

    return supervisor
