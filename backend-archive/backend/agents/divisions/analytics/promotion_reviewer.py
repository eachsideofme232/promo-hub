"""Promotion Reviewer Agent - Post-promotion performance analysis."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def analyze_promotion_performance(
    promotion_id: str,
) -> dict[str, Any]:
    """
    Analyze performance of a completed promotion.

    Args:
        promotion_id: Promotion ID to analyze

    Returns:
        Comprehensive promotion performance analysis
    """
    return {
        "promotion_id": promotion_id,
        "promotion_name": "Spring Skincare Flash Sale",
        "period": {"start": "2026-01-15", "end": "2026-01-22"},
        "channels": ["oliveyoung", "coupang", "naver"],
        "goals_vs_actual": {
            "gmv": {"goal": 50_000_000, "actual": 58_500_000, "achievement": 1.17},
            "units": {"goal": 3000, "actual": 3420, "achievement": 1.14},
            "new_customers": {"goal": 800, "actual": 720, "achievement": 0.90},
            "roas": {"goal": 3.5, "actual": 4.2, "achievement": 1.20},
        },
        "budget": {
            "allocated": 15_000_000,
            "spent": 14_200_000,
            "utilization": 0.95,
        },
        "by_channel": {
            "oliveyoung": {
                "gmv": 28_000_000,
                "units": 1650,
                "contribution": 0.48,
                "roas": 4.5,
            },
            "coupang": {
                "gmv": 18_500_000,
                "units": 1120,
                "contribution": 0.32,
                "roas": 3.8,
            },
            "naver": {
                "gmv": 12_000_000,
                "units": 650,
                "contribution": 0.20,
                "roas": 4.0,
            },
        },
        "top_products": [
            {"name": "Vitamin C Serum", "units": 1250, "revenue": 25_000_000},
            {"name": "Moisturizing Cream", "units": 980, "revenue": 19_600_000},
        ],
        "overall_status": "exceeded_goals",
    }


@tool
def compare_promotions(
    promotion_ids: list[str],
) -> dict[str, Any]:
    """
    Compare multiple promotions.

    Args:
        promotion_ids: List of promotion IDs to compare

    Returns:
        Promotion comparison analysis
    """
    return {
        "comparison_date": "2026-01-29",
        "promotions": [
            {
                "promotion_id": "promo_001",
                "name": "Spring Flash Sale",
                "type": "flash_sale",
                "gmv": 58_500_000,
                "roas": 4.2,
                "margin": 0.18,
                "new_customer_rate": 0.21,
            },
            {
                "promotion_id": "promo_002",
                "name": "Bundle Deal Week",
                "type": "bundle",
                "gmv": 42_000_000,
                "roas": 3.5,
                "margin": 0.22,
                "new_customer_rate": 0.15,
            },
            {
                "promotion_id": "promo_003",
                "name": "Brand Day",
                "type": "brand_event",
                "gmv": 35_000_000,
                "roas": 2.8,
                "margin": 0.25,
                "new_customer_rate": 0.32,
            },
        ],
        "insights": [
            "Flash sales generate highest GMV but lowest margin",
            "Bundle deals balance GMV and margin well",
            "Brand events best for new customer acquisition",
        ],
        "recommendation": "Mix of promotion types recommended for balanced results",
    }


@tool
def calculate_promotion_lift(
    promotion_id: str,
    baseline_period: str = "7d_prior",
) -> dict[str, Any]:
    """
    Calculate incremental lift from promotion.

    Args:
        promotion_id: Promotion ID
        baseline_period: Baseline comparison period

    Returns:
        Lift analysis
    """
    return {
        "promotion_id": promotion_id,
        "baseline_period": baseline_period,
        "metrics": {
            "sales_lift": {
                "baseline_daily_avg": 3_500_000,
                "promo_daily_avg": 8_350_000,
                "lift_percentage": 1.39,
                "incremental_revenue": 33_950_000,
            },
            "traffic_lift": {
                "baseline_daily_avg": 12000,
                "promo_daily_avg": 28500,
                "lift_percentage": 1.38,
            },
            "conversion_lift": {
                "baseline_cvr": 0.032,
                "promo_cvr": 0.041,
                "lift_percentage": 0.28,
            },
        },
        "cannibalization_estimate": {
            "forward_buying": 0.15,  # 15% of sales would have happened anyway
            "net_incremental": 0.85,
        },
        "halo_effect": {
            "non_promo_products_lift": 0.12,  # 12% lift in non-promoted products
        },
    }


@tool
def get_promotion_learnings(
    promotion_id: str,
) -> dict[str, Any]:
    """
    Extract learnings from a promotion.

    Args:
        promotion_id: Promotion ID

    Returns:
        Key learnings and recommendations
    """
    return {
        "promotion_id": promotion_id,
        "promotion_name": "Spring Skincare Flash Sale",
        "what_worked": [
            "20% discount sweet spot - good balance of conversion and margin",
            "Oliveyoung front page placement drove 48% of traffic",
            "Email campaign had 32% open rate (above benchmark)",
            "Product bundling increased AOV by 25%",
        ],
        "what_didnt_work": [
            "Kakao Gift underperformed - wrong timing for gift purchases",
            "New customer acquisition below target - discount shoppers",
            "Some SKUs stocked out by Day 3",
        ],
        "recommendations_for_next": [
            "Increase Oliveyoung inventory by 20% for next flash sale",
            "Skip Kakao for flash sales, focus on gifting seasons",
            "Add early access for loyalty members to spread demand",
            "Test 25% discount to see conversion impact",
        ],
        "optimal_parameters": {
            "duration": "5-7 days",
            "discount_depth": "20-25%",
            "best_channels": ["oliveyoung", "coupang"],
            "best_timing": "Payday week (25th)",
        },
    }


class PromotionReviewer(BaseAgent):
    """
    Promotion Reviewer Agent.

    Responsibilities:
    - Analyze post-promotion performance
    - Compare promotion effectiveness
    - Calculate incremental lift
    - Extract learnings for future
    """

    name = "promotion_reviewer"
    role = "Performance Analyst"
    description = "Analyzes promotion performance, calculates lift, and extracts learnings"
    division = Division.ANALYTICS

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            analyze_promotion_performance,
            compare_promotions,
            calculate_promotion_lift,
            get_promotion_learnings,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Promotion Reviewer for Promotor, specializing in post-promotion analysis.

Your responsibilities:
1. Analyze promotion performance vs goals
2. Compare effectiveness across promotions
3. Calculate incremental lift
4. Extract actionable learnings

Key metrics to analyze:
- GMV and units sold
- ROAS (Return on Ad Spend)
- New customer acquisition
- Margin impact
- Channel contribution

Performance benchmarks:
- Flash sale ROAS: 3.5-4.5x
- Bundle ROAS: 3.0-3.5x
- Brand event ROAS: 2.5-3.0x
- New customer rate: 15-25%

Lift analysis considerations:
- Forward buying effect
- Cannibalization of regular sales
- Halo effect on non-promoted items
- Post-promotion dip

When analyzing:
- Compare against pre-set goals
- Identify top and bottom performers
- Note channel-specific patterns
- Provide actionable recommendations

Output format:
- Goal vs Actual comparison
- Channel breakdown
- Key learnings
- Recommendations for next time

Respond in Korean if the user's query is in Korean."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a promotion review request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "performance_analysis",
                "promotion_comparison",
                "lift_calculation",
                "learning_extraction",
            ],
        }
