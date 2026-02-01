"""Influencer ROI Analyst Agent - KOL campaign tracking and ROI calculation."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def track_influencer_campaign(
    campaign_id: str,
) -> dict[str, Any]:
    """
    Track influencer campaign performance.

    Args:
        campaign_id: Campaign ID

    Returns:
        Campaign performance metrics
    """
    return {
        "campaign_id": campaign_id,
        "campaign_name": "Spring Skincare Launch",
        "period": {"start": "2026-01-10", "end": "2026-01-24"},
        "total_investment": 25_000_000,
        "influencers": [
            {
                "name": "뷰티크리에이터A",
                "platform": "YouTube",
                "tier": "mega",
                "followers": 1_200_000,
                "fee": 12_000_000,
                "content": {"videos": 1, "shorts": 2},
                "performance": {
                    "views": 450_000,
                    "likes": 28_000,
                    "comments": 1_850,
                    "engagement_rate": 0.066,
                    "tracked_sales": 380,
                    "attributed_revenue": 13_300_000,
                },
            },
            {
                "name": "스킨케어마니아B",
                "platform": "Instagram",
                "tier": "macro",
                "followers": 280_000,
                "fee": 8_000_000,
                "content": {"posts": 2, "reels": 3, "stories": 5},
                "performance": {
                    "impressions": 520_000,
                    "likes": 42_000,
                    "saves": 8_500,
                    "engagement_rate": 0.097,
                    "tracked_sales": 290,
                    "attributed_revenue": 10_150_000,
                },
            },
            {
                "name": "일반인리뷰어C",
                "platform": "TikTok",
                "tier": "micro",
                "followers": 45_000,
                "fee": 5_000_000,
                "content": {"videos": 5},
                "performance": {
                    "views": 850_000,
                    "likes": 95_000,
                    "shares": 12_000,
                    "engagement_rate": 0.126,
                    "tracked_sales": 420,
                    "attributed_revenue": 14_700_000,
                },
            },
        ],
        "totals": {
            "total_reach": 1_820_000,
            "total_engagement": 187_350,
            "total_tracked_sales": 1_090,
            "total_attributed_revenue": 38_150_000,
            "overall_roas": 1.53,
        },
    }


@tool
def calculate_influencer_roi(
    influencer_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate ROI for an influencer partnership.

    Args:
        influencer_data: Influencer performance data

    Returns:
        ROI calculation
    """
    fee = influencer_data.get("fee", 0)
    attributed_revenue = influencer_data.get("attributed_revenue", 0)
    views = influencer_data.get("views", 0)
    engagement = influencer_data.get("engagement", 0)

    # Calculate metrics
    roas = attributed_revenue / fee if fee > 0 else 0
    cost_per_view = fee / views if views > 0 else 0
    cost_per_engagement = fee / engagement if engagement > 0 else 0

    # Estimate media value
    estimated_media_value = views * 10 + engagement * 100  # Simplified EMV

    return {
        "investment": fee,
        "attributed_revenue": attributed_revenue,
        "roi_metrics": {
            "roas": roas,
            "roi_percentage": (attributed_revenue - fee) / fee if fee > 0 else 0,
            "cost_per_view": cost_per_view,
            "cost_per_engagement": cost_per_engagement,
            "cost_per_sale": fee / influencer_data.get("sales", 1),
        },
        "value_metrics": {
            "estimated_media_value": estimated_media_value,
            "emv_ratio": estimated_media_value / fee if fee > 0 else 0,
        },
        "assessment": "positive" if roas > 2.0 else "needs_review" if roas > 1.0 else "negative",
    }


@tool
def compare_influencer_tiers(
    brand_id: str,
    period: str = "90d",
) -> dict[str, Any]:
    """
    Compare performance across influencer tiers.

    Args:
        brand_id: Brand ID
        period: Analysis period

    Returns:
        Tier comparison analysis
    """
    return {
        "brand_id": brand_id,
        "period": period,
        "tier_comparison": {
            "mega": {
                "description": "1M+ followers",
                "campaigns": 3,
                "total_spend": 35_000_000,
                "total_revenue": 52_500_000,
                "avg_roas": 1.5,
                "avg_engagement_rate": 0.045,
                "reach_efficiency": 0.85,
                "best_for": ["brand awareness", "launches"],
            },
            "macro": {
                "description": "100K-1M followers",
                "campaigns": 8,
                "total_spend": 45_000_000,
                "total_revenue": 90_000_000,
                "avg_roas": 2.0,
                "avg_engagement_rate": 0.065,
                "reach_efficiency": 0.78,
                "best_for": ["consideration", "product education"],
            },
            "micro": {
                "description": "10K-100K followers",
                "campaigns": 15,
                "total_spend": 25_000_000,
                "total_revenue": 75_000_000,
                "avg_roas": 3.0,
                "avg_engagement_rate": 0.095,
                "reach_efficiency": 0.65,
                "best_for": ["conversions", "authentic reviews"],
            },
            "nano": {
                "description": "<10K followers",
                "campaigns": 25,
                "total_spend": 10_000_000,
                "total_revenue": 28_000_000,
                "avg_roas": 2.8,
                "avg_engagement_rate": 0.12,
                "reach_efficiency": 0.45,
                "best_for": ["niche targeting", "UGC generation"],
            },
        },
        "recommendation": "Optimal mix: 20% mega, 30% macro, 40% micro, 10% nano",
    }


@tool
def find_top_performers(
    brand_id: str,
    metric: str = "roas",
    limit: int = 10,
) -> list[dict[str, Any]]:
    """
    Find top performing influencers.

    Args:
        brand_id: Brand ID
        metric: Metric to rank by (roas, engagement, reach)
        limit: Number of results

    Returns:
        Top performing influencers
    """
    return [
        {
            "rank": 1,
            "name": "스킨케어전문가A",
            "platform": "YouTube",
            "tier": "micro",
            "total_campaigns": 5,
            "avg_roas": 4.2,
            "total_revenue": 45_000_000,
            "engagement_rate": 0.11,
            "audience_fit": 0.92,
            "recommendation": "Increase frequency, consider ambassador program",
        },
        {
            "rank": 2,
            "name": "뷰티인플루언서B",
            "platform": "Instagram",
            "tier": "macro",
            "total_campaigns": 3,
            "avg_roas": 3.8,
            "total_revenue": 38_000_000,
            "engagement_rate": 0.085,
            "audience_fit": 0.88,
            "recommendation": "Good performer, maintain partnership",
        },
        {
            "rank": 3,
            "name": "화장품리뷰어C",
            "platform": "TikTok",
            "tier": "micro",
            "total_campaigns": 4,
            "avg_roas": 3.5,
            "total_revenue": 28_000_000,
            "engagement_rate": 0.14,
            "audience_fit": 0.85,
            "recommendation": "High engagement, expand content types",
        },
    ][:limit]


class InfluencerROIAnalyst(BaseAgent):
    """
    Influencer ROI Analyst Agent.

    Responsibilities:
    - Track influencer campaign performance
    - Calculate ROI metrics
    - Compare tier effectiveness
    - Identify top performers
    """

    name = "influencer_roi_analyst"
    role = "Influencer Performance Analyst"
    description = "Tracks KOL campaigns, calculates ROI, and optimizes influencer mix"
    division = Division.ANALYTICS

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            track_influencer_campaign,
            calculate_influencer_roi,
            compare_influencer_tiers,
            find_top_performers,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Influencer ROI Analyst for Promotor, specializing in KOL performance analysis.

Your responsibilities:
1. Track influencer campaign performance
2. Calculate ROI and efficiency metrics
3. Compare tier effectiveness
4. Identify and recommend top performers

Influencer tiers:
- Mega: 1M+ followers - brand awareness
- Macro: 100K-1M followers - consideration
- Micro: 10K-100K followers - conversions
- Nano: <10K followers - UGC, authenticity

Key metrics:
- ROAS (Return on Ad Spend): Revenue / Cost
- EMV (Earned Media Value): View/engagement value
- Engagement rate: Interactions / Reach
- Cost per acquisition: Fee / Sales

Platform considerations:
- YouTube: Long-form, higher trust, longer shelf life
- Instagram: Visual, lifestyle, Stories + Reels
- TikTok: Viral potential, younger audience
- Naver Blog: SEO value, search discovery

ROI benchmarks:
- Mega: 1.0-2.0x ROAS typical
- Macro: 1.5-2.5x ROAS typical
- Micro: 2.0-4.0x ROAS typical
- Nano: 2.0-3.5x ROAS typical

When analyzing:
- Track attributed vs assisted conversions
- Consider brand lift impact
- Note content quality and authenticity
- Evaluate audience fit

Respond in Korean if the user's query is in Korean."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process an influencer analysis request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "campaign_tracking",
                "roi_calculation",
                "tier_comparison",
                "performer_identification",
            ],
        }
