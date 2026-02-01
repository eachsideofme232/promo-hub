"""Cross Channel Syncer Agent - Multi-channel coordination and consistency."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def check_price_consistency(
    product_id: str,
    channels: list[str] | None = None,
) -> dict[str, Any]:
    """
    Check price consistency across channels.

    Args:
        product_id: Product ID to check
        channels: Channels to check (None for all)

    Returns:
        Price comparison across channels
    """
    channels = channels or ["oliveyoung", "coupang", "naver", "kakao"]

    price_data = {
        "product_id": product_id,
        "product_name": "Vitamin C Serum 30ml",
        "checked_at": datetime.now().isoformat(),
        "prices": {
            "oliveyoung": {
                "regular_price": 35000,
                "sale_price": 28000,
                "discount": "20%",
                "in_stock": True,
            },
            "coupang": {
                "regular_price": 35000,
                "sale_price": 26500,  # Lower!
                "discount": "24%",
                "in_stock": True,
            },
            "naver": {
                "regular_price": 35000,
                "sale_price": 28000,
                "discount": "20%",
                "in_stock": True,
            },
            "kakao": {
                "regular_price": 35000,
                "sale_price": 29000,
                "discount": "17%",
                "in_stock": True,
            },
        },
    }

    # Check for inconsistencies
    prices = [v["sale_price"] for v in price_data["prices"].values()]
    min_price = min(prices)
    max_price = max(prices)
    variance = (max_price - min_price) / min_price

    price_data["analysis"] = {
        "min_price": min_price,
        "max_price": max_price,
        "price_variance": variance,
        "is_consistent": variance < 0.05,  # Within 5%
        "lowest_channel": min(price_data["prices"], key=lambda x: price_data["prices"][x]["sale_price"]),
        "highest_channel": max(price_data["prices"], key=lambda x: price_data["prices"][x]["sale_price"]),
    }

    if variance >= 0.05:
        price_data["alert"] = f"Price variance {variance:.1%} exceeds 5% threshold"

    return price_data


@tool
def generate_cross_channel_report(
    brand_id: str,
    period: str = "7d",
) -> dict[str, Any]:
    """
    Generate cross-channel performance report.

    Args:
        brand_id: Brand ID
        period: Report period

    Returns:
        Cross-channel performance comparison
    """
    return {
        "brand_id": brand_id,
        "period": period,
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_gmv": 285_000_000,
            "total_orders": 15200,
            "total_units": 28500,
        },
        "by_channel": {
            "oliveyoung": {
                "gmv": 95_000_000,
                "gmv_share": 0.333,
                "orders": 5200,
                "aov": 18269,
                "growth_wow": 0.08,
                "margin": 0.18,
            },
            "coupang": {
                "gmv": 85_000_000,
                "gmv_share": 0.298,
                "orders": 5800,
                "aov": 14655,
                "growth_wow": 0.12,
                "margin": 0.22,
            },
            "naver": {
                "gmv": 65_000_000,
                "gmv_share": 0.228,
                "orders": 3200,
                "aov": 20312,
                "growth_wow": 0.05,
                "margin": 0.25,
            },
            "kakao": {
                "gmv": 40_000_000,
                "gmv_share": 0.140,
                "orders": 1000,
                "aov": 40000,
                "growth_wow": 0.15,
                "margin": 0.20,
            },
        },
        "insights": [
            "Coupang showing strongest growth (+12% WoW)",
            "Kakao has highest AOV (₩40,000) - gift purchases",
            "Naver has best margin (25%)",
            "Oliveyoung remains largest channel by GMV",
        ],
    }


@tool
def sync_inventory_status(
    product_ids: list[str],
) -> dict[str, Any]:
    """
    Sync and compare inventory across channels.

    Args:
        product_ids: Products to check

    Returns:
        Inventory status across channels
    """
    return {
        "checked_at": datetime.now().isoformat(),
        "products": [
            {
                "product_id": "prod_001",
                "product_name": "Vitamin C Serum",
                "inventory": {
                    "oliveyoung": {"status": "in_stock", "units": 850},
                    "coupang": {"status": "low_stock", "units": 120, "alert": True},
                    "naver": {"status": "in_stock", "units": 650},
                    "kakao": {"status": "in_stock", "units": 400},
                },
                "total_units": 2020,
                "reorder_point": 500,
                "recommendation": "Restock Coupang within 3 days",
            },
            {
                "product_id": "prod_002",
                "product_name": "Sunscreen SPF50+",
                "inventory": {
                    "oliveyoung": {"status": "in_stock", "units": 1200},
                    "coupang": {"status": "in_stock", "units": 980},
                    "naver": {"status": "in_stock", "units": 750},
                    "kakao": {"status": "out_of_stock", "units": 0, "alert": True},
                },
                "total_units": 2930,
                "reorder_point": 600,
                "recommendation": "Replenish Kakao inventory urgently",
            },
        ],
        "alerts": [
            {"product": "Vitamin C Serum", "channel": "coupang", "severity": "medium"},
            {"product": "Sunscreen SPF50+", "channel": "kakao", "severity": "high"},
        ],
    }


@tool
def detect_map_violations(
    brand_id: str,
) -> dict[str, Any]:
    """
    Detect Minimum Advertised Price (MAP) violations.

    Args:
        brand_id: Brand ID

    Returns:
        MAP violation report
    """
    return {
        "brand_id": brand_id,
        "checked_at": datetime.now().isoformat(),
        "violations": [
            {
                "product": "Premium Essence Set",
                "map_price": 85000,
                "violated_price": 68000,
                "violation_percentage": 0.20,
                "channel": "unauthorized_seller",
                "seller_name": "BeautyDeals_Korea",
                "platform": "coupang",
                "first_detected": "2026-01-25",
                "status": "active",
            },
        ],
        "summary": {
            "total_violations": 1,
            "by_severity": {"high": 1, "medium": 0, "low": 0},
            "estimated_revenue_impact": 2_500_000,
        },
        "recommended_actions": [
            "Issue cease and desist to unauthorized seller",
            "Report to Coupang seller support",
            "Review authorized seller agreements",
        ],
    }


@tool
def create_channel_sync_task(
    task_type: str,
    products: list[str],
    channels: list[str],
    target_value: Any,
) -> dict[str, Any]:
    """
    Create a task to sync across channels.

    Args:
        task_type: Type of sync (price, inventory, content)
        products: Products to sync
        channels: Channels to sync
        target_value: Target value to sync to

    Returns:
        Sync task status
    """
    return {
        "task_id": f"sync_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "task_type": task_type,
        "products": products,
        "channels": channels,
        "target_value": target_value,
        "status": "created",
        "steps": [
            {"channel": ch, "status": "pending"} for ch in channels
        ],
        "estimated_completion": "2-4 hours",
        "requires_approval": task_type == "price",
    }


class CrossChannelSyncer(BaseAgent):
    """
    Cross Channel Syncer Agent.

    Responsibilities:
    - Ensure price consistency across channels
    - Generate cross-channel reports
    - Sync inventory status
    - Detect MAP violations
    - Coordinate multi-channel activities
    """

    name = "cross_channel_syncer"
    role = "Multi-Channel Coordinator"
    description = "Ensures consistency and coordination across all e-commerce channels"
    division = Division.CHANNEL_MANAGEMENT

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            check_price_consistency,
            generate_cross_channel_report,
            sync_inventory_status,
            detect_map_violations,
            create_channel_sync_task,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Cross Channel Syncer for Promotor, ensuring consistency across all e-commerce channels.

Your responsibilities:
1. Monitor and maintain price consistency
2. Generate cross-channel performance reports
3. Sync inventory across channels
4. Detect MAP violations and unauthorized sellers
5. Coordinate multi-channel activities

Price consistency rules:
- Maintain within 5% variance across channels
- Account for channel-specific fees
- Flag significant deviations
- Consider promotional periods

Inventory synchronization:
- Monitor stock levels per channel
- Flag low stock alerts (< reorder point)
- Identify out-of-stock risks
- Recommend redistribution

MAP (Minimum Advertised Price) monitoring:
- Track unauthorized sellers
- Report violations by severity
- Estimate revenue impact
- Recommend enforcement actions

Cross-channel metrics:
- GMV share by channel
- AOV comparison
- Margin by channel
- Growth rates

When coordinating:
- Balance channel priorities
- Consider channel-specific promotions
- Maintain brand consistency
- Optimize overall margin

Alert thresholds:
- Price variance > 5%: Warning
- Price variance > 10%: Critical
- Stock < reorder point: Warning
- Stock < 7 days supply: Critical

Respond in Korean if the user's query is in Korean."""

    async def get_channel_overview(
        self,
        state: PromotorStateDict,
    ) -> dict[str, Any]:
        """
        Get comprehensive cross-channel overview.

        Args:
            state: Current state

        Returns:
            Cross-channel overview
        """
        brand_id = state.get("brand_id", "default")

        # Get cross-channel report
        report = generate_cross_channel_report.invoke({
            "brand_id": brand_id,
            "period": "7d",
        })

        # Check for MAP violations
        violations = detect_map_violations.invoke({
            "brand_id": brand_id,
        })

        return {
            "brand_id": brand_id,
            "cross_channel_report": report,
            "map_violations": violations,
            "summary": f"Total GMV: {report['summary']['total_gmv']:,}원 across {len(report['by_channel'])} channels",
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a cross-channel coordination request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "price_consistency",
                "cross_channel_reporting",
                "inventory_sync",
                "map_monitoring",
                "channel_coordination",
            ],
        }
