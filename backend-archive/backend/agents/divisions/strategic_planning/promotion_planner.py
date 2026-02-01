"""Promotion Planner Agent - Promotion strategy and calendar specialist."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


# Tools for Promotion Planner
@tool
def create_promotion_calendar(
    start_date: str,
    end_date: str,
    brand_id: str,
    channels: list[str],
) -> dict[str, Any]:
    """
    Create a promotion calendar for a specified period.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        brand_id: Brand identifier
        channels: List of channels to include

    Returns:
        Promotion calendar with slots and recommendations
    """
    # This would integrate with database in production
    return {
        "calendar_id": f"cal_{brand_id}_{start_date}",
        "period": {"start": start_date, "end": end_date},
        "channels": channels,
        "slots": [
            {
                "date": "2026-04-15",
                "type": "flash_sale",
                "channels": ["oliveyoung", "coupang"],
                "recommended": True,
            },
            {
                "date": "2026-05-01",
                "type": "seasonal_campaign",
                "channels": ["all"],
                "recommended": True,
            },
        ],
        "status": "draft",
    }


@tool
def get_promotion_templates(category: str, season: str) -> list[dict[str, Any]]:
    """
    Get promotion templates based on category and season.

    Args:
        category: Product category (e.g., skincare, makeup, sunscreen)
        season: Season or period (e.g., spring, summer, holiday)

    Returns:
        List of promotion templates
    """
    templates = {
        ("sunscreen", "summer"): [
            {
                "name": "UV Protection Campaign",
                "duration_days": 14,
                "discount_range": "15-25%",
                "bundle_suggestion": "sunscreen + moisturizer",
            },
            {
                "name": "Beach Ready Bundle",
                "duration_days": 7,
                "discount_range": "20-30%",
                "bundle_suggestion": "sunscreen + lip balm SPF",
            },
        ],
        ("skincare", "spring"): [
            {
                "name": "Spring Refresh",
                "duration_days": 10,
                "discount_range": "10-20%",
                "bundle_suggestion": "cleanser + toner + moisturizer",
            },
        ],
    }
    return templates.get((category.lower(), season.lower()), [])


@tool
def analyze_promotion_timing(
    product_category: str,
    target_channels: list[str],
    quarter: str,
) -> dict[str, Any]:
    """
    Analyze optimal timing for promotions based on historical data.

    Args:
        product_category: Category of products
        target_channels: Channels to analyze
        quarter: Quarter (Q1, Q2, Q3, Q4)

    Returns:
        Timing analysis with recommendations
    """
    # Mock analysis - would use ML models in production
    timing_data = {
        "Q2": {
            "peak_weeks": [18, 19, 20, 21, 22],
            "peak_months": ["May"],
            "avoid_dates": ["2026-05-05"],  # Children's Day
            "best_days": ["Friday", "Saturday"],
            "competitor_activity": "high",
        }
    }
    return timing_data.get(quarter, {"message": "No data available"})


class PromotionPlanner(BaseAgent):
    """
    Promotion Planner Agent.

    Responsibilities:
    - Annual/quarterly/monthly/weekly promotion goal setting
    - Promotion calendar creation and management
    - Campaign strategy development
    - Promotion template recommendations
    """

    name = "promotion_planner"
    role = "Promotion Strategy Specialist"
    description = "Creates and manages promotion calendars, strategies, and campaigns"
    division = Division.STRATEGIC_PLANNING

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            create_promotion_calendar,
            get_promotion_templates,
            analyze_promotion_timing,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Promotion Planner for Promotor, specializing in beauty brand promotion strategies.

Your responsibilities:
1. Create and manage promotion calendars (annual, quarterly, monthly, weekly)
2. Develop campaign strategies aligned with brand goals
3. Recommend optimal promotion timing based on market data
4. Design promotion structures (discounts, bundles, flash sales)

Key considerations for K-beauty promotions:
- Major shopping events: 11.11, Black Friday, Chuseok, Lunar New Year
- Channel-specific events: Oliveyoung Festa, Coupang Wow Week
- Seasonal patterns: UV products peak in May-August
- Ingredient trends: Centella, Retinol, Vitamin C cycles

When creating plans:
- Consider competitor activity windows
- Account for inventory lead times (4-6 weeks)
- Align with channel promotional calendars
- Balance margin preservation with sales goals

Output format:
- Clear timeline with specific dates
- Channel-specific recommendations
- Expected outcomes and KPIs
- Risk factors and mitigation

Respond in Korean if the user's query is in Korean."""

    async def create_promotion_plan(
        self,
        state: PromotorStateDict,
        period: str,
        category: str | None = None,
    ) -> dict[str, Any]:
        """
        Create a comprehensive promotion plan.

        Args:
            state: Current state
            period: Planning period (Q1, Q2, monthly, etc.)
            category: Optional product category focus

        Returns:
            Detailed promotion plan
        """
        brand_id = state.get("brand_id", "default")
        channels = state.get("active_channels", ["oliveyoung", "coupang", "naver", "kakao"])

        # Get timing analysis
        timing = analyze_promotion_timing.invoke({
            "product_category": category or "skincare",
            "target_channels": channels,
            "quarter": period,
        })

        # Get templates
        season_map = {"Q1": "winter", "Q2": "spring", "Q3": "summer", "Q4": "fall"}
        season = season_map.get(period, "spring")
        templates = get_promotion_templates.invoke({
            "category": category or "skincare",
            "season": season,
        })

        return {
            "period": period,
            "brand_id": brand_id,
            "channels": channels,
            "timing_analysis": timing,
            "recommended_templates": templates,
            "summary": f"Promotion plan created for {period} focusing on {len(channels)} channels",
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a promotion planning request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "promotion_calendar",
                "campaign_strategy",
                "timing_optimization",
                "template_recommendations",
            ],
        }
