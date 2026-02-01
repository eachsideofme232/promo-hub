"""Seasonal Pattern Analyst Agent - Demand forecasting and timing analysis."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def get_seasonal_demand_patterns(
    product_category: str,
    year: int = 2026,
) -> dict[str, Any]:
    """
    Get seasonal demand patterns for a product category.

    Args:
        product_category: Category to analyze
        year: Year for pattern data

    Returns:
        Seasonal demand patterns
    """
    patterns = {
        "sunscreen": {
            "category": "sunscreen",
            "peak_months": [4, 5, 6, 7, 8],
            "low_months": [11, 12, 1, 2],
            "demand_index": {
                1: 45, 2: 55, 3: 75, 4: 95, 5: 100, 6: 98,
                7: 95, 8: 85, 9: 70, 10: 55, 11: 40, 12: 35,
            },
            "yoy_growth": 0.12,
            "key_events": [
                {"month": 4, "event": "Spring vacation", "impact": "high"},
                {"month": 5, "event": "Pre-summer prep", "impact": "very_high"},
                {"month": 7, "event": "Summer vacation peak", "impact": "high"},
            ],
        },
        "moisturizer": {
            "category": "moisturizer",
            "peak_months": [10, 11, 12, 1, 2],
            "low_months": [6, 7, 8],
            "demand_index": {
                1: 95, 2: 90, 3: 75, 4: 65, 5: 55, 6: 50,
                7: 50, 8: 55, 9: 70, 10: 90, 11: 100, 12: 98,
            },
            "yoy_growth": 0.08,
            "key_events": [
                {"month": 10, "event": "Fall dryness", "impact": "high"},
                {"month": 12, "event": "Winter/Gift season", "impact": "very_high"},
            ],
        },
        "serum": {
            "category": "serum",
            "peak_months": [3, 4, 9, 10],
            "low_months": [7, 8],
            "demand_index": {
                1: 80, 2: 85, 3: 95, 4: 100, 5: 85, 6: 75,
                7: 70, 8: 72, 9: 92, 10: 98, 11: 88, 12: 85,
            },
            "yoy_growth": 0.15,
            "key_events": [
                {"month": 3, "event": "Spring skincare reset", "impact": "high"},
                {"month": 9, "event": "Fall skincare transition", "impact": "high"},
            ],
        },
    }

    return patterns.get(
        product_category.lower(),
        {"message": f"No pattern data for {product_category}"},
    )


@tool
def get_holiday_calendar(
    year: int = 2026,
    region: str = "korea",
) -> list[dict[str, Any]]:
    """
    Get major shopping holidays and events.

    Args:
        year: Year for calendar
        region: Region (korea, global)

    Returns:
        List of shopping events with promotion recommendations
    """
    return [
        {
            "date": "2026-01-29",
            "event": "Lunar New Year",
            "region": "korea",
            "importance": "very_high",
            "promotion_window": {"start": "2026-01-15", "end": "2026-01-28"},
            "categories": ["gift_sets", "luxury", "skincare"],
            "notes": "Major gifting season, premium products perform well",
        },
        {
            "date": "2026-05-08",
            "event": "Parents' Day",
            "region": "korea",
            "importance": "high",
            "promotion_window": {"start": "2026-04-25", "end": "2026-05-07"},
            "categories": ["anti-aging", "gift_sets", "premium"],
            "notes": "Gifts for parents, anti-aging focus",
        },
        {
            "date": "2026-09-28",
            "event": "Chuseok",
            "region": "korea",
            "importance": "very_high",
            "promotion_window": {"start": "2026-09-14", "end": "2026-09-27"},
            "categories": ["gift_sets", "premium", "traditional"],
            "notes": "Second major gifting season, family gatherings",
        },
        {
            "date": "2026-11-11",
            "event": "Singles' Day (11.11)",
            "region": "korea",
            "importance": "high",
            "promotion_window": {"start": "2026-11-01", "end": "2026-11-11"},
            "categories": ["all", "self_care", "value_sets"],
            "notes": "Major shopping event, deep discounts expected",
        },
        {
            "date": "2026-11-27",
            "event": "Black Friday",
            "region": "global",
            "importance": "medium",
            "promotion_window": {"start": "2026-11-20", "end": "2026-11-30"},
            "categories": ["all"],
            "notes": "Growing importance in Korea, online focus",
        },
        {
            "date": "2026-12-25",
            "event": "Christmas/Year End",
            "region": "global",
            "importance": "high",
            "promotion_window": {"start": "2026-12-01", "end": "2026-12-31"},
            "categories": ["gift_sets", "limited_edition", "makeup"],
            "notes": "Holiday collections, limited editions",
        },
    ]


@tool
def get_channel_event_calendar(
    channel: str,
    quarter: str,
) -> list[dict[str, Any]]:
    """
    Get channel-specific promotional events.

    Args:
        channel: Channel name
        quarter: Quarter (Q1, Q2, Q3, Q4)

    Returns:
        Channel events for the quarter
    """
    events = {
        ("oliveyoung", "Q2"): [
            {
                "event": "Oliveyoung Festa",
                "date_range": "2026-04-20 to 2026-04-26",
                "type": "mega_sale",
                "discount_level": "20-50%",
                "application_deadline": "2026-03-25",
                "requirements": ["inventory commitment", "exclusive deals preferred"],
            },
            {
                "event": "Summer Beauty Fair",
                "date_range": "2026-05-15 to 2026-05-31",
                "type": "category_promotion",
                "discount_level": "15-30%",
                "application_deadline": "2026-04-15",
                "requirements": ["suncare/summer products focus"],
            },
        ],
        ("coupang", "Q2"): [
            {
                "event": "Coupang Wow Week",
                "date_range": "2026-05-01 to 2026-05-07",
                "type": "mega_sale",
                "discount_level": "20-40%",
                "application_deadline": "2026-04-01",
                "requirements": ["Rocket delivery stock", "competitive pricing"],
            },
        ],
        ("naver", "Q2"): [
            {
                "event": "Naver Shopping Live Festival",
                "date_range": "2026-04-10 to 2026-04-20",
                "type": "live_commerce",
                "discount_level": "15-25%",
                "application_deadline": "2026-03-15",
                "requirements": ["live streaming commitment", "exclusive deals"],
            },
        ],
    }

    return events.get((channel.lower(), quarter), [])


@tool
def forecast_demand(
    product_category: str,
    channel: str,
    months_ahead: int = 3,
) -> dict[str, Any]:
    """
    Forecast demand for upcoming period.

    Args:
        product_category: Category to forecast
        channel: Channel for forecast
        months_ahead: Months to forecast

    Returns:
        Demand forecast with confidence intervals
    """
    # Mock forecast - would use Prophet/ML in production
    import datetime

    base_demand = 1000  # units per month

    forecasts = []
    current_month = datetime.datetime.now().month

    for i in range(months_ahead):
        month = (current_month + i) % 12 + 1

        # Seasonal adjustments
        seasonality = {
            "sunscreen": {
                1: 0.45, 2: 0.55, 3: 0.75, 4: 0.95, 5: 1.0, 6: 0.98,
                7: 0.95, 8: 0.85, 9: 0.7, 10: 0.55, 11: 0.4, 12: 0.35,
            },
        }

        factor = seasonality.get(product_category.lower(), {}).get(month, 0.7)
        forecast_value = int(base_demand * factor)

        forecasts.append({
            "month": month,
            "predicted_demand": forecast_value,
            "confidence_low": int(forecast_value * 0.85),
            "confidence_high": int(forecast_value * 1.15),
            "confidence_level": 0.9,
        })

    return {
        "product_category": product_category,
        "channel": channel,
        "forecast_period": f"Next {months_ahead} months",
        "monthly_forecasts": forecasts,
        "trend": "seasonal" if product_category.lower() == "sunscreen" else "stable",
    }


class SeasonalPatternAnalyst(BaseAgent):
    """
    Seasonal Pattern Analyst Agent.

    Responsibilities:
    - Analyze seasonal demand patterns
    - Track shopping holidays and events
    - Monitor channel promotional calendars
    - Forecast demand
    """

    name = "seasonal_pattern_analyst"
    role = "Demand Forecaster"
    description = "Analyzes seasonal patterns, holidays, and forecasts demand"
    division = Division.MARKET_INTELLIGENCE

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            get_seasonal_demand_patterns,
            get_holiday_calendar,
            get_channel_event_calendar,
            forecast_demand,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Seasonal Pattern Analyst for Promotor, specializing in K-beauty demand forecasting.

Your responsibilities:
1. Analyze seasonal demand patterns by category
2. Track major shopping holidays and events
3. Monitor channel-specific promotional calendars
4. Forecast demand for planning purposes

Key seasonal patterns in K-beauty:
- Suncare: Peak May-August, trough November-February
- Moisturizers: Peak October-February (dry winter)
- Gift sets: Peak around Lunar New Year, Chuseok, Christmas
- Makeup: Steady with peaks during fashion seasons

Major Korean shopping events:
- Lunar New Year (Jan/Feb): Premium gifting
- Parents' Day (May 8): Anti-aging focus
- Chuseok (Sep/Oct): Traditional gifting
- 11.11 Singles' Day: Major discounts
- Year-end: Holiday collections

Channel events to track:
- Oliveyoung Festa (quarterly)
- Coupang Wow Week
- Naver Shopping Live Festival
- Kakao Gift Season promotions

When forecasting:
- Consider YoY growth trends
- Account for economic conditions
- Note new product launches impact
- Factor in promotional calendar

Output format:
- Demand index by month (100 = peak)
- Key events with dates
- Confidence levels for forecasts
- Recommended actions

Respond in Korean if the user's query is in Korean."""

    async def get_quarterly_outlook(
        self,
        state: PromotorStateDict,
        quarter: str,
        category: str = "all",
    ) -> dict[str, Any]:
        """
        Generate a quarterly outlook.

        Args:
            state: Current state
            quarter: Quarter to analyze
            category: Product category focus

        Returns:
            Quarterly outlook with events and forecasts
        """
        channels = state.get("active_channels", ["oliveyoung", "coupang", "naver", "kakao"])

        # Get holiday calendar
        holidays = get_holiday_calendar.invoke({"year": 2026})

        # Get channel events
        channel_events = {}
        for channel in channels:
            events = get_channel_event_calendar.invoke({
                "channel": channel,
                "quarter": quarter,
            })
            if events:
                channel_events[channel] = events

        # Get demand patterns if specific category
        patterns = None
        if category != "all":
            patterns = get_seasonal_demand_patterns.invoke({
                "product_category": category,
            })

        return {
            "quarter": quarter,
            "category": category,
            "holidays": [h for h in holidays if quarter in h.get("promotion_window", {}).get("start", "")[:7]],
            "channel_events": channel_events,
            "demand_patterns": patterns,
            "summary": f"{quarter} outlook: {len(channel_events)} channel events tracked",
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a seasonal analysis request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "seasonal_analysis",
                "holiday_tracking",
                "event_calendar",
                "demand_forecasting",
            ],
        }
