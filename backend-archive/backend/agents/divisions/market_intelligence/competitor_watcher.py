"""Competitor Watcher Agent - Competitive intelligence and tracking."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def get_competitor_promotions(
    competitor_name: str | None = None,
    channel: str = "all",
    days_back: int = 30,
) -> list[dict[str, Any]]:
    """
    Get competitor promotions and deals.

    Args:
        competitor_name: Specific competitor to track (None for all)
        channel: Channel filter
        days_back: Days to look back

    Returns:
        List of competitor promotions
    """
    today = datetime.now()
    promotions = [
        {
            "competitor": "Innisfree",
            "promotion_type": "bundle",
            "channel": "oliveyoung",
            "discount": "25%",
            "start_date": (today - timedelta(days=5)).strftime("%Y-%m-%d"),
            "end_date": (today + timedelta(days=9)).strftime("%Y-%m-%d"),
            "products": ["Green Tea Serum", "Green Tea Moisturizer"],
            "notes": "Buy 1 Get 1 50% off",
        },
        {
            "competitor": "Laneige",
            "promotion_type": "flash_sale",
            "channel": "coupang",
            "discount": "30%",
            "start_date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
            "end_date": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
            "products": ["Water Bank Cream", "Lip Sleeping Mask"],
            "notes": "Limited time rocket delivery deal",
        },
        {
            "competitor": "Etude",
            "promotion_type": "new_launch",
            "channel": "all",
            "discount": "20%",
            "start_date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (today + timedelta(days=14)).strftime("%Y-%m-%d"),
            "products": ["Soon Jung Line Extension"],
            "notes": "Launch promotion with GWP",
        },
    ]

    if competitor_name:
        promotions = [p for p in promotions if competitor_name.lower() in p["competitor"].lower()]

    if channel != "all":
        promotions = [p for p in promotions if p["channel"] in [channel, "all"]]

    return promotions


@tool
def get_competitor_pricing(
    product_category: str,
    channel: str = "oliveyoung",
) -> list[dict[str, Any]]:
    """
    Get competitor pricing for a category.

    Args:
        product_category: Product category to compare
        channel: Channel to check pricing

    Returns:
        Competitor pricing data
    """
    pricing_data = {
        "sunscreen": [
            {
                "competitor": "Innisfree",
                "product": "Daily UV Defense",
                "regular_price": 22000,
                "current_price": 17600,
                "discount": "20%",
                "channel": "oliveyoung",
            },
            {
                "competitor": "Laneige",
                "product": "Watery Sun Cream",
                "regular_price": 32000,
                "current_price": 25600,
                "discount": "20%",
                "channel": "oliveyoung",
            },
            {
                "competitor": "Missha",
                "product": "All Around Safe Block",
                "regular_price": 15000,
                "current_price": 12000,
                "discount": "20%",
                "channel": "oliveyoung",
            },
        ],
        "serum": [
            {
                "competitor": "COSRX",
                "product": "Snail Mucin Essence",
                "regular_price": 25000,
                "current_price": 18750,
                "discount": "25%",
                "channel": "oliveyoung",
            },
            {
                "competitor": "Some By Mi",
                "product": "AHA BHA PHA Serum",
                "regular_price": 18000,
                "current_price": 14400,
                "discount": "20%",
                "channel": "oliveyoung",
            },
        ],
    }
    return pricing_data.get(product_category.lower(), [])


@tool
def get_competitor_launches(
    months_ahead: int = 3,
) -> list[dict[str, Any]]:
    """
    Get upcoming competitor product launches.

    Args:
        months_ahead: Months to look ahead

    Returns:
        List of upcoming launches
    """
    return [
        {
            "competitor": "Amorepacific",
            "product_line": "Retinol Advanced",
            "expected_launch": "2026-Q2",
            "category": "anti-aging",
            "key_claims": ["encapsulated retinol", "less irritation"],
            "target_demographic": "30-45",
            "estimated_price_range": "45000-85000",
            "confidence": "high",
        },
        {
            "competitor": "LG H&H",
            "product_line": "The History of Whoo Limited Edition",
            "expected_launch": "2026-05",
            "category": "luxury skincare",
            "key_claims": ["heritage collection", "gift set"],
            "target_demographic": "40+",
            "estimated_price_range": "200000+",
            "confidence": "high",
        },
        {
            "competitor": "COSRX",
            "product_line": "Propolis Line Extension",
            "expected_launch": "2026-04",
            "category": "moisturizing",
            "key_claims": ["enhanced formula", "sensitive skin"],
            "target_demographic": "20-35",
            "estimated_price_range": "20000-35000",
            "confidence": "medium",
        },
    ]


@tool
def analyze_competitor_strategy(
    competitor_name: str,
) -> dict[str, Any]:
    """
    Analyze a competitor's overall strategy.

    Args:
        competitor_name: Name of competitor to analyze

    Returns:
        Strategy analysis
    """
    strategies = {
        "innisfree": {
            "positioning": "Natural, eco-friendly K-beauty",
            "price_strategy": "Mid-range, frequent promotions",
            "key_channels": ["oliveyoung", "own_stores", "coupang"],
            "promotion_frequency": "high",
            "avg_discount": "20-30%",
            "focus_categories": ["skincare", "suncare", "makeup"],
            "recent_moves": [
                "Increased Coupang presence",
                "Sustainable packaging initiative",
                "Younger demographic targeting",
            ],
            "strengths": ["Brand recognition", "Wide distribution", "Nature-based messaging"],
            "weaknesses": ["Price competition", "Brand fatigue in Korea"],
        },
        "laneige": {
            "positioning": "Premium hydration specialist",
            "price_strategy": "Premium pricing, selective promotions",
            "key_channels": ["department_stores", "oliveyoung", "duty_free"],
            "promotion_frequency": "medium",
            "avg_discount": "15-25%",
            "focus_categories": ["skincare", "lip care"],
            "recent_moves": [
                "Global expansion focus",
                "Celebrity partnerships",
                "Premium line extension",
            ],
            "strengths": ["Strong brand equity", "Hero products", "Global recognition"],
            "weaknesses": ["Limited price flexibility", "Premium positioning limits reach"],
        },
    }

    return strategies.get(
        competitor_name.lower(),
        {"message": f"No detailed analysis available for {competitor_name}"},
    )


class CompetitorWatcher(BaseAgent):
    """
    Competitor Watcher Agent.

    Responsibilities:
    - Track competitor promotions and deals
    - Monitor competitor pricing
    - Identify upcoming launches
    - Analyze competitor strategies
    """

    name = "competitor_watcher"
    role = "Competitive Intelligence Analyst"
    description = "Tracks competitor promotions, pricing, launches, and strategies"
    division = Division.MARKET_INTELLIGENCE

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            get_competitor_promotions,
            get_competitor_pricing,
            get_competitor_launches,
            analyze_competitor_strategy,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Competitor Watcher for Promotor, specializing in K-beauty competitive intelligence.

Your responsibilities:
1. Track competitor promotions across all channels
2. Monitor pricing changes and strategies
3. Identify upcoming product launches
4. Analyze competitor positioning and tactics

Key competitors to monitor:
- Amorepacific brands: Innisfree, Laneige, Sulwhasoo, Etude, Mamonde
- LG H&H brands: The Face Shop, OHUI, su:m37°, CNP
- Independent: COSRX, Some By Mi, Missha, TONYMOLY, Nature Republic

Competitive signals to track:
- Promotion depth and frequency
- New channel partnerships
- Influencer collaborations
- Product launches and reformulations
- Packaging/branding changes

When analyzing:
- Compare against your brand's positioning
- Identify gaps and opportunities
- Flag aggressive competitive moves
- Note timing patterns

Output format:
- Competitor name and action
- Channel and timing
- Strategic implications
- Recommended response

Respond in Korean if the user's query is in Korean."""

    async def get_competitive_snapshot(
        self,
        state: PromotorStateDict,
    ) -> dict[str, Any]:
        """
        Generate a competitive snapshot.

        Args:
            state: Current state

        Returns:
            Competitive intelligence summary
        """
        channels = state.get("active_channels", ["oliveyoung", "coupang", "naver", "kakao"])

        # Get active promotions
        promotions = get_competitor_promotions.invoke({
            "channel": "all",
            "days_back": 7,
        })

        # Get upcoming launches
        launches = get_competitor_launches.invoke({
            "months_ahead": 3,
        })

        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "active_promotions": promotions,
            "upcoming_launches": launches,
            "summary": f"Tracking {len(promotions)} active competitor promotions, {len(launches)} upcoming launches",
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a competitor analysis request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "promotion_tracking",
                "price_monitoring",
                "launch_detection",
                "strategy_analysis",
            ],
        }
