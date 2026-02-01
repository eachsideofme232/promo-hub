"""Margin Calculator Agent - Profitability analysis and discount optimization."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def calculate_product_margin(
    product_id: str,
    channel: str,
    discount_percentage: float = 0,
) -> dict[str, Any]:
    """
    Calculate product margin by channel.

    Args:
        product_id: Product ID
        channel: Channel name
        discount_percentage: Applied discount

    Returns:
        Margin calculation breakdown
    """
    # Base product economics
    base_price = 35000
    cogs = 8000

    # Channel fees
    channel_fees = {
        "oliveyoung": {"commission": 0.30, "marketing_fee": 0.05},
        "coupang": {"commission": 0.25, "marketing_fee": 0.03},
        "naver": {"commission": 0.15, "marketing_fee": 0.05},
        "kakao": {"commission": 0.18, "marketing_fee": 0.02},
    }

    fees = channel_fees.get(channel, {"commission": 0.20, "marketing_fee": 0.03})

    # Calculate
    selling_price = base_price * (1 - discount_percentage)
    commission = selling_price * fees["commission"]
    marketing = selling_price * fees["marketing_fee"]
    net_revenue = selling_price - commission - marketing
    gross_margin = net_revenue - cogs
    margin_percentage = gross_margin / selling_price if selling_price > 0 else 0

    return {
        "product_id": product_id,
        "channel": channel,
        "discount_applied": discount_percentage,
        "breakdown": {
            "base_price": base_price,
            "selling_price": selling_price,
            "cogs": cogs,
            "commission": commission,
            "marketing_fee": marketing,
            "net_revenue": net_revenue,
            "gross_margin": gross_margin,
        },
        "margin_percentage": margin_percentage,
        "is_profitable": margin_percentage > 0.15,
    }


@tool
def find_optimal_discount(
    product_id: str,
    channel: str,
    target_margin: float = 0.20,
) -> dict[str, Any]:
    """
    Find optimal discount level for target margin.

    Args:
        product_id: Product ID
        channel: Channel name
        target_margin: Target margin percentage

    Returns:
        Optimal discount analysis
    """
    # Simulate different discount levels
    discounts = [0, 0.10, 0.15, 0.20, 0.25, 0.30]
    results = []

    for disc in discounts:
        margin_calc = calculate_product_margin.invoke({
            "product_id": product_id,
            "channel": channel,
            "discount_percentage": disc,
        })
        results.append({
            "discount": disc,
            "margin": margin_calc["margin_percentage"],
            "selling_price": margin_calc["breakdown"]["selling_price"],
            "gross_margin": margin_calc["breakdown"]["gross_margin"],
        })

    # Find optimal
    optimal = None
    for r in results:
        if r["margin"] >= target_margin:
            optimal = r
        else:
            break

    return {
        "product_id": product_id,
        "channel": channel,
        "target_margin": target_margin,
        "analysis": results,
        "optimal_discount": optimal["discount"] if optimal else 0,
        "recommendation": f"Maximum discount for {target_margin:.0%} margin: {optimal['discount']:.0%}" if optimal else "Cannot achieve target margin",
    }


@tool
def compare_channel_margins(
    product_id: str,
    discount_percentage: float = 0.20,
) -> dict[str, Any]:
    """
    Compare margins across channels.

    Args:
        product_id: Product ID
        discount_percentage: Discount to apply

    Returns:
        Channel margin comparison
    """
    channels = ["oliveyoung", "coupang", "naver", "kakao"]
    comparisons = []

    for channel in channels:
        margin = calculate_product_margin.invoke({
            "product_id": product_id,
            "channel": channel,
            "discount_percentage": discount_percentage,
        })
        comparisons.append({
            "channel": channel,
            "margin_percentage": margin["margin_percentage"],
            "gross_margin": margin["breakdown"]["gross_margin"],
            "is_profitable": margin["is_profitable"],
        })

    # Sort by margin
    comparisons.sort(key=lambda x: x["margin_percentage"], reverse=True)

    return {
        "product_id": product_id,
        "discount_applied": discount_percentage,
        "channel_comparison": comparisons,
        "best_margin_channel": comparisons[0]["channel"],
        "worst_margin_channel": comparisons[-1]["channel"],
        "margin_spread": comparisons[0]["margin_percentage"] - comparisons[-1]["margin_percentage"],
    }


@tool
def calculate_promotion_profitability(
    promotion_config: dict[str, Any],
) -> dict[str, Any]:
    """
    Calculate overall promotion profitability.

    Args:
        promotion_config: Promotion configuration with products, channels, discounts

    Returns:
        Profitability projection
    """
    # Example config: {"products": [...], "channels": [...], "discount": 0.20, "budget": 5000000}

    projected_units = 2500
    projected_revenue = 75_000_000
    projected_cogs = 20_000_000
    channel_fees = 18_750_000  # 25% average
    marketing_spend = promotion_config.get("budget", 5_000_000)

    gross_profit = projected_revenue - projected_cogs - channel_fees
    net_profit = gross_profit - marketing_spend
    roi = (net_profit / marketing_spend) if marketing_spend > 0 else 0

    return {
        "projection": {
            "units": projected_units,
            "revenue": projected_revenue,
            "cogs": projected_cogs,
            "channel_fees": channel_fees,
            "marketing_spend": marketing_spend,
            "gross_profit": gross_profit,
            "net_profit": net_profit,
        },
        "metrics": {
            "gross_margin": gross_profit / projected_revenue,
            "net_margin": net_profit / projected_revenue,
            "marketing_roi": roi,
            "breakeven_units": int(marketing_spend / (30000 - 8000 - 7500)),  # Simplified
        },
        "recommendation": "Proceed" if roi > 2.0 else "Review budget or discount",
    }


class MarginCalculator(BaseAgent):
    """
    Margin Calculator Agent.

    Responsibilities:
    - Calculate product margins by channel
    - Find optimal discount levels
    - Compare channel profitability
    - Project promotion profitability
    """

    name = "margin_calculator"
    role = "Profitability Analyst"
    description = "Calculates margins, optimizes discounts, and analyzes profitability"
    division = Division.ANALYTICS

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            calculate_product_margin,
            find_optimal_discount,
            compare_channel_margins,
            calculate_promotion_profitability,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Margin Calculator for Promotor, specializing in profitability analysis.

Your responsibilities:
1. Calculate product margins by channel
2. Find optimal discount levels
3. Compare channel profitability
4. Project promotion profitability

Channel fee structure:
- Oliveyoung: 25-35% commission + 3-5% marketing
- Coupang: 20-30% commission + 2-5% marketing
- Naver: 10-20% commission + 3-7% marketing
- Kakao: 15-20% commission + 2-4% marketing

Margin targets:
- Minimum acceptable: 15%
- Target: 20-25%
- Premium products: 25-35%

Discount impact awareness:
- Each 5% discount reduces margin significantly
- Channel fees are on discounted price
- COGS is fixed regardless of price

When calculating:
- Include all channel fees
- Account for payment processing
- Consider marketing spend
- Factor in returns/refunds (2-5%)

Profitability signals:
- Gross margin < 15%: Warning
- Net margin < 10%: Critical
- ROI < 2.0x: Review needed

Output format:
- Clear margin breakdowns
- Channel comparisons
- Optimal discount recommendations
- Profitability projections

Respond in Korean if the user's query is in Korean."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a margin calculation request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "margin_calculation",
                "discount_optimization",
                "channel_comparison",
                "profitability_projection",
            ],
        }
