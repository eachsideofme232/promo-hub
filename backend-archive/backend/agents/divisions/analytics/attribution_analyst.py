"""Attribution Analyst Agent - Marketing attribution and channel contribution analysis."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def analyze_attribution(
    brand_id: str,
    period: str = "30d",
    model: str = "data_driven",
) -> dict[str, Any]:
    """
    Analyze marketing attribution across channels.

    Args:
        brand_id: Brand ID
        period: Analysis period
        model: Attribution model (last_click, first_click, linear, data_driven)

    Returns:
        Attribution analysis results
    """
    return {
        "brand_id": brand_id,
        "period": period,
        "model": model,
        "total_conversions": 8500,
        "total_revenue": 255_000_000,
        "attribution_by_channel": {
            "naver_search": {
                "attributed_conversions": 2800,
                "attributed_revenue": 84_000_000,
                "contribution": 0.33,
                "role": "converter",
                "avg_position_in_path": 4.2,
            },
            "instagram_ads": {
                "attributed_conversions": 1950,
                "attributed_revenue": 58_500_000,
                "contribution": 0.23,
                "role": "initiator",
                "avg_position_in_path": 1.8,
            },
            "coupang_search": {
                "attributed_conversions": 1530,
                "attributed_revenue": 45_900_000,
                "contribution": 0.18,
                "role": "converter",
                "avg_position_in_path": 4.5,
            },
            "influencer": {
                "attributed_conversions": 1020,
                "attributed_revenue": 30_600_000,
                "contribution": 0.12,
                "role": "influencer",
                "avg_position_in_path": 2.5,
            },
            "kakao_channel": {
                "attributed_conversions": 680,
                "attributed_revenue": 20_400_000,
                "contribution": 0.08,
                "role": "supporter",
                "avg_position_in_path": 3.2,
            },
            "direct": {
                "attributed_conversions": 520,
                "attributed_revenue": 15_600_000,
                "contribution": 0.06,
                "role": "converter",
                "avg_position_in_path": 5.0,
            },
        },
        "path_insights": {
            "avg_touchpoints": 4.8,
            "avg_days_to_convert": 12,
            "most_common_path": "Instagram → Naver Blog → Naver Search → Purchase",
        },
    }


@tool
def compare_attribution_models(
    brand_id: str,
    period: str = "30d",
) -> dict[str, Any]:
    """
    Compare different attribution models.

    Args:
        brand_id: Brand ID
        period: Analysis period

    Returns:
        Attribution model comparison
    """
    channels = ["naver_search", "instagram_ads", "coupang_search", "influencer", "kakao_channel"]

    return {
        "brand_id": brand_id,
        "period": period,
        "model_comparison": {
            "last_click": {
                "naver_search": 0.42,
                "instagram_ads": 0.12,
                "coupang_search": 0.28,
                "influencer": 0.08,
                "kakao_channel": 0.10,
            },
            "first_click": {
                "naver_search": 0.15,
                "instagram_ads": 0.45,
                "coupang_search": 0.08,
                "influencer": 0.25,
                "kakao_channel": 0.07,
            },
            "linear": {
                "naver_search": 0.28,
                "instagram_ads": 0.25,
                "coupang_search": 0.20,
                "influencer": 0.15,
                "kakao_channel": 0.12,
            },
            "data_driven": {
                "naver_search": 0.33,
                "instagram_ads": 0.23,
                "coupang_search": 0.18,
                "influencer": 0.12,
                "kakao_channel": 0.14,
            },
        },
        "insights": [
            "Instagram undervalued in last-click, crucial for awareness",
            "Influencer impact spreads across journey, not just initiation",
            "Naver search captures intent, but needs upper-funnel support",
        ],
        "recommended_model": "data_driven",
        "reason": "Most balanced view of actual contribution",
    }


@tool
def analyze_customer_journey(
    conversion_id: str | None = None,
    segment: str = "all",
) -> dict[str, Any]:
    """
    Analyze customer journey paths.

    Args:
        conversion_id: Specific conversion to analyze
        segment: Customer segment

    Returns:
        Journey analysis
    """
    return {
        "segment": segment,
        "sample_size": 5000,
        "journey_patterns": [
            {
                "pattern": "Instagram → Naver Blog → Naver Search → Oliveyoung",
                "frequency": 0.22,
                "avg_value": 45000,
                "avg_days": 8,
                "description": "Discovery to research to purchase",
            },
            {
                "pattern": "Influencer → Instagram → Coupang",
                "frequency": 0.18,
                "avg_value": 38000,
                "avg_days": 5,
                "description": "Influencer-driven quick conversion",
            },
            {
                "pattern": "Naver Search → Oliveyoung (direct)",
                "frequency": 0.15,
                "avg_value": 32000,
                "avg_days": 1,
                "description": "Intent-driven immediate purchase",
            },
            {
                "pattern": "Kakao Gift → Repeat on Naver",
                "frequency": 0.12,
                "avg_value": 55000,
                "avg_days": 45,
                "description": "Gift recipient becomes customer",
            },
        ],
        "funnel_metrics": {
            "awareness_to_consideration": 0.35,
            "consideration_to_intent": 0.45,
            "intent_to_purchase": 0.68,
            "overall_conversion": 0.11,
        },
        "drop_off_points": [
            {"stage": "awareness → consideration", "drop": 0.65, "recommendation": "Improve retargeting"},
            {"stage": "intent → purchase", "drop": 0.32, "recommendation": "Reduce friction at checkout"},
        ],
    }


@tool
def calculate_channel_efficiency(
    brand_id: str,
    period: str = "30d",
) -> dict[str, Any]:
    """
    Calculate channel efficiency metrics.

    Args:
        brand_id: Brand ID
        period: Analysis period

    Returns:
        Channel efficiency analysis
    """
    return {
        "brand_id": brand_id,
        "period": period,
        "channel_efficiency": {
            "naver_search": {
                "spend": 25_000_000,
                "attributed_revenue": 84_000_000,
                "roas": 3.36,
                "cpa": 8929,
                "efficiency_score": 8.5,
            },
            "instagram_ads": {
                "spend": 18_000_000,
                "attributed_revenue": 58_500_000,
                "roas": 3.25,
                "cpa": 9231,
                "efficiency_score": 8.2,
            },
            "coupang_search": {
                "spend": 15_000_000,
                "attributed_revenue": 45_900_000,
                "roas": 3.06,
                "cpa": 9804,
                "efficiency_score": 7.8,
            },
            "influencer": {
                "spend": 20_000_000,
                "attributed_revenue": 30_600_000,
                "roas": 1.53,
                "cpa": 19608,
                "efficiency_score": 6.5,
            },
            "kakao_channel": {
                "spend": 5_000_000,
                "attributed_revenue": 20_400_000,
                "roas": 4.08,
                "cpa": 7353,
                "efficiency_score": 8.8,
            },
        },
        "optimization_recommendations": [
            "Increase Kakao Channel budget - highest efficiency",
            "Maintain Naver Search - strong converter",
            "Review Influencer spend - lower direct ROAS but brand value",
        ],
        "budget_reallocation_suggestion": {
            "from": "influencer",
            "to": "kakao_channel",
            "amount": 5_000_000,
            "projected_impact": "+12% overall ROAS",
        },
    }


class AttributionAnalyst(BaseAgent):
    """
    Attribution Analyst Agent.

    Responsibilities:
    - Analyze marketing attribution
    - Compare attribution models
    - Map customer journeys
    - Calculate channel efficiency
    """

    name = "attribution_analyst"
    role = "Marketing Attribution Expert"
    description = "Analyzes multi-touch attribution and channel contribution"
    division = Division.ANALYTICS

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            analyze_attribution,
            compare_attribution_models,
            analyze_customer_journey,
            calculate_channel_efficiency,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Attribution Analyst for Promotor, specializing in marketing attribution.

Your responsibilities:
1. Analyze multi-touch attribution
2. Compare attribution models
3. Map customer journeys
4. Calculate channel efficiency

Attribution models:
- Last-click: Credit to final touchpoint (biased to converters)
- First-click: Credit to initial touchpoint (biased to awareness)
- Linear: Equal credit across touchpoints
- Data-driven: ML-based credit assignment (recommended)

Channel roles:
- Initiator: Starts customer journey (awareness)
- Influencer: Assists consideration
- Converter: Closes the sale

Journey analysis:
- Map typical conversion paths
- Identify drop-off points
- Calculate funnel metrics
- Understand channel interplay

Efficiency metrics:
- ROAS: Revenue / Spend
- CPA: Spend / Conversions
- Efficiency score: Composite metric

When analyzing:
- Consider full funnel impact
- Don't over-credit last-click
- Recognize upper-funnel value
- Look at assisted conversions

Budget optimization:
- Reallocate from low-efficiency
- But maintain awareness channels
- Test incrementality
- Consider attribution lag

Respond in Korean if the user's query is in Korean."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process an attribution analysis request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "attribution_analysis",
                "model_comparison",
                "journey_mapping",
                "efficiency_calculation",
            ],
        }
