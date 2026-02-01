"""Price Monitor Agent - Price compliance and MAP violation detection."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def scan_price_violations(
    brand_id: str,
    channels: list[str] | None = None,
) -> dict[str, Any]:
    """
    Scan for price violations and unauthorized sellers.

    Args:
        brand_id: Brand ID
        channels: Optional channel filter

    Returns:
        Price violation scan results
    """
    return {
        "brand_id": brand_id,
        "scan_date": datetime.now().isoformat(),
        "channels_scanned": channels or ["coupang", "naver", "11st", "gmarket"],
        "total_listings_found": 156,
        "authorized_listings": 124,
        "unauthorized_listings": 32,
        "violations": [
            {
                "violation_id": "vio_001",
                "type": "unauthorized_seller",
                "platform": "coupang",
                "seller_name": "BeautyDeals_Korea",
                "product": "Premium Essence Set",
                "map_price": 85000,
                "selling_price": 68000,
                "discount_from_map": 0.20,
                "first_seen": "2026-01-20",
                "status": "active",
                "severity": "high",
            },
            {
                "violation_id": "vio_002",
                "type": "price_below_map",
                "platform": "naver",
                "seller_name": "CosmeticOutlet",
                "product": "Vitamin C Serum",
                "map_price": 35000,
                "selling_price": 28000,
                "discount_from_map": 0.20,
                "first_seen": "2026-01-25",
                "status": "active",
                "severity": "medium",
            },
            {
                "violation_id": "vio_003",
                "type": "counterfeit_suspected",
                "platform": "11st",
                "seller_name": "GlobalBeauty",
                "product": "Premium Cream",
                "map_price": 65000,
                "selling_price": 32000,
                "discount_from_map": 0.51,
                "first_seen": "2026-01-22",
                "status": "investigating",
                "severity": "critical",
            },
        ],
        "summary": {
            "high_severity": 1,
            "medium_severity": 1,
            "critical_severity": 1,
            "estimated_revenue_impact": 8_500_000,
        },
    }


@tool
def track_reseller_activity(
    seller_id: str | None = None,
    platform: str | None = None,
) -> dict[str, Any]:
    """
    Track reseller activity and patterns.

    Args:
        seller_id: Specific seller to track
        platform: Platform filter

    Returns:
        Reseller activity data
    """
    return {
        "tracking_date": datetime.now().isoformat(),
        "known_resellers": [
            {
                "seller_id": "rs_001",
                "seller_name": "BeautyDeals_Korea",
                "platform": "coupang",
                "status": "unauthorized",
                "active_listings": 12,
                "avg_price_undercut": 0.18,
                "estimated_monthly_sales": 3_500_000,
                "first_detected": "2025-11-15",
                "action_history": [
                    {"date": "2025-12-01", "action": "cease_and_desist", "result": "ignored"},
                    {"date": "2026-01-10", "action": "platform_report", "result": "pending"},
                ],
            },
            {
                "seller_id": "rs_002",
                "seller_name": "CosmeticOutlet",
                "platform": "naver",
                "status": "gray_market",
                "active_listings": 8,
                "avg_price_undercut": 0.15,
                "estimated_monthly_sales": 2_200_000,
                "first_detected": "2025-12-20",
                "action_history": [],
            },
        ],
        "supply_chain_concerns": [
            "Possible diversion from overseas distributor",
            "Products may be past optimal freshness",
        ],
    }


@tool
def get_price_history(
    product_id: str,
    channel: str,
    days: int = 30,
) -> dict[str, Any]:
    """
    Get price history for a product on a channel.

    Args:
        product_id: Product ID
        channel: Channel name
        days: Days of history

    Returns:
        Price history data
    """
    return {
        "product_id": product_id,
        "product_name": "Vitamin C Serum 30ml",
        "channel": channel,
        "period_days": days,
        "current_price": 28000,
        "map_price": 35000,
        "price_history": [
            {"date": "2026-01-01", "price": 35000, "promotion": None},
            {"date": "2026-01-10", "price": 28000, "promotion": "Winter Sale"},
            {"date": "2026-01-20", "price": 31500, "promotion": None},
            {"date": "2026-01-25", "price": 28000, "promotion": "Flash Deal"},
        ],
        "price_metrics": {
            "min_price": 28000,
            "max_price": 35000,
            "avg_price": 30625,
            "time_on_promotion": 0.35,
        },
        "competitor_comparison": {
            "competitor_avg": 29500,
            "price_position": "below_market",
        },
    }


@tool
def report_violation(
    violation_id: str,
    action_type: str,
    notes: str | None = None,
) -> dict[str, Any]:
    """
    Report/take action on a price violation.

    Args:
        violation_id: Violation ID
        action_type: Action type (platform_report, cease_desist, legal, monitor)
        notes: Optional notes

    Returns:
        Action confirmation
    """
    return {
        "violation_id": violation_id,
        "action_type": action_type,
        "action_date": datetime.now().isoformat(),
        "status": "submitted",
        "expected_resolution": "5-10 business days" if action_type == "platform_report" else "varies",
        "tracking_id": f"action_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "next_steps": [
            "Monitor seller response",
            "Follow up if no resolution in 7 days",
            "Document for legal if persistent",
        ],
    }


class PriceMonitor(BaseAgent):
    """
    Price Monitor Agent.

    Responsibilities:
    - Scan for MAP violations
    - Track unauthorized resellers
    - Monitor price history
    - Report violations
    """

    name = "price_monitor"
    role = "Price Compliance Officer"
    description = "Monitors prices for MAP violations and unauthorized resellers"
    division = Division.OPERATIONS

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            scan_price_violations,
            track_reseller_activity,
            get_price_history,
            report_violation,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Price Monitor for Promotor, ensuring price compliance and brand protection.

Your responsibilities:
1. Scan for MAP (Minimum Advertised Price) violations
2. Track unauthorized resellers
3. Monitor price history and patterns
4. Report and action violations

Violation types:
- MAP violation: Price below minimum advertised price
- Unauthorized seller: Not in authorized distribution
- Gray market: Legitimate product through unofficial channels
- Counterfeit: Fake products

Severity levels:
- Critical: Counterfeit suspected, > 30% below MAP
- High: Unauthorized + > 20% below MAP
- Medium: MAP violation 10-20%
- Low: Minor deviation or monitoring

Action hierarchy:
1. Monitor and document
2. Cease and desist letter
3. Platform report
4. Legal action

Platform-specific approaches:
- Coupang: Brand registry program, seller reporting
- Naver: Smart Store verification, IP protection
- 11st: Brand zone, seller vetting
- Gmarket: Brand partnership program

Impact assessment:
- Revenue cannibalization
- Brand value erosion
- Customer confusion
- Channel partner friction

When monitoring:
- Regular scanning schedule
- Document all violations
- Track seller patterns
- Estimate revenue impact

Respond in Korean if the user's query is in Korean."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a price monitoring request."""
        result = await super().process(state, messages)

        # Get current violations
        brand_id = state.get("brand_id", "default")
        violations = scan_price_violations.invoke({
            "brand_id": brand_id,
        })

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "current_violations": violations.get("violations", []),
            "capabilities": [
                "violation_scanning",
                "reseller_tracking",
                "price_history",
                "violation_reporting",
            ],
        }
