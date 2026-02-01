"""Analytics Division Supervisor."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool

from backend.agents.base import BaseAgent, BaseDivisionSupervisor, agent_registry
from backend.agents.divisions.analytics.attribution_analyst import AttributionAnalyst
from backend.agents.divisions.analytics.bundle_analyzer import BundleAnalyzer
from backend.agents.divisions.analytics.influencer_analyst import InfluencerROIAnalyst
from backend.agents.divisions.analytics.margin_calculator import MarginCalculator
from backend.agents.divisions.analytics.promotion_reviewer import PromotionReviewer
from backend.agents.divisions.analytics.sentiment_analyst import ReviewSentimentAnalyst
from backend.agents.divisions.analytics.stockout_predictor import StockoutPredictor
from backend.graph.state import Division, PromotorStateDict


class AnalyticsSupervisor(BaseDivisionSupervisor):
    """
    Analytics Division Supervisor.

    Coordinates:
    - ReviewSentimentAnalyst: Customer sentiment analysis
    - PromotionReviewer: Post-promotion analysis
    - BundleAnalyzer: Bundle optimization
    - MarginCalculator: Profitability analysis
    - StockoutPredictor: Inventory forecasting
    - InfluencerROIAnalyst: KOL performance
    - AttributionAnalyst: Marketing attribution
    """

    name = "analytics_supervisor"
    role = "Analytics Division Head"
    description = "Coordinates all analytics functions"
    division = Division.ANALYTICS

    def __init__(
        self,
        llm: BaseChatModel,
        agents: dict[str, BaseAgent] | None = None,
        tools: Sequence[BaseTool] | None = None,
    ):
        super().__init__(llm, agents, tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Analytics Division Supervisor for Promotor.

Your division handles:
1. Sentiment Analysis - Customer reviews and feedback
2. Promotion Review - Post-promotion performance
3. Bundle Analysis - Product bundling optimization
4. Margin Calculation - Profitability analysis
5. Stockout Prediction - Inventory forecasting
6. Influencer ROI - KOL campaign performance
7. Attribution - Marketing channel contribution

Your agents:
- review_sentiment_analyst: Korean NLP sentiment analysis
- promotion_reviewer: Post-promotion analysis
- bundle_analyzer: Bundle optimization
- margin_calculator: Profitability analysis
- stockout_predictor: Inventory forecasting
- influencer_roi_analyst: KOL performance
- attribution_analyst: Marketing attribution

Route requests appropriately:
- Review/sentiment/feedback → review_sentiment_analyst
- Promotion performance/results → promotion_reviewer
- Bundle/cross-sell/upsell → bundle_analyzer
- Margin/profit/discount → margin_calculator
- Stock/inventory/forecast → stockout_predictor
- Influencer/KOL/creator → influencer_roi_analyst
- Attribution/channel contribution → attribution_analyst

When coordinating:
- Connect insights across analytics areas
- Provide actionable recommendations
- Highlight correlations and patterns
- Support data-driven decisions

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
        if any(kw in query for kw in ["review", "sentiment", "feedback", "리뷰", "평가", "고객반응"]):
            return "review_sentiment_analyst"
        elif any(kw in query for kw in ["promotion result", "performance", "how did", "성과", "결과"]):
            return "promotion_reviewer"
        elif any(kw in query for kw in ["bundle", "cross-sell", "upsell", "세트", "번들"]):
            return "bundle_analyzer"
        elif any(kw in query for kw in ["margin", "profit", "discount", "마진", "수익", "할인"]):
            return "margin_calculator"
        elif any(kw in query for kw in ["stock", "inventory", "stockout", "재고", "품절"]):
            return "stockout_predictor"
        elif any(kw in query for kw in ["influencer", "kol", "creator", "인플루언서", "크리에이터"]):
            return "influencer_roi_analyst"
        elif any(kw in query for kw in ["attribution", "channel contribution", "기여도", "어트리뷰션"]):
            return "attribution_analyst"

        # Default to promotion reviewer for general analytics
        return "promotion_reviewer"

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a request through the Analytics division."""
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
            "summary": result.get("content", "Analytics request processed."),
        }


def create_analytics_division(
    llm: BaseChatModel,
) -> AnalyticsSupervisor:
    """
    Factory function to create the Analytics division.

    Args:
        llm: Language model to use

    Returns:
        Configured AnalyticsSupervisor with all agents
    """
    # Create agents
    sentiment_analyst = ReviewSentimentAnalyst(llm)
    promotion_reviewer = PromotionReviewer(llm)
    bundle_analyzer = BundleAnalyzer(llm)
    margin_calculator = MarginCalculator(llm)
    stockout_predictor = StockoutPredictor(llm)
    influencer_analyst = InfluencerROIAnalyst(llm)
    attribution_analyst = AttributionAnalyst(llm)

    # Create supervisor with agents
    supervisor = AnalyticsSupervisor(
        llm,
        agents={
            "review_sentiment_analyst": sentiment_analyst,
            "promotion_reviewer": promotion_reviewer,
            "bundle_analyzer": bundle_analyzer,
            "margin_calculator": margin_calculator,
            "stockout_predictor": stockout_predictor,
            "influencer_roi_analyst": influencer_analyst,
            "attribution_analyst": attribution_analyst,
        },
    )

    # Register all agents
    agent_registry.register_agent(sentiment_analyst)
    agent_registry.register_agent(promotion_reviewer)
    agent_registry.register_agent(bundle_analyzer)
    agent_registry.register_agent(margin_calculator)
    agent_registry.register_agent(stockout_predictor)
    agent_registry.register_agent(influencer_analyst)
    agent_registry.register_agent(attribution_analyst)
    agent_registry.register_supervisor(Division.ANALYTICS, supervisor)

    return supervisor
