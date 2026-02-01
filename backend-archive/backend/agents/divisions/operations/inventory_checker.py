"""Inventory Checker Agent - Real-time inventory monitoring and alerts."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def get_inventory_status(
    brand_id: str,
    channel: str | None = None,
) -> dict[str, Any]:
    """
    Get current inventory status across channels.

    Args:
        brand_id: Brand ID
        channel: Optional channel filter

    Returns:
        Inventory status summary
    """
    return {
        "brand_id": brand_id,
        "checked_at": datetime.now().isoformat(),
        "total_sku_count": 45,
        "inventory_summary": {
            "total_units": 125000,
            "total_value": 2_875_000_000,
            "healthy": 32,
            "low_stock": 8,
            "critical": 3,
            "out_of_stock": 2,
        },
        "by_channel": {
            "oliveyoung": {
                "total_units": 42000,
                "healthy": 35,
                "low_stock": 6,
                "critical": 2,
                "out_of_stock": 2,
            },
            "coupang": {
                "total_units": 38000,
                "healthy": 33,
                "low_stock": 8,
                "critical": 3,
                "out_of_stock": 1,
            },
            "naver": {
                "total_units": 28000,
                "healthy": 38,
                "low_stock": 5,
                "critical": 2,
                "out_of_stock": 0,
            },
            "kakao": {
                "total_units": 17000,
                "healthy": 40,
                "low_stock": 3,
                "critical": 1,
                "out_of_stock": 1,
            },
        },
    }


@tool
def get_inventory_alerts(
    brand_id: str,
    severity: str = "all",
) -> list[dict[str, Any]]:
    """
    Get inventory alerts.

    Args:
        brand_id: Brand ID
        severity: Filter by severity (all, critical, warning)

    Returns:
        List of inventory alerts
    """
    alerts = [
        {
            "alert_id": "inv_alert_001",
            "severity": "critical",
            "product_id": "prod_003",
            "product_name": "Retinol Night Cream 50ml",
            "channel": "oliveyoung",
            "current_stock": 45,
            "days_of_supply": 3,
            "daily_sales_avg": 15,
            "message": "Critical stock level - stockout imminent",
            "action_required": "Emergency restock",
            "created_at": datetime.now().isoformat(),
        },
        {
            "alert_id": "inv_alert_002",
            "severity": "critical",
            "product_id": "prod_007",
            "product_name": "SPF50 Sunscreen",
            "channel": "coupang",
            "current_stock": 120,
            "days_of_supply": 5,
            "daily_sales_avg": 24,
            "message": "Critical stock level during peak season",
            "action_required": "Urgent restock for Rocket delivery",
            "created_at": datetime.now().isoformat(),
        },
        {
            "alert_id": "inv_alert_003",
            "severity": "warning",
            "product_id": "prod_012",
            "product_name": "Vitamin C Serum 30ml",
            "channel": "kakao",
            "current_stock": 280,
            "days_of_supply": 12,
            "daily_sales_avg": 23,
            "message": "Low stock warning",
            "action_required": "Plan restock within 7 days",
            "created_at": datetime.now().isoformat(),
        },
    ]

    if severity != "all":
        alerts = [a for a in alerts if a["severity"] == severity]

    return alerts


@tool
def check_product_inventory(
    product_id: str,
) -> dict[str, Any]:
    """
    Check detailed inventory for a specific product.

    Args:
        product_id: Product ID

    Returns:
        Detailed product inventory
    """
    return {
        "product_id": product_id,
        "product_name": "Vitamin C Serum 30ml",
        "sku": "VCS-30ML-001",
        "checked_at": datetime.now().isoformat(),
        "total_inventory": 2850,
        "by_location": {
            "warehouse": 1200,
            "oliveyoung_consignment": 650,
            "coupang_fba": 520,
            "naver_fulfillment": 280,
            "kakao_stock": 200,
        },
        "by_channel_available": {
            "oliveyoung": {"available": 650, "reserved": 45, "incoming": 300},
            "coupang": {"available": 520, "reserved": 30, "incoming": 250},
            "naver": {"available": 280, "reserved": 15, "incoming": 0},
            "kakao": {"available": 200, "reserved": 8, "incoming": 0},
        },
        "metrics": {
            "days_of_supply": 34,
            "daily_sales_avg": 84,
            "weekly_sales_trend": "increasing",
            "reorder_point": 1500,
            "safety_stock": 750,
        },
        "incoming_shipments": [
            {"date": "2026-02-05", "quantity": 550, "status": "in_transit"},
        ],
    }


@tool
def update_inventory_threshold(
    product_id: str,
    channel: str,
    threshold_type: str,
    value: int,
) -> dict[str, Any]:
    """
    Update inventory alert threshold.

    Args:
        product_id: Product ID
        channel: Channel
        threshold_type: Type (critical, warning, reorder)
        value: New threshold value

    Returns:
        Updated threshold confirmation
    """
    return {
        "product_id": product_id,
        "channel": channel,
        "threshold_type": threshold_type,
        "previous_value": 100,
        "new_value": value,
        "updated_at": datetime.now().isoformat(),
        "status": "success",
    }


class InventoryChecker(BaseAgent):
    """
    Inventory Checker Agent.

    Responsibilities:
    - Monitor real-time inventory levels
    - Generate inventory alerts
    - Check product-specific inventory
    - Manage alert thresholds
    """

    name = "inventory_checker"
    role = "Inventory Monitor"
    description = "Monitors real-time inventory levels and generates alerts"
    division = Division.OPERATIONS

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            get_inventory_status,
            get_inventory_alerts,
            check_product_inventory,
            update_inventory_threshold,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Inventory Checker for Promotor, monitoring real-time inventory levels.

Your responsibilities:
1. Monitor inventory levels across all channels
2. Generate timely alerts for low stock
3. Provide detailed product inventory status
4. Manage alert thresholds

Inventory status levels:
- Healthy: > 21 days supply
- Low stock: 14-21 days supply
- Critical: 7-14 days supply
- Out of stock: < 7 days or zero

Channel-specific considerations:
- Oliveyoung: Consignment stock, weekly replenishment
- Coupang: FBA inventory, Rocket requires minimum levels
- Naver: Fulfillment center stock
- Kakao: Direct ship capability

Key metrics to monitor:
- Days of supply (DOS)
- Daily sales average
- Reorder point
- Safety stock level
- Incoming shipments

Alert priority:
- Critical: Immediate action needed (< 7 days)
- Warning: Plan restock (7-14 days)
- Info: Monitor (14-21 days)

When checking:
- Consider seasonal demand variations
- Account for lead times
- Flag channel-specific risks
- Note promotion impacts

Respond in Korean if the user's query is in Korean."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process an inventory check request."""
        result = await super().process(state, messages)

        # Get current alerts
        brand_id = state.get("brand_id", "default")
        alerts = get_inventory_alerts.invoke({
            "brand_id": brand_id,
            "severity": "all",
        })

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "current_alerts": alerts,
            "capabilities": [
                "inventory_monitoring",
                "alert_generation",
                "product_status",
                "threshold_management",
            ],
        }
