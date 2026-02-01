"""Base classes for Promotor agents."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import BaseTool

from backend.graph.state import Division, PromotorStateDict


class BaseAgent(ABC):
    """
    Base class for all Promotor agents.

    Each agent has:
    - A name and role description
    - Access to specific tools
    - A system prompt defining behavior
    - Methods to process requests
    """

    name: str
    role: str
    description: str
    division: Division

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        """
        Initialize the agent.

        Args:
            llm: Language model to use
            tools: List of tools available to this agent
        """
        self.llm = llm
        self.tools = list(tools) if tools else []

        # Bind tools to LLM if available
        if self.tools:
            self.llm_with_tools = self.llm.bind_tools(self.tools)
        else:
            self.llm_with_tools = self.llm

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass

    def get_system_message(self) -> SystemMessage:
        """Get the system message for this agent."""
        return SystemMessage(content=self.system_prompt)

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """
        Process a request and return results.

        Args:
            state: Current graph state
            messages: Optional additional messages

        Returns:
            Dictionary with agent's response and any updates to state
        """
        # Build messages for LLM
        llm_messages = [self.get_system_message()]

        # Add conversation history
        if state.get("messages"):
            llm_messages.extend(state["messages"])

        # Add any additional messages
        if messages:
            llm_messages.extend(messages)

        # Invoke LLM
        response = await self.llm_with_tools.ainvoke(llm_messages)

        return {
            "agent_name": self.name,
            "response": response,
            "content": response.content if hasattr(response, "content") else str(response),
        }

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name}, role={self.role})>"


class BaseDivisionSupervisor(BaseAgent):
    """
    Base class for division supervisors.

    Supervisors coordinate agents within their division,
    deciding which agent(s) should handle specific tasks.
    """

    agents: dict[str, BaseAgent]

    def __init__(
        self,
        llm: BaseChatModel,
        agents: dict[str, BaseAgent] | None = None,
        tools: Sequence[BaseTool] | None = None,
    ):
        """
        Initialize the division supervisor.

        Args:
            llm: Language model to use
            agents: Dictionary of agents in this division
            tools: Additional tools for the supervisor
        """
        super().__init__(llm, tools)
        self.agents = agents or {}

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent with this supervisor."""
        self.agents[agent.name] = agent

    def get_agent(self, name: str) -> BaseAgent | None:
        """Get an agent by name."""
        return self.agents.get(name)

    @abstractmethod
    async def route_to_agent(
        self,
        state: PromotorStateDict,
    ) -> str:
        """
        Determine which agent should handle the request.

        Args:
            state: Current graph state

        Returns:
            Name of the agent to route to
        """
        pass

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """
        Process request by routing to appropriate agent.

        Args:
            state: Current graph state
            messages: Optional additional messages

        Returns:
            Results from the handling agent
        """
        # Determine which agent should handle this
        agent_name = await self.route_to_agent(state)

        agent = self.get_agent(agent_name)
        if not agent:
            # Fallback to supervisor handling
            return await super().process(state, messages)

        # Delegate to the agent
        result = await agent.process(state, messages)

        return {
            "division": self.division.value,
            "routed_to": agent_name,
            **result,
        }


class AgentRegistry:
    """Registry for all agents in the system."""

    _instance: AgentRegistry | None = None
    _agents: dict[str, BaseAgent]
    _supervisors: dict[Division, BaseDivisionSupervisor]

    def __new__(cls) -> AgentRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._agents = {}
            cls._instance._supervisors = {}
        return cls._instance

    def register_agent(self, agent: BaseAgent) -> None:
        """Register an agent globally."""
        self._agents[agent.name] = agent

    def register_supervisor(
        self,
        division: Division,
        supervisor: BaseDivisionSupervisor,
    ) -> None:
        """Register a division supervisor."""
        self._supervisors[division] = supervisor

    def get_agent(self, name: str) -> BaseAgent | None:
        """Get an agent by name."""
        return self._agents.get(name)

    def get_supervisor(self, division: Division) -> BaseDivisionSupervisor | None:
        """Get a division supervisor."""
        return self._supervisors.get(division)

    def get_all_agents(self) -> dict[str, BaseAgent]:
        """Get all registered agents."""
        return self._agents.copy()

    def get_all_supervisors(self) -> dict[Division, BaseDivisionSupervisor]:
        """Get all registered supervisors."""
        return self._supervisors.copy()


# Global registry instance
agent_registry = AgentRegistry()
