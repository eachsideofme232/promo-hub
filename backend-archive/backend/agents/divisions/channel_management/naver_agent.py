"""Naver Agent - Naver channel specialist."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def get_naver_shopping_rankings(
    category: str,
    sort_type: str = "popularity",
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    Get Naver Shopping search rankings.

    Args:
        category: Product category
        sort_type: Sort type (popularity, price_low, price_high, review)
        limit: Number of results

    Returns:
        Shopping search results
    """
    return [
        {
            "rank": 1,
            "product_name": "COSRX Advanced Snail 96 Mucin",
            "brand": "COSRX",
            "store_type": "smart_store",
            "price": 13800,
            "original_price": 18000,
            "naver_pay": True,
            "review_count": 58000,
            "rating": 4.9,
            "purchase_count": 125000,
        },
        {
            "rank": 2,
            "product_name": "Anua Heartleaf 77% Soothing Toner",
            "brand": "Anua",
            "store_type": "brand_store",
            "price": 18500,
            "original_price": 25000,
            "naver_pay": True,
            "review_count": 42000,
            "rating": 4.8,
            "purchase_count": 98000,
        },
    ][:limit]


@tool
def get_smart_store_metrics(
    store_id: str,
    period: str = "7d",
) -> dict[str, Any]:
    """
    Get Naver Smart Store analytics.

    Args:
        store_id: Smart Store ID
        period: Analysis period (7d, 30d, 90d)

    Returns:
        Store performance metrics
    """
    return {
        "store_id": store_id,
        "period": period,
        "metrics": {
            "visitors": 45000,
            "page_views": 125000,
            "orders": 2100,
            "gmv": 38_500_000,
            "conversion_rate": 0.047,
            "average_order_value": 18333,
        },
        "traffic_sources": {
            "naver_search": 0.45,
            "naver_shopping": 0.30,
            "direct": 0.12,
            "blog_cafe": 0.08,
            "other": 0.05,
        },
        "top_products": [
            {"name": "Vitamin C Serum", "sales": 8_500_000, "units": 520},
            {"name": "Sunscreen SPF50+", "sales": 7_200_000, "units": 450},
        ],
        "store_grade": "파워",
    }


@tool
def get_shopping_live_schedule(
    store_id: str,
    weeks_ahead: int = 4,
) -> dict[str, Any]:
    """
    Get Naver Shopping Live schedule and slots.

    Args:
        store_id: Store ID
        weeks_ahead: Weeks to look ahead

    Returns:
        Live commerce schedule
    """
    return {
        "store_id": store_id,
        "scheduled_lives": [
            {
                "live_id": "live_001",
                "title": "Spring Skincare Collection",
                "date": "2026-02-10",
                "time": "20:00",
                "duration_minutes": 60,
                "products": ["Toner", "Serum", "Moisturizer"],
                "expected_viewers": 5000,
                "status": "confirmed",
            },
        ],
        "available_slots": [
            {
                "date": "2026-02-17",
                "time_slots": ["19:00", "20:00", "21:00"],
                "slot_type": "regular",
            },
            {
                "date": "2026-02-24",
                "time_slots": ["20:00"],
                "slot_type": "premium",
                "fee": 500_000,
            },
        ],
        "live_performance_history": {
            "average_viewers": 4500,
            "average_gmv": 12_000_000,
            "conversion_rate": 0.085,
        },
    }


@tool
def get_naver_search_ad_performance(
    campaign_id: str | None = None,
) -> dict[str, Any]:
    """
    Get Naver Search Ad performance metrics.

    Args:
        campaign_id: Optional campaign ID

    Returns:
        Search ad performance
    """
    return {
        "period": "Last 7 days",
        "total_spend": 1_800_000,
        "metrics": {
            "impressions": 450000,
            "clicks": 18000,
            "conversions": 720,
            "ctr": 0.04,
            "cvr": 0.04,
            "cpc": 100,
            "cpa": 2500,
            "roas": 3.2,
        },
        "campaigns": [
            {
                "id": "ncamp_001",
                "name": "브랜드 키워드",
                "type": "brand",
                "spend": 500_000,
                "roas": 5.5,
            },
            {
                "id": "ncamp_002",
                "name": "카테고리 타겟팅",
                "type": "category",
                "spend": 800_000,
                "roas": 2.8,
            },
            {
                "id": "ncamp_003",
                "name": "쇼핑검색광고",
                "type": "shopping",
                "spend": 500_000,
                "roas": 3.5,
            },
        ],
        "top_keywords": [
            {"keyword": "선크림 추천", "cpc": 850, "conversions": 125},
            {"keyword": "비타민C 세럼", "cpc": 720, "conversions": 98},
        ],
    }


@tool
def book_shopping_live_slot(
    store_id: str,
    date: str,
    time: str,
    title: str,
    products: list[str],
) -> dict[str, Any]:
    """
    Book a Naver Shopping Live slot.

    Args:
        store_id: Store ID
        date: Date YYYY-MM-DD
        time: Time HH:MM
        title: Live title
        products: Products to feature

    Returns:
        Booking confirmation
    """
    return {
        "booking_id": f"book_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "store_id": store_id,
        "date": date,
        "time": time,
        "title": title,
        "products": products,
        "status": "pending_confirmation",
        "checklist": [
            {"item": "Product registration", "status": "required"},
            {"item": "Live thumbnail", "status": "required"},
            {"item": "Script/outline", "status": "optional"},
            {"item": "Host confirmation", "status": "required"},
        ],
        "deadline": f"{date} 12:00 (day before)",
    }


class NaverAgent(BaseAgent):
    """
    Naver Agent.

    Responsibilities:
    - Track Naver Shopping rankings
    - Monitor Smart Store metrics
    - Manage Shopping Live
    - Optimize search advertising
    """

    name = "naver_agent"
    role = "Naver Specialist"
    description = "Manages Naver Smart Store, Shopping Live, and search advertising"
    division = Division.CHANNEL_MANAGEMENT

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            get_naver_shopping_rankings,
            get_smart_store_metrics,
            get_shopping_live_schedule,
            get_naver_search_ad_performance,
            book_shopping_live_slot,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Naver Specialist for Promotor, managing all Naver channel operations.

Your responsibilities:
1. Track Naver Shopping rankings
2. Monitor Smart Store performance
3. Manage Shopping Live sessions
4. Optimize search advertising

Key Naver platforms:
- Smart Store: Brand's own Naver store
- Brand Store: Premium branded storefront
- Shopping Live: Live commerce
- Search Ads: Keyword advertising

Smart Store metrics to track:
- Visitor count and conversion rate
- Traffic sources (search vs direct)
- Store grade (새싹 → 씨앗 → 파워 → 빅파워 → 프리미엄)
- Review count and rating

Shopping Live best practices:
- Prime time: 19:00-21:00 weekdays
- Optimal duration: 45-60 minutes
- Target conversion: 8-12%
- Engage with chat actively

Search Ad optimization:
- Maintain Quality Index 7+
- Separate brand vs category campaigns
- Monitor CPC vs category average
- Use 쇼핑검색광고 for product visibility

Naver Pay benefits:
- Higher conversion vs non-Naver Pay
- Review incentives
- 네이버페이 포인트 attraction

When analyzing:
- Compare rankings vs competitors
- Track traffic source mix
- Monitor Live performance trends
- Optimize ad spend allocation

Respond in Korean if the user's query is in Korean."""

    async def get_channel_status(
        self,
        state: PromotorStateDict,
        category: str = "스킨케어",
    ) -> dict[str, Any]:
        """
        Get comprehensive Naver channel status.

        Args:
            state: Current state
            category: Product category

        Returns:
            Channel status summary
        """
        brand_id = state.get("brand_id", "default")

        # Get rankings
        rankings = get_naver_shopping_rankings.invoke({
            "category": category,
            "limit": 10,
        })

        # Get store metrics
        metrics = get_smart_store_metrics.invoke({
            "store_id": brand_id,
            "period": "7d",
        })

        # Get Live schedule
        live = get_shopping_live_schedule.invoke({
            "store_id": brand_id,
        })

        # Get ad performance
        ads = get_naver_search_ad_performance.invoke({})

        return {
            "channel": "naver",
            "category": category,
            "shopping_rankings": rankings,
            "store_metrics": metrics,
            "live_schedule": live,
            "ad_performance": ads,
            "summary": f"Store grade: {metrics['store_grade']}, CVR: {metrics['metrics']['conversion_rate']:.1%}",
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a Naver-related request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "channel": "naver",
            "capabilities": [
                "shopping_rankings",
                "smart_store",
                "shopping_live",
                "search_ads",
            ],
        }
