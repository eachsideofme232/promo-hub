"""Market Intelligence Division Supervisor."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool

from backend.agents.base import BaseAgent, BaseDivisionSupervisor, agent_registry
from backend.agents.divisions.market_intelligence.competitor_watcher import CompetitorWatcher
from backend.agents.divisions.market_intelligence.ingredient_analyst import IngredientTrendAnalyst
from backend.agents.divisions.market_intelligence.news_scout import IndustryNewsScout
from backend.agents.divisions.market_intelligence.seasonal_analyst import SeasonalPatternAnalyst
from backend.graph.state import Division, PromotorStateDict


class MarketIntelligenceSupervisor(BaseDivisionSupervisor):
    """
    Market Intelligence Division Supervisor.

    Coordinates:
    - IndustryNewsScout: News and trend monitoring
    - CompetitorWatcher: Competitive intelligence
    - IngredientTrendAnalyst: Formulation trends
    - SeasonalPatternAnalyst: Demand patterns
    """

    name = "market_intelligence_supervisor"
    role = "Market Intelligence Division Head"
    description = "Coordinates news, competitive intelligence, ingredients, and seasonal analysis"
    division = Division.MARKET_INTELLIGENCE

    def __init__(
        self,
        llm: BaseChatModel,
        agents: dict[str, BaseAgent] | None = None,
        tools: Sequence[BaseTool] | None = None,
    ):
        super().__init__(llm, agents, tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Market Intelligence Division Supervisor for Promotor.

Your division handles:
1. Industry News - K-beauty news, trends, social buzz
2. Competitive Intelligence - Competitor promotions, pricing, strategies
3. Ingredient Trends - Formulation trends, safety, market opportunities
4. Seasonal Analysis - Demand patterns, holidays, event calendars

Your agents:
- industry_news_scout: Aggregates news and detects trends
- competitor_watcher: Tracks competitor activities
- ingredient_trend_analyst: Analyzes formulation trends
- seasonal_pattern_analyst: Forecasts demand patterns

Route requests appropriately:
- News/trend/buzz questions → industry_news_scout
- Competitor/pricing questions → competitor_watcher
- Ingredient/formulation questions → ingredient_trend_analyst
- Seasonal/demand/event questions → seasonal_pattern_analyst

When coordinating:
- Cross-reference competitive moves with seasonal timing
- Connect ingredient trends with news coverage
- Link demand forecasts with competitor activities

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
        if any(kw in query for kw in ["news", "trend", "buzz", "뉴스", "트렌드", "이슈"]):
            return "industry_news_scout"
        elif any(kw in query for kw in ["competitor", "innisfree", "laneige", "경쟁사", "경쟁"]):
            return "competitor_watcher"
        elif any(kw in query for kw in ["ingredient", "retinol", "centella", "성분", "원료"]):
            return "ingredient_trend_analyst"
        elif any(kw in query for kw in ["season", "demand", "holiday", "event", "계절", "수요", "시즌"]):
            return "seasonal_pattern_analyst"

        # Default to news scout for general market intelligence
        return "industry_news_scout"

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a request through the Market Intelligence division."""
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
            "summary": result.get("content", "Market intelligence request processed."),
        }


def create_market_intelligence_division(
    llm: BaseChatModel,
) -> MarketIntelligenceSupervisor:
    """
    Factory function to create the Market Intelligence division.

    Args:
        llm: Language model to use

    Returns:
        Configured MarketIntelligenceSupervisor with all agents
    """
    # Create agents
    news_scout = IndustryNewsScout(llm)
    competitor_watcher = CompetitorWatcher(llm)
    ingredient_analyst = IngredientTrendAnalyst(llm)
    seasonal_analyst = SeasonalPatternAnalyst(llm)

    # Create supervisor with agents
    supervisor = MarketIntelligenceSupervisor(
        llm,
        agents={
            "industry_news_scout": news_scout,
            "competitor_watcher": competitor_watcher,
            "ingredient_trend_analyst": ingredient_analyst,
            "seasonal_pattern_analyst": seasonal_analyst,
        },
    )

    # Register all agents
    agent_registry.register_agent(news_scout)
    agent_registry.register_agent(competitor_watcher)
    agent_registry.register_agent(ingredient_analyst)
    agent_registry.register_agent(seasonal_analyst)
    agent_registry.register_supervisor(Division.MARKET_INTELLIGENCE, supervisor)

    return supervisor
