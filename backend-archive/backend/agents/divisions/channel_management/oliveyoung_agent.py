"""Oliveyoung Agent - Oliveyoung channel specialist."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def get_oliveyoung_rankings(
    category: str,
    ranking_type: str = "sales",
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    Get Oliveyoung product rankings.

    Args:
        category: Product category
        ranking_type: Type of ranking (sales, review, wish)
        limit: Number of products to return

    Returns:
        List of ranked products
    """
    # Mock data - would scrape Oliveyoung in production
    return [
        {
            "rank": 1,
            "product_name": "Round Lab Dokdo Toner",
            "brand": "Round Lab",
            "price": 18500,
            "original_price": 23000,
            "discount": "20%",
            "rating": 4.8,
            "review_count": 45230,
            "category": category,
        },
        {
            "rank": 2,
            "product_name": "COSRX Advanced Snail 96 Mucin",
            "brand": "COSRX",
            "price": 14000,
            "original_price": 18000,
            "discount": "22%",
            "rating": 4.9,
            "review_count": 38450,
            "category": category,
        },
        {
            "rank": 3,
            "product_name": "Anua Heartleaf Pore Control Cleansing Oil",
            "brand": "Anua",
            "price": 19800,
            "original_price": 25000,
            "discount": "21%",
            "rating": 4.7,
            "review_count": 28900,
            "category": category,
        },
    ][:limit]


@tool
def get_oliveyoung_deals(
    category: str | None = None,
    deal_type: str = "all",
) -> list[dict[str, Any]]:
    """
    Get current Oliveyoung deals and promotions.

    Args:
        category: Optional category filter
        deal_type: Type of deal (all, 1plus1, bundle, flash)

    Returns:
        List of active deals
    """
    today = datetime.now()
    return [
        {
            "deal_id": "deal_001",
            "deal_type": "1plus1",
            "brand": "Some By Mi",
            "products": ["AHA BHA PHA Toner"],
            "discount": "50%",
            "valid_until": "2026-02-15",
            "terms": "While stocks last",
        },
        {
            "deal_id": "deal_002",
            "deal_type": "bundle",
            "brand": "Dr.Jart+",
            "products": ["Cicapair Cream", "Cicapair Serum"],
            "discount": "30%",
            "valid_until": "2026-02-10",
            "terms": "Set purchase only",
        },
        {
            "deal_id": "deal_003",
            "deal_type": "flash",
            "brand": "Torriden",
            "products": ["Dive-In Serum"],
            "discount": "40%",
            "valid_until": "2026-02-02",
            "terms": "Online only, 11AM-2PM",
        },
    ]


@tool
def get_oliveyoung_product_reviews(
    product_id: str,
    limit: int = 50,
    sort_by: str = "recent",
) -> dict[str, Any]:
    """
    Get product reviews from Oliveyoung.

    Args:
        product_id: Product ID
        limit: Number of reviews to fetch
        sort_by: Sort order (recent, helpful, rating_high, rating_low)

    Returns:
        Reviews with sentiment analysis
    """
    return {
        "product_id": product_id,
        "total_reviews": 1250,
        "average_rating": 4.6,
        "rating_distribution": {
            "5": 720,
            "4": 380,
            "3": 100,
            "2": 35,
            "1": 15,
        },
        "sentiment_summary": {
            "positive": 0.78,
            "neutral": 0.15,
            "negative": 0.07,
        },
        "top_keywords": [
            {"keyword": "순함", "count": 320, "sentiment": "positive"},
            {"keyword": "촉촉", "count": 280, "sentiment": "positive"},
            {"keyword": "가성비", "count": 195, "sentiment": "positive"},
            {"keyword": "흡수", "count": 150, "sentiment": "neutral"},
        ],
        "sample_reviews": [
            {
                "rating": 5,
                "content": "피부가 민감한데 자극없이 잘 맞아요!",
                "date": "2026-01-28",
                "helpful_count": 45,
            },
        ],
    }


@tool
def check_oliveyoung_inventory(
    product_ids: list[str],
) -> dict[str, Any]:
    """
    Check inventory status on Oliveyoung.

    Args:
        product_ids: List of product IDs to check

    Returns:
        Inventory status per product
    """
    return {
        "checked_at": datetime.now().isoformat(),
        "products": [
            {
                "product_id": "prod_001",
                "status": "in_stock",
                "estimated_stock": "high",
                "delivery_type": "normal",
            },
            {
                "product_id": "prod_002",
                "status": "low_stock",
                "estimated_stock": "low",
                "delivery_type": "normal",
                "alert": "May sell out within 7 days",
            },
        ],
    }


@tool
def apply_oliveyoung_deal_slot(
    deal_type: str,
    products: list[str],
    start_date: str,
    end_date: str,
    discount: float,
) -> dict[str, Any]:
    """
    Apply for an Oliveyoung deal slot.

    Args:
        deal_type: Type of deal (1plus1, bundle, flash, festa)
        products: List of product names
        start_date: Start date YYYY-MM-DD
        end_date: End date YYYY-MM-DD
        discount: Discount percentage

    Returns:
        Application status
    """
    return {
        "application_id": f"app_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "deal_type": deal_type,
        "products": products,
        "period": {"start": start_date, "end": end_date},
        "discount": discount,
        "status": "submitted",
        "expected_review_date": "Within 5 business days",
        "requirements_checklist": [
            {"item": "Inventory commitment", "status": "pending"},
            {"item": "Marketing fee payment", "status": "pending"},
            {"item": "Creative assets", "status": "pending"},
        ],
    }


class OliveyoungAgent(BaseAgent):
    """
    Oliveyoung Agent.

    Responsibilities:
    - Track Oliveyoung rankings and deals
    - Monitor reviews and sentiment
    - Check inventory status
    - Apply for deal slots
    """

    name = "oliveyoung_agent"
    role = "Oliveyoung Specialist"
    description = "Manages Oliveyoung channel operations, rankings, deals, and reviews"
    division = Division.CHANNEL_MANAGEMENT

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            get_oliveyoung_rankings,
            get_oliveyoung_deals,
            get_oliveyoung_product_reviews,
            check_oliveyoung_inventory,
            apply_oliveyoung_deal_slot,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Oliveyoung Specialist for Promotor, managing all Oliveyoung channel operations.

Your responsibilities:
1. Track category and product rankings
2. Monitor active deals and promotions
3. Analyze product reviews and sentiment
4. Check inventory status
5. Apply for deal slots and promotions

Key Oliveyoung metrics to track:
- Category rankings (Sales, Reviews, Wishes)
- Deal performance by type (1+1, Bundle, Flash)
- Review sentiment and keywords
- Inventory levels and sellout risk

Deal types on Oliveyoung:
- 1+1: Buy one get one free
- Bundle: Set discounts
- Flash Sale: Time-limited deals
- Festa: Major promotional events (quarterly)
- Brand Day: Brand-specific promotions

Fee structure awareness:
- Standard commission: 25-35%
- Deal slot fees vary by prominence
- Marketing contribution requirements

Application timelines:
- Regular deals: 2-3 weeks lead time
- Festa events: 6+ weeks lead time
- Brand Day: 4+ weeks lead time

When analyzing:
- Compare against category benchmarks
- Note ranking movements
- Flag review concerns
- Recommend deal opportunities

Respond in Korean if the user's query is in Korean."""

    async def get_channel_status(
        self,
        state: PromotorStateDict,
        category: str = "skincare",
    ) -> dict[str, Any]:
        """
        Get comprehensive Oliveyoung channel status.

        Args:
            state: Current state
            category: Product category

        Returns:
            Channel status summary
        """
        # Get rankings
        rankings = get_oliveyoung_rankings.invoke({
            "category": category,
            "ranking_type": "sales",
            "limit": 10,
        })

        # Get deals
        deals = get_oliveyoung_deals.invoke({
            "category": category,
        })

        return {
            "channel": "oliveyoung",
            "category": category,
            "rankings_snapshot": rankings,
            "active_deals": deals,
            "summary": f"Top 10 rankings and {len(deals)} active deals tracked",
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process an Oliveyoung-related request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "channel": "oliveyoung",
            "capabilities": [
                "ranking_tracking",
                "deal_monitoring",
                "review_analysis",
                "inventory_check",
                "deal_application",
            ],
        }
