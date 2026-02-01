"""Stockout Predictor Agent - Inventory forecasting and stock-out risk prediction."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def predict_stockout_risk(
    product_id: str,
    days_ahead: int = 30,
) -> dict[str, Any]:
    """
    Predict stock-out risk for a product.

    Args:
        product_id: Product ID
        days_ahead: Days to forecast

    Returns:
        Stock-out risk prediction
    """
    today = datetime.now()

    return {
        "product_id": product_id,
        "product_name": "Vitamin C Serum 30ml",
        "prediction_date": today.strftime("%Y-%m-%d"),
        "forecast_period": f"{days_ahead} days",
        "current_inventory": {
            "total_units": 2850,
            "by_channel": {
                "oliveyoung": 950,
                "coupang": 780,
                "naver": 650,
                "kakao": 470,
            },
        },
        "sales_forecast": {
            "daily_average": 85,
            "weekly_forecast": [595, 612, 628, 645],
            "monthly_forecast": 2550,
        },
        "stockout_prediction": {
            "days_of_supply": 33,
            "stockout_date": (today + timedelta(days=33)).strftime("%Y-%m-%d"),
            "risk_level": "medium",
            "confidence": 0.82,
        },
        "channel_risk": {
            "oliveyoung": {"days_supply": 35, "risk": "low"},
            "coupang": {"days_supply": 28, "risk": "medium"},
            "naver": {"days_supply": 38, "risk": "low"},
            "kakao": {"days_supply": 25, "risk": "high"},
        },
        "recommendation": "Restock Kakao within 10 days, Coupang within 14 days",
    }


@tool
def calculate_reorder_quantity(
    product_id: str,
    lead_time_days: int = 21,
    safety_stock_days: int = 14,
) -> dict[str, Any]:
    """
    Calculate optimal reorder quantity.

    Args:
        product_id: Product ID
        lead_time_days: Production/shipping lead time
        safety_stock_days: Safety stock buffer

    Returns:
        Reorder quantity recommendation
    """
    daily_demand = 85
    demand_variability = 0.15  # 15% standard deviation

    # EOQ components
    annual_demand = daily_demand * 365
    ordering_cost = 500000  # Per order
    holding_cost_rate = 0.20  # 20% of item cost
    unit_cost = 8000

    # EOQ calculation
    eoq = ((2 * annual_demand * ordering_cost) / (holding_cost_rate * unit_cost)) ** 0.5

    # Reorder point
    reorder_point = (daily_demand * lead_time_days) + (daily_demand * safety_stock_days)

    # Safety stock
    safety_stock = int(daily_demand * safety_stock_days * (1 + demand_variability))

    return {
        "product_id": product_id,
        "parameters": {
            "daily_demand": daily_demand,
            "lead_time_days": lead_time_days,
            "safety_stock_days": safety_stock_days,
            "demand_variability": demand_variability,
        },
        "recommendations": {
            "economic_order_quantity": int(eoq),
            "reorder_point": int(reorder_point),
            "safety_stock": safety_stock,
            "maximum_inventory": int(eoq + safety_stock),
        },
        "cost_analysis": {
            "order_frequency": f"{int(annual_demand / eoq)} times/year",
            "average_inventory_value": int((eoq / 2 + safety_stock) * unit_cost),
            "annual_holding_cost": int((eoq / 2 + safety_stock) * unit_cost * holding_cost_rate),
        },
    }


@tool
def simulate_promotion_inventory(
    product_id: str,
    promotion_start: str,
    expected_lift: float = 2.0,
    duration_days: int = 7,
) -> dict[str, Any]:
    """
    Simulate inventory needs for a promotion.

    Args:
        product_id: Product ID
        promotion_start: Promotion start date
        expected_lift: Sales multiplier during promotion
        duration_days: Promotion duration

    Returns:
        Inventory simulation for promotion
    """
    normal_daily_sales = 85
    promo_daily_sales = int(normal_daily_sales * expected_lift)
    total_promo_demand = promo_daily_sales * duration_days

    current_inventory = 2850

    return {
        "product_id": product_id,
        "promotion_period": {
            "start": promotion_start,
            "duration_days": duration_days,
            "expected_lift": expected_lift,
        },
        "demand_projection": {
            "normal_daily": normal_daily_sales,
            "promo_daily": promo_daily_sales,
            "total_promo_demand": total_promo_demand,
            "post_promo_buffer": normal_daily_sales * 14,  # 2 weeks buffer
        },
        "inventory_analysis": {
            "current_inventory": current_inventory,
            "required_inventory": total_promo_demand + (normal_daily_sales * 14),
            "surplus_shortfall": current_inventory - (total_promo_demand + normal_daily_sales * 14),
        },
        "scenarios": {
            "conservative": {
                "lift": 1.5,
                "demand": int(normal_daily_sales * 1.5 * duration_days),
                "status": "sufficient",
            },
            "expected": {
                "lift": 2.0,
                "demand": total_promo_demand,
                "status": "sufficient" if current_inventory > total_promo_demand else "shortfall",
            },
            "aggressive": {
                "lift": 3.0,
                "demand": int(normal_daily_sales * 3.0 * duration_days),
                "status": "shortfall",
            },
        },
        "recommendation": "Current inventory sufficient for expected scenario. Order additional 500 units for safety.",
    }


@tool
def get_inventory_alerts(
    brand_id: str,
    threshold_days: int = 21,
) -> list[dict[str, Any]]:
    """
    Get inventory alerts for products below threshold.

    Args:
        brand_id: Brand ID
        threshold_days: Days of supply threshold for alerts

    Returns:
        List of inventory alerts
    """
    return [
        {
            "product_id": "prod_003",
            "product_name": "Retinol Night Cream",
            "current_inventory": 450,
            "daily_sales": 32,
            "days_of_supply": 14,
            "alert_level": "critical",
            "channels_at_risk": ["oliveyoung", "coupang"],
            "recommended_action": "Urgent restock - 800 units",
        },
        {
            "product_id": "prod_007",
            "product_name": "SPF50 Sunscreen",
            "current_inventory": 680,
            "daily_sales": 38,
            "days_of_supply": 18,
            "alert_level": "warning",
            "channels_at_risk": ["kakao"],
            "recommended_action": "Restock within 7 days - 600 units",
        },
    ]


class StockoutPredictor(BaseAgent):
    """
    Stockout Predictor Agent.

    Responsibilities:
    - Predict stock-out risks
    - Calculate reorder quantities
    - Simulate promotion inventory needs
    - Generate inventory alerts
    """

    name = "stockout_predictor"
    role = "Inventory Forecaster"
    description = "Predicts stock-out risks and optimizes inventory levels"
    division = Division.ANALYTICS

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            predict_stockout_risk,
            calculate_reorder_quantity,
            simulate_promotion_inventory,
            get_inventory_alerts,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Stockout Predictor for Promotor, specializing in inventory forecasting.

Your responsibilities:
1. Predict stock-out risks by product/channel
2. Calculate optimal reorder quantities
3. Simulate inventory for promotions
4. Generate proactive alerts

Forecasting methodology:
- Historical sales analysis
- Seasonal adjustment
- Promotion impact modeling
- Trend extrapolation

Key parameters:
- Lead time: 14-30 days typically
- Safety stock: 14-21 days recommended
- Reorder point: Lead time demand + safety stock

Risk levels:
- Critical: < 14 days supply
- Warning: 14-21 days supply
- Low: > 21 days supply

Promotion inventory planning:
- Typical lift: 1.5-3x normal sales
- Plan for aggressive scenario
- Account for post-promo dip

Channel considerations:
- Each channel has separate inventory
- Rebalancing takes time
- Stockouts hurt search rankings

When predicting:
- Use conservative estimates
- Account for variability
- Consider seasonality
- Flag uncertainty

Respond in Korean if the user's query is in Korean."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a stockout prediction request."""
        result = await super().process(state, messages)

        # Get current alerts
        brand_id = state.get("brand_id", "default")
        alerts = get_inventory_alerts.invoke({
            "brand_id": brand_id,
        })

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "current_alerts": alerts,
            "capabilities": [
                "stockout_prediction",
                "reorder_calculation",
                "promotion_simulation",
                "inventory_alerts",
            ],
        }
