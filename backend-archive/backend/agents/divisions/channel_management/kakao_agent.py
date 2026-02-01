"""Kakao Agent - Kakao channel specialist."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def get_kakao_gift_rankings(
    category: str,
    age_group: str = "all",
    limit: int = 20,
) -> list[dict[str, Any]]:
    """
    Get KakaoTalk Gift rankings.

    Args:
        category: Product category
        age_group: Target age group (all, 20s, 30s, 40s)
        limit: Number of results

    Returns:
        Gift ranking results
    """
    return [
        {
            "rank": 1,
            "product_name": "설화수 윤조에센스 세트",
            "brand": "Sulwhasoo",
            "price": 185000,
            "gift_wrap": True,
            "message_card": True,
            "category": "premium_skincare",
            "gift_count": 12500,
            "rating": 4.9,
            "popular_occasions": ["birthday", "anniversary", "parents_day"],
        },
        {
            "rank": 2,
            "product_name": "이니스프리 그린티 세트",
            "brand": "Innisfree",
            "price": 45000,
            "gift_wrap": True,
            "message_card": True,
            "category": "skincare",
            "gift_count": 9800,
            "rating": 4.7,
            "popular_occasions": ["birthday", "thank_you"],
        },
        {
            "rank": 3,
            "product_name": "라네즈 립 슬리핑 마스크 세트",
            "brand": "Laneige",
            "price": 32000,
            "gift_wrap": True,
            "message_card": True,
            "category": "lip_care",
            "gift_count": 8500,
            "rating": 4.8,
            "popular_occasions": ["casual", "friend"],
        },
    ][:limit]


@tool
def get_kakao_gift_metrics(
    brand_id: str,
    period: str = "30d",
) -> dict[str, Any]:
    """
    Get KakaoTalk Gift performance metrics.

    Args:
        brand_id: Brand ID
        period: Analysis period

    Returns:
        Gift performance metrics
    """
    return {
        "brand_id": brand_id,
        "period": period,
        "metrics": {
            "total_gifts_sent": 4500,
            "total_gmv": 135_000_000,
            "average_gift_value": 30000,
            "conversion_rate": 0.85,  # Gift sent → claimed
            "claim_rate": 0.92,
        },
        "top_products": [
            {"name": "스킨케어 세트 A", "gifts": 1200, "revenue": 54_000_000},
            {"name": "립케어 기프트", "gifts": 850, "revenue": 25_500_000},
        ],
        "occasion_breakdown": {
            "birthday": 0.35,
            "thank_you": 0.25,
            "anniversary": 0.15,
            "holiday": 0.15,
            "other": 0.10,
        },
        "sender_demographics": {
            "20s": 0.30,
            "30s": 0.40,
            "40s": 0.20,
            "50+": 0.10,
        },
    }


@tool
def get_kakao_channel_metrics(
    channel_id: str,
) -> dict[str, Any]:
    """
    Get Kakao Channel (friend) metrics.

    Args:
        channel_id: Kakao Channel ID

    Returns:
        Channel performance metrics
    """
    return {
        "channel_id": channel_id,
        "friends_count": 125000,
        "friends_growth": {
            "7d": 2500,
            "30d": 8500,
            "growth_rate": 0.07,
        },
        "message_metrics": {
            "last_campaign": {
                "sent": 120000,
                "delivered": 118000,
                "opened": 42000,
                "clicked": 8400,
                "open_rate": 0.356,
                "click_rate": 0.20,
            },
        },
        "blocked_rate": 0.02,
        "active_rate": 0.45,  # Engaged in last 30 days
        "top_content_types": [
            {"type": "promotion", "engagement": 0.25},
            {"type": "new_product", "engagement": 0.22},
            {"type": "tips", "engagement": 0.18},
        ],
    }


@tool
def create_kakao_gift_campaign(
    campaign_name: str,
    products: list[str],
    discount: float,
    start_date: str,
    end_date: str,
    target_occasion: str | None = None,
) -> dict[str, Any]:
    """
    Create a KakaoTalk Gift campaign.

    Args:
        campaign_name: Campaign name
        products: Products to include
        discount: Discount percentage
        start_date: Start date
        end_date: End date
        target_occasion: Target gifting occasion

    Returns:
        Campaign creation status
    """
    return {
        "campaign_id": f"kcamp_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "campaign_name": campaign_name,
        "products": products,
        "discount": discount,
        "period": {"start": start_date, "end": end_date},
        "target_occasion": target_occasion,
        "status": "draft",
        "requirements": [
            {"item": "Product images (gift box)", "status": "required"},
            {"item": "Gift message templates", "status": "required"},
            {"item": "Inventory allocation", "status": "required"},
            {"item": "Pricing approval", "status": "pending"},
        ],
        "estimated_reach": 50000,
        "estimated_gifts": 1500,
    }


@tool
def send_kakao_channel_message(
    channel_id: str,
    message_type: str,
    content: dict[str, Any],
    target_segment: str = "all",
) -> dict[str, Any]:
    """
    Send a Kakao Channel message.

    Args:
        channel_id: Channel ID
        message_type: Message type (text, image, carousel)
        content: Message content
        target_segment: Target segment (all, active, dormant)

    Returns:
        Message send status
    """
    return {
        "message_id": f"msg_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "channel_id": channel_id,
        "message_type": message_type,
        "target_segment": target_segment,
        "estimated_recipients": 112000,
        "status": "scheduled",
        "cost_estimate": 560000,  # 5 won per message
        "scheduled_time": content.get("send_time", "immediate"),
        "preview_url": f"https://preview.kakao.com/msg/{datetime.now().strftime('%Y%m%d%H%M%S')}",
    }


class KakaoAgent(BaseAgent):
    """
    Kakao Agent.

    Responsibilities:
    - Track KakaoTalk Gift rankings
    - Monitor gift performance
    - Manage Kakao Channel
    - Create gift campaigns
    """

    name = "kakao_agent"
    role = "Kakao Specialist"
    description = "Manages KakaoTalk Gift, Kakao Channel, and Kakao commerce"
    division = Division.CHANNEL_MANAGEMENT

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            get_kakao_gift_rankings,
            get_kakao_gift_metrics,
            get_kakao_channel_metrics,
            create_kakao_gift_campaign,
            send_kakao_channel_message,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Kakao Specialist for Promotor, managing all Kakao channel operations.

Your responsibilities:
1. Track KakaoTalk Gift rankings and performance
2. Manage gift campaigns
3. Optimize Kakao Channel engagement
4. Analyze gifting patterns

KakaoTalk Gift strategy:
- Focus on gift-worthy presentation
- Include gift wrap and message card options
- Price points: 20,000-50,000 KRW sweet spot
- Premium gifts perform well during holidays

Key gifting occasions:
- Birthday (연중): Consistent demand
- Parents' Day (5월): Premium products
- Chuseok/Lunar New Year: Gift sets
- Christmas: Limited editions
- Thank You gifts: Mid-range items

Kakao Channel best practices:
- Maintain < 3% block rate
- Optimal message frequency: 2-3/week
- Best send times: 12:00-13:00, 19:00-21:00
- Mix content: promos + tips + new products

Gift optimization:
- High claim rate (>90%) indicates good product-occasion fit
- Track refund rate for quality issues
- Monitor competitor gift pricing
- Create occasion-specific bundles

Fee structure:
- Gift sales: 15-20% commission
- Channel messages: ~5 KRW per message
- Featured placement fees vary

When analyzing:
- Compare vs gift category benchmarks
- Track seasonal patterns
- Monitor claim and refund rates
- Optimize gift presentation

Respond in Korean if the user's query is in Korean."""

    async def get_channel_status(
        self,
        state: PromotorStateDict,
        category: str = "skincare",
    ) -> dict[str, Any]:
        """
        Get comprehensive Kakao channel status.

        Args:
            state: Current state
            category: Product category

        Returns:
            Channel status summary
        """
        brand_id = state.get("brand_id", "default")

        # Get gift rankings
        rankings = get_kakao_gift_rankings.invoke({
            "category": category,
            "limit": 10,
        })

        # Get gift metrics
        gift_metrics = get_kakao_gift_metrics.invoke({
            "brand_id": brand_id,
        })

        # Get channel metrics
        channel_metrics = get_kakao_channel_metrics.invoke({
            "channel_id": brand_id,
        })

        return {
            "channel": "kakao",
            "category": category,
            "gift_rankings": rankings,
            "gift_metrics": gift_metrics,
            "channel_metrics": channel_metrics,
            "summary": f"Friends: {channel_metrics['friends_count']:,}, Gift GMV: {gift_metrics['metrics']['total_gmv']:,}원",
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a Kakao-related request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "channel": "kakao",
            "capabilities": [
                "gift_rankings",
                "gift_campaigns",
                "channel_messaging",
                "occasion_analysis",
            ],
        }
