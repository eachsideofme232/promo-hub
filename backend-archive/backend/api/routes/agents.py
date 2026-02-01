"""Agent management endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

from backend.graph.state import Division

router = APIRouter()


class AgentInfo(BaseModel):
    """Agent information model."""

    name: str
    role: str
    description: str
    division: str
    capabilities: list[str]


class DivisionInfo(BaseModel):
    """Division information model."""

    name: str
    description: str
    agents: list[AgentInfo]


@router.get("/")
async def list_agents():
    """List all available agents."""
    return {
        "total_agents": 21,
        "divisions": [
            {
                "name": "Strategic Planning",
                "code": "strategic_planning",
                "agent_count": 3,
                "agents": ["promotion_planner", "timeline_manager", "budget_allocator"],
            },
            {
                "name": "Market Intelligence",
                "code": "market_intelligence",
                "agent_count": 4,
                "agents": [
                    "industry_news_scout",
                    "competitor_watcher",
                    "ingredient_trend_analyst",
                    "seasonal_pattern_analyst",
                ],
            },
            {
                "name": "Channel Management",
                "code": "channel_management",
                "agent_count": 5,
                "agents": [
                    "oliveyoung_agent",
                    "coupang_agent",
                    "naver_agent",
                    "kakao_agent",
                    "cross_channel_syncer",
                ],
            },
            {
                "name": "Analytics",
                "code": "analytics",
                "agent_count": 7,
                "agents": [
                    "review_sentiment_analyst",
                    "promotion_reviewer",
                    "bundle_analyzer",
                    "margin_calculator",
                    "stockout_predictor",
                    "influencer_roi_analyst",
                    "attribution_analyst",
                ],
            },
            {
                "name": "Operations",
                "code": "operations",
                "agent_count": 3,
                "agents": ["inventory_checker", "price_monitor", "checklist_manager"],
            },
        ],
    }


@router.get("/{division}")
async def get_division_agents(division: str):
    """Get agents for a specific division."""
    division_agents = {
        "strategic_planning": {
            "name": "Strategic Planning",
            "description": "Promotion planning, timelines, and budgets",
            "agents": [
                {
                    "name": "promotion_planner",
                    "role": "Promotion Strategy Specialist",
                    "description": "Creates and manages promotion calendars, strategies, and campaigns",
                    "capabilities": [
                        "promotion_calendar",
                        "campaign_strategy",
                        "timing_optimization",
                    ],
                },
                {
                    "name": "timeline_manager",
                    "role": "Schedule Coordinator",
                    "description": "Tracks deadlines, manages milestones, and coordinates schedules",
                    "capabilities": [
                        "milestone_tracking",
                        "lead_time_calculation",
                        "reminder_scheduling",
                    ],
                },
                {
                    "name": "budget_allocator",
                    "role": "Budget Specialist",
                    "description": "Manages budget distribution, ROI projections, and financial optimization",
                    "capabilities": [
                        "budget_allocation",
                        "roi_projection",
                        "scenario_comparison",
                    ],
                },
            ],
        },
        "market_intelligence": {
            "name": "Market Intelligence",
            "description": "News, competitors, ingredients, and seasonal analysis",
            "agents": [
                {
                    "name": "industry_news_scout",
                    "role": "Beauty Industry Reporter",
                    "description": "Aggregates K-beauty news, detects trends, and monitors industry developments",
                    "capabilities": ["news_aggregation", "trend_detection", "social_monitoring"],
                },
                {
                    "name": "competitor_watcher",
                    "role": "Competitive Intelligence Analyst",
                    "description": "Tracks competitor promotions, pricing, launches, and strategies",
                    "capabilities": ["promotion_tracking", "price_monitoring", "strategy_analysis"],
                },
                {
                    "name": "ingredient_trend_analyst",
                    "role": "Formulation Expert",
                    "description": "Analyzes trending ingredients, safety data, and formulation trends",
                    "capabilities": ["trend_tracking", "safety_analysis", "market_assessment"],
                },
                {
                    "name": "seasonal_pattern_analyst",
                    "role": "Demand Forecaster",
                    "description": "Analyzes seasonal patterns, holidays, and forecasts demand",
                    "capabilities": ["seasonal_analysis", "event_calendar", "demand_forecasting"],
                },
            ],
        },
        "channel_management": {
            "name": "Channel Management",
            "description": "E-commerce channel operations",
            "agents": [
                {
                    "name": "oliveyoung_agent",
                    "role": "Oliveyoung Specialist",
                    "description": "Manages Oliveyoung channel operations, rankings, deals, and reviews",
                    "capabilities": ["ranking_tracking", "deal_monitoring", "review_analysis"],
                },
                {
                    "name": "coupang_agent",
                    "role": "Coupang Specialist",
                    "description": "Manages Coupang WING portal, Rocket delivery, and advertising",
                    "capabilities": ["search_ranking", "rocket_delivery", "ad_management"],
                },
                {
                    "name": "naver_agent",
                    "role": "Naver Specialist",
                    "description": "Manages Naver Smart Store, Shopping Live, and search advertising",
                    "capabilities": ["smart_store", "shopping_live", "search_ads"],
                },
                {
                    "name": "kakao_agent",
                    "role": "Kakao Specialist",
                    "description": "Manages KakaoTalk Gift, Kakao Channel, and commerce",
                    "capabilities": ["gift_commerce", "channel_messaging", "occasion_analysis"],
                },
                {
                    "name": "cross_channel_syncer",
                    "role": "Multi-Channel Coordinator",
                    "description": "Ensures consistency and coordination across all channels",
                    "capabilities": ["price_consistency", "inventory_sync", "map_monitoring"],
                },
            ],
        },
        "analytics": {
            "name": "Analytics",
            "description": "Performance analysis and insights",
            "agents": [
                {
                    "name": "review_sentiment_analyst",
                    "role": "Customer Sentiment Expert",
                    "description": "Analyzes customer reviews and sentiment using Korean NLP",
                    "capabilities": ["sentiment_analysis", "theme_extraction", "competitive_comparison"],
                },
                {
                    "name": "promotion_reviewer",
                    "role": "Performance Analyst",
                    "description": "Analyzes promotion performance, calculates lift, and extracts learnings",
                    "capabilities": ["performance_analysis", "lift_calculation", "learning_extraction"],
                },
                {
                    "name": "bundle_analyzer",
                    "role": "Bundle Optimization Expert",
                    "description": "Analyzes purchase patterns and optimizes product bundles",
                    "capabilities": ["pattern_analysis", "bundle_suggestion", "cross_sell_analysis"],
                },
                {
                    "name": "margin_calculator",
                    "role": "Profitability Analyst",
                    "description": "Calculates margins, optimizes discounts, and analyzes profitability",
                    "capabilities": ["margin_calculation", "discount_optimization", "profitability_projection"],
                },
                {
                    "name": "stockout_predictor",
                    "role": "Inventory Forecaster",
                    "description": "Predicts stock-out risks and optimizes inventory levels",
                    "capabilities": ["stockout_prediction", "reorder_calculation", "promotion_simulation"],
                },
                {
                    "name": "influencer_roi_analyst",
                    "role": "Influencer Performance Analyst",
                    "description": "Tracks KOL campaigns, calculates ROI, and optimizes influencer mix",
                    "capabilities": ["campaign_tracking", "roi_calculation", "tier_comparison"],
                },
                {
                    "name": "attribution_analyst",
                    "role": "Marketing Attribution Expert",
                    "description": "Analyzes multi-touch attribution and channel contribution",
                    "capabilities": ["attribution_analysis", "journey_mapping", "efficiency_calculation"],
                },
            ],
        },
        "operations": {
            "name": "Operations",
            "description": "Inventory, pricing, and compliance",
            "agents": [
                {
                    "name": "inventory_checker",
                    "role": "Inventory Monitor",
                    "description": "Monitors real-time inventory levels and generates alerts",
                    "capabilities": ["inventory_monitoring", "alert_generation", "threshold_management"],
                },
                {
                    "name": "price_monitor",
                    "role": "Price Compliance Officer",
                    "description": "Monitors prices for MAP violations and unauthorized resellers",
                    "capabilities": ["violation_scanning", "reseller_tracking", "violation_reporting"],
                },
                {
                    "name": "checklist_manager",
                    "role": "Compliance Officer",
                    "description": "Manages pre-launch checklists and compliance verification",
                    "capabilities": ["checklist_management", "compliance_monitoring", "automated_validation"],
                },
            ],
        },
    }

    if division not in division_agents:
        return {"error": f"Division '{division}' not found"}

    return division_agents[division]


@router.get("/{division}/{agent_name}")
async def get_agent_details(division: str, agent_name: str):
    """Get detailed information about a specific agent."""
    # Would fetch from agent registry
    return {
        "name": agent_name,
        "division": division,
        "status": "active",
        "last_invoked": None,
        "total_invocations": 0,
    }
