"""Operations Division Supervisor."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool

from backend.agents.base import BaseAgent, BaseDivisionSupervisor, agent_registry
from backend.agents.divisions.operations.checklist_manager import ChecklistManager
from backend.agents.divisions.operations.inventory_checker import InventoryChecker
from backend.agents.divisions.operations.price_monitor import PriceMonitor
from backend.graph.state import Division, PromotorStateDict


class OperationsSupervisor(BaseDivisionSupervisor):
    """
    Operations Division Supervisor.

    Coordinates:
    - InventoryChecker: Real-time inventory monitoring
    - PriceMonitor: Price compliance and MAP violations
    - ChecklistManager: Pre-launch validation
    """

    name = "operations_supervisor"
    role = "Operations Division Head"
    description = "Coordinates inventory, pricing, and compliance operations"
    division = Division.OPERATIONS

    def __init__(
        self,
        llm: BaseChatModel,
        agents: dict[str, BaseAgent] | None = None,
        tools: Sequence[BaseTool] | None = None,
    ):
        super().__init__(llm, agents, tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Operations Division Supervisor for Promotor.

Your division handles:
1. Inventory Monitoring - Real-time stock levels and alerts
2. Price Monitoring - MAP compliance and violation detection
3. Checklist Management - Pre-launch validation and compliance

Your agents:
- inventory_checker: Monitors inventory levels and generates alerts
- price_monitor: Scans for MAP violations and unauthorized sellers
- checklist_manager: Manages pre-launch checklists and compliance

Route requests appropriately:
- Stock/inventory questions → inventory_checker
- Price violations/MAP/resellers → price_monitor
- Checklist/compliance/launch readiness → checklist_manager

Operational priorities:
1. Prevent stockouts (revenue protection)
2. Maintain price integrity (brand protection)
3. Ensure launch readiness (execution quality)

When coordinating:
- Connect inventory alerts with promotion planning
- Link price violations with channel management
- Integrate compliance checks with launch timelines

Alert escalation:
- Critical: Immediate attention, blocks operations
- Warning: Plan action within 48 hours
- Info: Monitor and document

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
        if any(kw in query for kw in ["inventory", "stock", "재고", "품절", "물량"]):
            return "inventory_checker"
        elif any(kw in query for kw in ["price", "map", "violation", "reseller", "가격", "위반"]):
            return "price_monitor"
        elif any(kw in query for kw in ["checklist", "compliance", "launch", "체크리스트", "검증", "런칭"]):
            return "checklist_manager"

        # Default to inventory checker for general operations
        return "inventory_checker"

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a request through the Operations division."""
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
            "summary": result.get("content", "Operations request processed."),
        }


def create_operations_division(
    llm: BaseChatModel,
) -> OperationsSupervisor:
    """
    Factory function to create the Operations division.

    Args:
        llm: Language model to use

    Returns:
        Configured OperationsSupervisor with all agents
    """
    # Create agents
    inventory_checker = InventoryChecker(llm)
    price_monitor = PriceMonitor(llm)
    checklist_manager = ChecklistManager(llm)

    # Create supervisor with agents
    supervisor = OperationsSupervisor(
        llm,
        agents={
            "inventory_checker": inventory_checker,
            "price_monitor": price_monitor,
            "checklist_manager": checklist_manager,
        },
    )

    # Register all agents
    agent_registry.register_agent(inventory_checker)
    agent_registry.register_agent(price_monitor)
    agent_registry.register_agent(checklist_manager)
    agent_registry.register_supervisor(Division.OPERATIONS, supervisor)

    return supervisor
