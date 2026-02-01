"""Ingredient Trend Analyst Agent - Formulation and ingredient trend analysis."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def get_trending_ingredients(
    category: str = "all",
    region: str = "korea",
) -> list[dict[str, Any]]:
    """
    Get currently trending ingredients in K-beauty.

    Args:
        category: Product category filter (all, skincare, suncare, haircare)
        region: Region for trend data (korea, global, asia)

    Returns:
        List of trending ingredients with metrics
    """
    ingredients = [
        {
            "name": "Centella Asiatica (CICA)",
            "trend_score": 95,
            "growth_rate": 0.15,
            "category": "skincare",
            "benefits": ["soothing", "barrier repair", "anti-inflammatory"],
            "popular_products": ["COSRX CICA Serum", "Dr. Jart+ Cicapair"],
            "consumer_sentiment": "very positive",
            "lifecycle_stage": "mature",
        },
        {
            "name": "Retinol/Retinal",
            "trend_score": 92,
            "growth_rate": 0.35,
            "category": "skincare",
            "benefits": ["anti-aging", "texture improvement", "collagen boost"],
            "popular_products": ["COSRX Retinol", "Innisfree Retinol Cica"],
            "consumer_sentiment": "positive",
            "lifecycle_stage": "growth",
        },
        {
            "name": "Niacinamide",
            "trend_score": 88,
            "growth_rate": 0.08,
            "category": "skincare",
            "benefits": ["brightening", "pore minimizing", "oil control"],
            "popular_products": ["Some By Mi Niacinamide", "TIAM Niacinamide"],
            "consumer_sentiment": "positive",
            "lifecycle_stage": "mature",
        },
        {
            "name": "Mugwort (Artemisia)",
            "trend_score": 78,
            "growth_rate": 0.25,
            "category": "skincare",
            "benefits": ["soothing", "anti-oxidant", "traditional Korean"],
            "popular_products": ["I'm From Mugwort", "Missha Artemisia"],
            "consumer_sentiment": "positive",
            "lifecycle_stage": "growth",
        },
        {
            "name": "Tranexamic Acid",
            "trend_score": 75,
            "growth_rate": 0.45,
            "category": "skincare",
            "benefits": ["brightening", "hyperpigmentation", "melasma"],
            "popular_products": ["COSRX The TXA", "Some By Mi TXA"],
            "consumer_sentiment": "emerging positive",
            "lifecycle_stage": "emerging",
        },
    ]

    if category != "all":
        ingredients = [i for i in ingredients if i["category"] == category]

    return ingredients


@tool
def get_ingredient_safety_info(
    ingredient_name: str,
) -> dict[str, Any]:
    """
    Get safety and regulatory information for an ingredient.

    Args:
        ingredient_name: Name of the ingredient

    Returns:
        Safety and regulatory information
    """
    safety_data = {
        "retinol": {
            "ingredient": "Retinol",
            "inci_name": "Retinol",
            "ewg_rating": "1-3",
            "korea_regulation": "allowed up to 0.5% in OTC",
            "eu_regulation": "allowed with restrictions",
            "us_regulation": "OTC drug in higher concentrations",
            "concerns": ["photosensitivity", "pregnancy contraindication"],
            "recommended_concentration": "0.1-0.5%",
            "stability_notes": "Light and air sensitive, requires opaque packaging",
        },
        "niacinamide": {
            "ingredient": "Niacinamide",
            "inci_name": "Niacinamide",
            "ewg_rating": "1",
            "korea_regulation": "no restrictions",
            "eu_regulation": "no restrictions",
            "us_regulation": "no restrictions",
            "concerns": ["flushing at very high concentrations"],
            "recommended_concentration": "2-10%",
            "stability_notes": "Stable, compatible with most ingredients",
        },
    }

    return safety_data.get(
        ingredient_name.lower(),
        {"message": f"No safety data available for {ingredient_name}"},
    )


@tool
def analyze_ingredient_combinations(
    ingredients: list[str],
) -> dict[str, Any]:
    """
    Analyze ingredient combinations for compatibility.

    Args:
        ingredients: List of ingredients to analyze

    Returns:
        Compatibility analysis
    """
    # Known incompatibilities
    incompatible_pairs = {
        ("retinol", "vitamin_c"): "pH conflict, may reduce efficacy",
        ("retinol", "aha"): "increased irritation risk",
        ("retinol", "bha"): "increased irritation risk",
        ("vitamin_c", "niacinamide"): "old myth - actually compatible",
        ("aha", "bha"): "over-exfoliation risk if combined",
    }

    # Known synergies
    synergies = {
        ("niacinamide", "hyaluronic_acid"): "complementary hydration",
        ("centella", "niacinamide"): "enhanced barrier repair",
        ("vitamin_c", "vitamin_e"): "enhanced antioxidant protection",
        ("retinol", "peptides"): "complementary anti-aging",
    }

    issues = []
    positive_combinations = []

    ingredients_lower = [i.lower().replace(" ", "_") for i in ingredients]

    for i, ing1 in enumerate(ingredients_lower):
        for ing2 in ingredients_lower[i + 1:]:
            pair = tuple(sorted([ing1, ing2]))
            if pair in incompatible_pairs:
                issues.append({
                    "ingredients": [ing1, ing2],
                    "issue": incompatible_pairs[pair],
                })
            if pair in synergies:
                positive_combinations.append({
                    "ingredients": [ing1, ing2],
                    "benefit": synergies[pair],
                })

    return {
        "ingredients_analyzed": ingredients,
        "compatibility_issues": issues,
        "positive_synergies": positive_combinations,
        "overall_assessment": "compatible" if not issues else "has_concerns",
    }


@tool
def get_ingredient_market_data(
    ingredient_name: str,
) -> dict[str, Any]:
    """
    Get market data for an ingredient.

    Args:
        ingredient_name: Name of the ingredient

    Returns:
        Market data including search volume and product count
    """
    market_data = {
        "retinol": {
            "ingredient": "Retinol",
            "monthly_searches_korea": 245000,
            "search_trend": "increasing",
            "products_on_oliveyoung": 89,
            "avg_price_range": "25000-55000",
            "top_brands": ["COSRX", "Innisfree", "Some By Mi"],
            "market_saturation": "medium-high",
            "opportunity_score": 7.5,
        },
        "centella": {
            "ingredient": "Centella Asiatica",
            "monthly_searches_korea": 180000,
            "search_trend": "stable",
            "products_on_oliveyoung": 156,
            "avg_price_range": "18000-35000",
            "top_brands": ["COSRX", "Dr.Jart+", "Skin1004"],
            "market_saturation": "high",
            "opportunity_score": 5.5,
        },
    }

    return market_data.get(
        ingredient_name.lower(),
        {"message": f"No market data available for {ingredient_name}"},
    )


class IngredientTrendAnalyst(BaseAgent):
    """
    Ingredient Trend Analyst Agent.

    Responsibilities:
    - Track trending ingredients in K-beauty
    - Provide safety and regulatory information
    - Analyze ingredient combinations
    - Assess market opportunities
    """

    name = "ingredient_trend_analyst"
    role = "Formulation Expert"
    description = "Analyzes trending ingredients, safety data, and formulation trends"
    division = Division.MARKET_INTELLIGENCE

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            get_trending_ingredients,
            get_ingredient_safety_info,
            analyze_ingredient_combinations,
            get_ingredient_market_data,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Ingredient Trend Analyst for Promotor, specializing in K-beauty formulation trends.

Your responsibilities:
1. Track trending ingredients and their lifecycle stage
2. Provide safety and regulatory information
3. Analyze ingredient combinations and compatibility
4. Assess market opportunities for ingredients

Key ingredients to monitor:
- Anti-aging: Retinol, Retinal, Peptides, EGF
- Brightening: Vitamin C, Niacinamide, Arbutin, Tranexamic Acid
- Soothing: Centella, Mugwort, Aloe, Panthenol
- Hydrating: Hyaluronic Acid, Ceramides, Squalane
- Exfoliating: AHA, BHA, PHA, Enzymes

Trend lifecycle stages:
1. Emerging - New, growing interest
2. Growth - Rapid adoption
3. Mature - Widespread, saturated
4. Decline - Interest waning

When analyzing:
- Consider consumer education level
- Note regulatory differences by region
- Highlight formulation challenges
- Identify white space opportunities

Output format:
- Ingredient name and trend status
- Benefits and claims
- Market saturation level
- Opportunity assessment

Respond in Korean if the user's query is in Korean."""

    async def get_ingredient_report(
        self,
        state: PromotorStateDict,
        category: str = "skincare",
    ) -> dict[str, Any]:
        """
        Generate an ingredient trend report.

        Args:
            state: Current state
            category: Product category focus

        Returns:
            Comprehensive ingredient report
        """
        # Get trending ingredients
        trends = get_trending_ingredients.invoke({
            "category": category,
            "region": "korea",
        })

        # Categorize by lifecycle
        emerging = [i for i in trends if i["lifecycle_stage"] == "emerging"]
        growth = [i for i in trends if i["lifecycle_stage"] == "growth"]
        mature = [i for i in trends if i["lifecycle_stage"] == "mature"]

        return {
            "category": category,
            "total_tracked": len(trends),
            "by_lifecycle": {
                "emerging": emerging,
                "growth": growth,
                "mature": mature,
            },
            "top_opportunities": [i for i in trends if i.get("growth_rate", 0) > 0.3],
            "summary": f"Tracking {len(trends)} ingredients: {len(emerging)} emerging, {len(growth)} growing, {len(mature)} mature",
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process an ingredient analysis request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "trend_tracking",
                "safety_analysis",
                "combination_check",
                "market_assessment",
            ],
        }
