"""Budget Allocator Agent - Budget distribution and ROI projection."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def allocate_budget(
    total_budget: float,
    channels: list[str],
    allocation_strategy: str = "balanced",
) -> dict[str, Any]:
    """
    Allocate budget across channels.

    Args:
        total_budget: Total budget in KRW
        channels: List of channels to allocate to
        allocation_strategy: Strategy (balanced, performance_based, growth_focused)

    Returns:
        Budget allocation per channel
    """
    strategies = {
        "balanced": {
            "oliveyoung": 0.30,
            "coupang": 0.30,
            "naver": 0.25,
            "kakao": 0.15,
        },
        "performance_based": {
            "oliveyoung": 0.35,
            "coupang": 0.35,
            "naver": 0.20,
            "kakao": 0.10,
        },
        "growth_focused": {
            "oliveyoung": 0.25,
            "coupang": 0.25,
            "naver": 0.30,
            "kakao": 0.20,
        },
    }

    weights = strategies.get(allocation_strategy, strategies["balanced"])

    allocations = {}
    for channel in channels:
        if channel in weights:
            allocations[channel] = {
                "amount": total_budget * weights[channel],
                "percentage": weights[channel] * 100,
                "breakdown": {
                    "advertising": total_budget * weights[channel] * 0.4,
                    "discounts": total_budget * weights[channel] * 0.35,
                    "influencer": total_budget * weights[channel] * 0.15,
                    "creative": total_budget * weights[channel] * 0.10,
                },
            }

    return {
        "total_budget": total_budget,
        "strategy": allocation_strategy,
        "allocations": allocations,
    }


@tool
def calculate_roi_projection(
    budget: float,
    channel: str,
    promotion_type: str,
    historical_roas: float | None = None,
) -> dict[str, Any]:
    """
    Calculate projected ROI for a promotion.

    Args:
        budget: Budget amount in KRW
        channel: Target channel
        promotion_type: Type of promotion (flash_sale, bundle, campaign)
        historical_roas: Historical ROAS if available

    Returns:
        ROI projection with scenarios
    """
    # Base ROAS estimates by channel and promotion type
    base_roas = {
        ("oliveyoung", "flash_sale"): 3.5,
        ("oliveyoung", "bundle"): 2.8,
        ("oliveyoung", "campaign"): 2.5,
        ("coupang", "flash_sale"): 4.0,
        ("coupang", "bundle"): 3.2,
        ("coupang", "campaign"): 2.8,
        ("naver", "flash_sale"): 3.0,
        ("naver", "bundle"): 2.5,
        ("naver", "campaign"): 2.2,
        ("kakao", "flash_sale"): 2.5,
        ("kakao", "bundle"): 2.0,
        ("kakao", "campaign"): 1.8,
    }

    estimated_roas = historical_roas or base_roas.get((channel, promotion_type), 2.5)

    return {
        "budget": budget,
        "channel": channel,
        "promotion_type": promotion_type,
        "scenarios": {
            "pessimistic": {
                "roas": estimated_roas * 0.7,
                "projected_revenue": budget * estimated_roas * 0.7,
                "net_return": budget * (estimated_roas * 0.7 - 1),
            },
            "expected": {
                "roas": estimated_roas,
                "projected_revenue": budget * estimated_roas,
                "net_return": budget * (estimated_roas - 1),
            },
            "optimistic": {
                "roas": estimated_roas * 1.3,
                "projected_revenue": budget * estimated_roas * 1.3,
                "net_return": budget * (estimated_roas * 1.3 - 1),
            },
        },
        "break_even_roas": 1.0,
        "recommendation": "proceed" if estimated_roas > 2.0 else "review",
    }


@tool
def get_budget_utilization(
    brand_id: str,
    period: str,
) -> dict[str, Any]:
    """
    Get current budget utilization status.

    Args:
        brand_id: Brand identifier
        period: Period (Q1, Q2, monthly, etc.)

    Returns:
        Budget utilization summary
    """
    # Mock data - would query database in production
    return {
        "brand_id": brand_id,
        "period": period,
        "total_budget": 100_000_000,  # 100M KRW
        "spent": 45_000_000,
        "committed": 25_000_000,
        "available": 30_000_000,
        "utilization_rate": 0.70,
        "by_channel": {
            "oliveyoung": {"budget": 30_000_000, "spent": 18_000_000},
            "coupang": {"budget": 30_000_000, "spent": 15_000_000},
            "naver": {"budget": 25_000_000, "spent": 8_000_000},
            "kakao": {"budget": 15_000_000, "spent": 4_000_000},
        },
        "by_category": {
            "advertising": {"budget": 40_000_000, "spent": 20_000_000},
            "discounts": {"budget": 35_000_000, "spent": 15_000_000},
            "influencer": {"budget": 15_000_000, "spent": 7_000_000},
            "creative": {"budget": 10_000_000, "spent": 3_000_000},
        },
    }


@tool
def compare_budget_scenarios(
    scenarios: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Compare different budget allocation scenarios.

    Args:
        scenarios: List of scenarios with name, allocations, and expected outcomes

    Returns:
        Comparison analysis
    """
    if not scenarios:
        return {"error": "No scenarios provided"}

    comparison = {
        "scenarios": scenarios,
        "metrics": {
            "total_projected_revenue": [],
            "total_roi": [],
            "risk_level": [],
        },
    }

    for scenario in scenarios:
        # Calculate metrics for each scenario
        total_revenue = sum(
            alloc.get("projected_revenue", 0)
            for alloc in scenario.get("allocations", {}).values()
        )
        total_budget = sum(
            alloc.get("amount", 0)
            for alloc in scenario.get("allocations", {}).values()
        )

        comparison["metrics"]["total_projected_revenue"].append({
            "scenario": scenario.get("name", "Unknown"),
            "value": total_revenue,
        })
        comparison["metrics"]["total_roi"].append({
            "scenario": scenario.get("name", "Unknown"),
            "value": total_revenue / total_budget if total_budget > 0 else 0,
        })

    return comparison


class BudgetAllocator(BaseAgent):
    """
    Budget Allocator Agent.

    Responsibilities:
    - Budget distribution across channels
    - ROI projection and analysis
    - Budget utilization tracking
    - Scenario comparison and optimization
    """

    name = "budget_allocator"
    role = "Budget Specialist"
    description = "Manages budget distribution, ROI projections, and financial optimization"
    division = Division.STRATEGIC_PLANNING

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            allocate_budget,
            calculate_roi_projection,
            get_budget_utilization,
            compare_budget_scenarios,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Budget Allocator for Promotor, specializing in beauty brand promotion budget management.

Your responsibilities:
1. Distribute budgets across channels optimally
2. Project ROI for promotion investments
3. Track budget utilization
4. Compare and optimize budget scenarios

Key budget considerations for K-beauty:
- Oliveyoung: Higher traffic, lower margins (25-30% fees)
- Coupang: Best ROAS typically, but competitive
- Naver: Good for brand building, moderate ROAS
- Kakao: Lowest volume but high gift market potential

Budget allocation best practices:
- Reserve 10-15% contingency for opportunities
- Allocate 40% to proven performers
- Use 20-30% for testing new channels/tactics
- Track spending velocity vs. timeline

ROI benchmarks by promotion type:
- Flash sales: 3-5x ROAS expected
- Bundle deals: 2.5-3.5x ROAS expected
- Brand campaigns: 1.5-2.5x ROAS (brand value impact)
- Influencer: 2-4x ROAS (varies widely)

When recommending allocations:
- Consider historical performance
- Account for seasonality
- Balance short-term ROI vs. growth
- Flag high-risk allocations

Output format:
- Clear budget tables with KRW amounts
- Percentage breakdowns
- ROI projections with scenarios
- Risk indicators

Respond in Korean if the user's query is in Korean."""

    async def create_budget_plan(
        self,
        state: PromotorStateDict,
        total_budget: float,
        strategy: str = "balanced",
    ) -> dict[str, Any]:
        """
        Create a comprehensive budget plan.

        Args:
            state: Current state
            total_budget: Total budget amount
            strategy: Allocation strategy

        Returns:
            Complete budget plan with projections
        """
        channels = state.get("active_channels", ["oliveyoung", "coupang", "naver", "kakao"])

        # Allocate budget
        allocation = allocate_budget.invoke({
            "total_budget": total_budget,
            "channels": channels,
            "allocation_strategy": strategy,
        })

        # Calculate ROI projections for each channel
        projections = {}
        for channel in channels:
            projection = calculate_roi_projection.invoke({
                "budget": allocation["allocations"].get(channel, {}).get("amount", 0),
                "channel": channel,
                "promotion_type": "campaign",
            })
            projections[channel] = projection

        # Calculate totals
        total_expected_revenue = sum(
            p["scenarios"]["expected"]["projected_revenue"]
            for p in projections.values()
        )

        return {
            "total_budget": total_budget,
            "strategy": strategy,
            "allocation": allocation,
            "projections": projections,
            "summary": {
                "total_expected_revenue": total_expected_revenue,
                "expected_roas": total_expected_revenue / total_budget if total_budget > 0 else 0,
                "channels_count": len(channels),
            },
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a budget allocation request."""
        result = await super().process(state, messages)

        # Add current utilization context
        brand_id = state.get("brand_id", "default")
        utilization = get_budget_utilization.invoke({
            "brand_id": brand_id,
            "period": "Q2",
        })

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "current_utilization": utilization,
            "capabilities": [
                "budget_allocation",
                "roi_projection",
                "utilization_tracking",
                "scenario_comparison",
            ],
        }
