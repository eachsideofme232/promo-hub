"""Channel Management Division Supervisor."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool

from backend.agents.base import BaseAgent, BaseDivisionSupervisor, agent_registry
from backend.agents.divisions.channel_management.coupang_agent import CoupangAgent
from backend.agents.divisions.channel_management.cross_channel_syncer import CrossChannelSyncer
from backend.agents.divisions.channel_management.kakao_agent import KakaoAgent
from backend.agents.divisions.channel_management.naver_agent import NaverAgent
from backend.agents.divisions.channel_management.oliveyoung_agent import OliveyoungAgent
from backend.graph.state import Division, PromotorStateDict


class ChannelManagementSupervisor(BaseDivisionSupervisor):
    """
    Channel Management Division Supervisor.

    Coordinates:
    - OliveyoungAgent: Oliveyoung operations
    - CoupangAgent: Coupang operations
    - NaverAgent: Naver operations
    - KakaoAgent: Kakao operations
    - CrossChannelSyncer: Multi-channel coordination
    """

    name = "channel_management_supervisor"
    role = "Channel Management Division Head"
    description = "Coordinates all e-commerce channel operations"
    division = Division.CHANNEL_MANAGEMENT

    def __init__(
        self,
        llm: BaseChatModel,
        agents: dict[str, BaseAgent] | None = None,
        tools: Sequence[BaseTool] | None = None,
    ):
        super().__init__(llm, agents, tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Channel Management Division Supervisor for Promotor.

Your division handles:
1. Oliveyoung - Rankings, deals, reviews
2. Coupang - WING portal, Rocket delivery, ads
3. Naver - Smart Store, Shopping Live, search ads
4. Kakao - Gift commerce, channel messaging
5. Cross-Channel - Price sync, inventory, MAP monitoring

Your agents:
- oliveyoung_agent: Oliveyoung channel specialist
- coupang_agent: Coupang channel specialist
- naver_agent: Naver channel specialist
- kakao_agent: Kakao channel specialist
- cross_channel_syncer: Multi-channel coordinator

Route requests appropriately:
- Oliveyoung/올리브영 questions → oliveyoung_agent
- Coupang/쿠팡/Rocket questions → coupang_agent
- Naver/네이버/Smart Store questions → naver_agent
- Kakao/카카오/Gift questions → kakao_agent
- Price sync/multi-channel/consistency → cross_channel_syncer

Channel priority considerations:
- Traffic: Oliveyoung > Coupang > Naver > Kakao
- Margin: Naver > Coupang > Kakao > Oliveyoung
- Gift/Premium: Kakao > Naver
- Speed to market: Kakao > Naver > Coupang > Oliveyoung

When coordinating:
- Consider channel-specific requirements
- Maintain price consistency
- Balance inventory across channels
- Optimize for overall brand performance

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

        # Route based on channel keywords
        if any(kw in query for kw in ["oliveyoung", "올리브영", "올영"]):
            return "oliveyoung_agent"
        elif any(kw in query for kw in ["coupang", "쿠팡", "rocket", "로켓"]):
            return "coupang_agent"
        elif any(kw in query for kw in ["naver", "네이버", "smart store", "스마트스토어", "shopping live"]):
            return "naver_agent"
        elif any(kw in query for kw in ["kakao", "카카오", "gift", "선물하기"]):
            return "kakao_agent"
        elif any(kw in query for kw in ["sync", "consistency", "cross", "all channel", "전체", "동기화", "일치"]):
            return "cross_channel_syncer"

        # Default to cross-channel syncer for general channel queries
        return "cross_channel_syncer"

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a request through the Channel Management division."""
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
            "summary": result.get("content", "Channel management request processed."),
        }


def create_channel_management_division(
    llm: BaseChatModel,
) -> ChannelManagementSupervisor:
    """
    Factory function to create the Channel Management division.

    Args:
        llm: Language model to use

    Returns:
        Configured ChannelManagementSupervisor with all agents
    """
    # Create agents
    oliveyoung_agent = OliveyoungAgent(llm)
    coupang_agent = CoupangAgent(llm)
    naver_agent = NaverAgent(llm)
    kakao_agent = KakaoAgent(llm)
    cross_channel_syncer = CrossChannelSyncer(llm)

    # Create supervisor with agents
    supervisor = ChannelManagementSupervisor(
        llm,
        agents={
            "oliveyoung_agent": oliveyoung_agent,
            "coupang_agent": coupang_agent,
            "naver_agent": naver_agent,
            "kakao_agent": kakao_agent,
            "cross_channel_syncer": cross_channel_syncer,
        },
    )

    # Register all agents
    agent_registry.register_agent(oliveyoung_agent)
    agent_registry.register_agent(coupang_agent)
    agent_registry.register_agent(naver_agent)
    agent_registry.register_agent(kakao_agent)
    agent_registry.register_agent(cross_channel_syncer)
    agent_registry.register_supervisor(Division.CHANNEL_MANAGEMENT, supervisor)

    return supervisor
