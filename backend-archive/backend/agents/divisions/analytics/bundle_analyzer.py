"""Bundle Analyzer Agent - Product bundle optimization and cross-sell analysis."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def analyze_purchase_patterns(
    brand_id: str,
    period: str = "90d",
) -> dict[str, Any]:
    """
    Analyze customer purchase patterns for bundling opportunities.

    Args:
        brand_id: Brand ID
        period: Analysis period

    Returns:
        Purchase pattern analysis
    """
    return {
        "brand_id": brand_id,
        "period": period,
        "total_orders": 45000,
        "multi_product_orders": 18500,
        "multi_product_rate": 0.41,
        "average_items_per_order": 1.8,
        "frequent_combinations": [
            {
                "products": ["Toner", "Serum"],
                "frequency": 2850,
                "lift": 2.4,
                "confidence": 0.72,
            },
            {
                "products": ["Cleanser", "Toner", "Moisturizer"],
                "frequency": 1950,
                "lift": 3.1,
                "confidence": 0.65,
            },
            {
                "products": ["Sunscreen", "Moisturizer"],
                "frequency": 1680,
                "lift": 1.8,
                "confidence": 0.58,
            },
            {
                "products": ["Serum", "Eye Cream"],
                "frequency": 1420,
                "lift": 2.2,
                "confidence": 0.61,
            },
        ],
    }


@tool
def suggest_bundles(
    brand_id: str,
    target_price_range: tuple[int, int] | None = None,
) -> list[dict[str, Any]]:
    """
    Suggest optimal product bundles.

    Args:
        brand_id: Brand ID
        target_price_range: Optional price range filter

    Returns:
        Bundle suggestions with projected performance
    """
    return [
        {
            "bundle_id": "bundle_001",
            "name": "Complete Skincare Routine",
            "products": [
                {"name": "Gentle Cleanser", "individual_price": 22000},
                {"name": "Hydrating Toner", "individual_price": 25000},
                {"name": "Vitamin C Serum", "individual_price": 35000},
                {"name": "Daily Moisturizer", "individual_price": 28000},
            ],
            "total_individual": 110000,
            "suggested_bundle_price": 88000,
            "discount_rate": 0.20,
            "projected_metrics": {
                "monthly_sales": 450,
                "margin": 0.25,
                "aov_lift": 1.45,
            },
            "rationale": "Based on top purchase combination, targets new customers",
        },
        {
            "bundle_id": "bundle_002",
            "name": "Anti-Aging Duo",
            "products": [
                {"name": "Retinol Serum", "individual_price": 45000},
                {"name": "Peptide Eye Cream", "individual_price": 38000},
            ],
            "total_individual": 83000,
            "suggested_bundle_price": 69000,
            "discount_rate": 0.17,
            "projected_metrics": {
                "monthly_sales": 280,
                "margin": 0.28,
                "aov_lift": 1.32,
            },
            "rationale": "High affinity products, premium segment",
        },
        {
            "bundle_id": "bundle_003",
            "name": "Sun Protection Set",
            "products": [
                {"name": "Daily Sunscreen SPF50", "individual_price": 28000},
                {"name": "Sun Stick SPF50", "individual_price": 18000},
            ],
            "total_individual": 46000,
            "suggested_bundle_price": 39000,
            "discount_rate": 0.15,
            "projected_metrics": {
                "monthly_sales": 620,
                "margin": 0.22,
                "aov_lift": 1.18,
            },
            "rationale": "Seasonal relevance (summer), complementary use cases",
        },
    ]


@tool
def analyze_bundle_performance(
    bundle_id: str,
) -> dict[str, Any]:
    """
    Analyze performance of an existing bundle.

    Args:
        bundle_id: Bundle ID to analyze

    Returns:
        Bundle performance analysis
    """
    return {
        "bundle_id": bundle_id,
        "bundle_name": "Complete Skincare Routine",
        "period": "Last 30 days",
        "metrics": {
            "units_sold": 425,
            "revenue": 37_400_000,
            "margin": 0.24,
            "aov_contribution": 88000,
        },
        "customer_metrics": {
            "new_customer_rate": 0.35,
            "repeat_rate": 0.18,
            "satisfaction_score": 4.5,
        },
        "channel_breakdown": {
            "oliveyoung": {"units": 180, "share": 0.42},
            "coupang": {"units": 145, "share": 0.34},
            "naver": {"units": 100, "share": 0.24},
        },
        "vs_individual_purchase": {
            "bundle_rate": 0.38,  # 38% choose bundle vs individual
            "margin_impact": -0.02,  # Slight margin decrease
            "volume_impact": 0.45,  # 45% volume increase
        },
        "recommendation": "Optimize - consider reducing discount to 18%",
    }


@tool
def calculate_cross_sell_opportunity(
    product_id: str,
) -> dict[str, Any]:
    """
    Calculate cross-sell opportunities for a product.

    Args:
        product_id: Product ID

    Returns:
        Cross-sell analysis
    """
    return {
        "product_id": product_id,
        "product_name": "Vitamin C Serum",
        "current_attach_rate": 0.28,  # % of buyers also buy another product
        "cross_sell_opportunities": [
            {
                "product": "Niacinamide Toner",
                "affinity_score": 0.72,
                "current_attach": 0.12,
                "potential_attach": 0.25,
                "incremental_revenue": 8_500_000,
                "recommended_offer": "10% off when bought together",
            },
            {
                "product": "SPF Moisturizer",
                "affinity_score": 0.65,
                "current_attach": 0.08,
                "potential_attach": 0.18,
                "incremental_revenue": 5_200_000,
                "recommended_offer": "Free sample with purchase",
            },
            {
                "product": "Gentle Cleanser",
                "affinity_score": 0.58,
                "current_attach": 0.15,
                "potential_attach": 0.22,
                "incremental_revenue": 3_800_000,
                "recommended_offer": "Bundle discount",
            },
        ],
        "total_potential_revenue": 17_500_000,
    }


class BundleAnalyzer(BaseAgent):
    """
    Bundle Analyzer Agent.

    Responsibilities:
    - Analyze purchase patterns
    - Suggest optimal bundles
    - Evaluate bundle performance
    - Identify cross-sell opportunities
    """

    name = "bundle_analyzer"
    role = "Bundle Optimization Expert"
    description = "Analyzes purchase patterns and optimizes product bundles"
    division = Division.ANALYTICS

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            analyze_purchase_patterns,
            suggest_bundles,
            analyze_bundle_performance,
            calculate_cross_sell_opportunity,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Bundle Analyzer for Promotor, specializing in product bundle optimization.

Your responsibilities:
1. Analyze purchase patterns and affinities
2. Suggest optimal product bundles
3. Evaluate bundle performance
4. Identify cross-sell opportunities

Bundle strategy principles:
- Complementary products (routine-based)
- Price tier matching
- Seasonal relevance
- Margin preservation

Key metrics:
- Lift: How much more likely products are bought together vs random
- Confidence: % of A buyers who also buy B
- Attach rate: Cross-sell success rate
- AOV impact: Bundle effect on order value

Bundle types:
- Starter kits: Entry-level, trial sizes
- Routine sets: Complete regimen
- Seasonal: Holiday, weather-specific
- Gift sets: Premium packaging

Pricing guidelines:
- 15-25% bundle discount is typical
- Maintain 20%+ margin
- Price below psychological thresholds
- Consider channel fees

When suggesting bundles:
- Base on actual purchase data
- Consider inventory levels
- Account for seasonality
- Project realistic sales

Respond in Korean if the user's query is in Korean."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a bundle analysis request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "pattern_analysis",
                "bundle_suggestion",
                "performance_tracking",
                "cross_sell_analysis",
            ],
        }
