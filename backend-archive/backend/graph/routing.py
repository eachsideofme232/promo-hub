"""Routing logic for directing requests to appropriate divisions and agents."""

from __future__ import annotations

import re
from typing import Any

from backend.graph.state import Division, PromotorStateDict, TaskType


# Keywords for task classification
TASK_KEYWORDS = {
    TaskType.PROMOTION_PLANNING: [
        "plan", "planning", "calendar", "schedule", "campaign", "q1", "q2", "q3", "q4",
        "quarterly", "monthly", "weekly", "annual", "프로모션", "계획", "캠페인"
    ],
    TaskType.TIMELINE_MANAGEMENT: [
        "timeline", "deadline", "milestone", "due", "when", "reminder", "일정", "마감"
    ],
    TaskType.BUDGET_ALLOCATION: [
        "budget", "cost", "spend", "allocate", "roi", "예산", "비용", "배분"
    ],
    TaskType.NEWS_SCOUTING: [
        "news", "trend", "industry", "뉴스", "트렌드", "업계"
    ],
    TaskType.COMPETITOR_ANALYSIS: [
        "competitor", "competition", "innisfree", "laneige", "etude", "경쟁사", "경쟁"
    ],
    TaskType.INGREDIENT_TRENDS: [
        "ingredient", "centella", "retinol", "niacinamide", "vitamin", "성분", "레티놀"
    ],
    TaskType.SEASONAL_ANALYSIS: [
        "seasonal", "season", "summer", "winter", "holiday", "계절", "여름", "겨울"
    ],
    TaskType.CHANNEL_STATUS: [
        "oliveyoung", "coupang", "naver", "kakao", "channel", "올리브영", "쿠팡", "네이버"
    ],
    TaskType.PRICE_SYNC: [
        "price sync", "price consistency", "가격 동기화", "가격 일치"
    ],
    TaskType.SENTIMENT_ANALYSIS: [
        "review", "sentiment", "feedback", "customer opinion", "리뷰", "평점", "고객 의견"
    ],
    TaskType.PROMOTION_REVIEW: [
        "performance", "analyze promotion", "how did", "결과", "성과", "분석"
    ],
    TaskType.BUNDLE_ANALYSIS: [
        "bundle", "cross-sell", "upsell", "세트", "번들", "교차판매"
    ],
    TaskType.MARGIN_CALCULATION: [
        "margin", "profit", "discount level", "마진", "수익", "할인율"
    ],
    TaskType.STOCKOUT_PREDICTION: [
        "stockout", "stock out", "reorder", "inventory forecast", "재고 부족", "발주"
    ],
    TaskType.INFLUENCER_ROI: [
        "influencer", "kol", "creator", "인플루언서", "크리에이터"
    ],
    TaskType.ATTRIBUTION: [
        "attribution", "channel contribution", "기여도", "채널 기여"
    ],
    TaskType.INVENTORY_MONITORING: [
        "inventory", "stock level", "재고", "재고 현황"
    ],
    TaskType.PRICE_MONITORING: [
        "price monitor", "map violation", "reseller", "가격 모니터링", "리셀러"
    ],
    TaskType.CHECKLIST_VALIDATION: [
        "checklist", "validation", "pre-launch", "체크리스트", "검증"
    ],
}

# Division mappings
TASK_TO_DIVISION: dict[TaskType, Division] = {
    # Strategic Planning
    TaskType.PROMOTION_PLANNING: Division.STRATEGIC_PLANNING,
    TaskType.TIMELINE_MANAGEMENT: Division.STRATEGIC_PLANNING,
    TaskType.BUDGET_ALLOCATION: Division.STRATEGIC_PLANNING,
    # Market Intelligence
    TaskType.NEWS_SCOUTING: Division.MARKET_INTELLIGENCE,
    TaskType.COMPETITOR_ANALYSIS: Division.MARKET_INTELLIGENCE,
    TaskType.INGREDIENT_TRENDS: Division.MARKET_INTELLIGENCE,
    TaskType.SEASONAL_ANALYSIS: Division.MARKET_INTELLIGENCE,
    # Channel Management
    TaskType.CHANNEL_STATUS: Division.CHANNEL_MANAGEMENT,
    TaskType.PRICE_SYNC: Division.CHANNEL_MANAGEMENT,
    TaskType.INVENTORY_CHECK: Division.CHANNEL_MANAGEMENT,
    TaskType.CROSS_CHANNEL: Division.CHANNEL_MANAGEMENT,
    # Analytics
    TaskType.SENTIMENT_ANALYSIS: Division.ANALYTICS,
    TaskType.PROMOTION_REVIEW: Division.ANALYTICS,
    TaskType.BUNDLE_ANALYSIS: Division.ANALYTICS,
    TaskType.MARGIN_CALCULATION: Division.ANALYTICS,
    TaskType.STOCKOUT_PREDICTION: Division.ANALYTICS,
    TaskType.INFLUENCER_ROI: Division.ANALYTICS,
    TaskType.ATTRIBUTION: Division.ANALYTICS,
    # Operations
    TaskType.INVENTORY_MONITORING: Division.OPERATIONS,
    TaskType.PRICE_MONITORING: Division.OPERATIONS,
    TaskType.CHECKLIST_VALIDATION: Division.OPERATIONS,
}

# Multi-division task patterns
MULTI_DIVISION_PATTERNS = [
    {
        "pattern": r"plan.*promotion|promotion.*plan|캠페인.*계획|계획.*캠페인",
        "divisions": [
            Division.STRATEGIC_PLANNING,
            Division.MARKET_INTELLIGENCE,
            Division.CHANNEL_MANAGEMENT,
            Division.ANALYTICS,
        ],
        "description": "Full promotion planning workflow",
    },
    {
        "pattern": r"launch.*check|pre.*launch|런칭.*체크|사전.*검토",
        "divisions": [
            Division.OPERATIONS,
            Division.CHANNEL_MANAGEMENT,
        ],
        "description": "Pre-launch validation",
    },
    {
        "pattern": r"analyze.*channel|channel.*performance|채널.*분석|성과.*분석",
        "divisions": [
            Division.CHANNEL_MANAGEMENT,
            Division.ANALYTICS,
        ],
        "description": "Channel performance analysis",
    },
]


def classify_task(query: str) -> TaskType:
    """
    Classify user query into a task type based on keywords.

    Args:
        query: User's input query

    Returns:
        Classified TaskType
    """
    query_lower = query.lower()

    # Score each task type based on keyword matches
    scores: dict[TaskType, int] = {}
    for task_type, keywords in TASK_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in query_lower)
        if score > 0:
            scores[task_type] = score

    if not scores:
        return TaskType.GENERAL_QUERY

    # Return the task type with highest score
    return max(scores, key=lambda x: scores[x])


def determine_divisions(query: str, task_type: TaskType) -> list[Division]:
    """
    Determine which divisions should handle the request.

    Args:
        query: User's input query
        task_type: Classified task type

    Returns:
        List of divisions to route to (may be multiple for complex tasks)
    """
    query_lower = query.lower()

    # Check for multi-division patterns first
    for pattern_config in MULTI_DIVISION_PATTERNS:
        if re.search(pattern_config["pattern"], query_lower, re.IGNORECASE):
            return pattern_config["divisions"]

    # Single division routing based on task type
    if task_type in TASK_TO_DIVISION:
        return [TASK_TO_DIVISION[task_type]]

    # Default: route to Chief Coordinator for general queries
    return []


def determine_model_tier(task_type: TaskType, query: str) -> str:
    """
    Determine which model tier to use based on task complexity.

    Args:
        task_type: Classified task type
        query: User's input query

    Returns:
        Model tier: "tier1_free", "tier2_cheap", or "tier3_full"
    """
    # Tier 1: Free (no LLM needed)
    tier1_tasks = {
        TaskType.INVENTORY_MONITORING,
        TaskType.CHANNEL_STATUS,
    }
    if task_type in tier1_tasks:
        return "tier1_free"

    # Tier 2: Cheap (mini model)
    tier2_tasks = {
        TaskType.PRICE_MONITORING,
        TaskType.CHECKLIST_VALIDATION,
    }
    if task_type in tier2_tasks:
        return "tier2_cheap"

    # Check query length - short queries might use cheaper model
    if len(query) < 50 and task_type not in {
        TaskType.PROMOTION_PLANNING,
        TaskType.MULTI_DIVISION,
    }:
        return "tier2_cheap"

    # Tier 3: Full model for complex tasks
    return "tier3_full"


def route_to_next(state: PromotorStateDict) -> str | list[str]:
    """
    Route to the next node(s) in the graph based on state.

    This is used as a conditional edge function in LangGraph.

    Args:
        state: Current graph state

    Returns:
        Next node name or list of node names for parallel execution
    """
    next_divisions = state.get("next_divisions", [])
    completed = state.get("completed_divisions", [])
    error = state.get("error")

    # If there's an error, go to error handler
    if error:
        return "error_handler"

    # If all divisions completed, go to aggregator
    if not next_divisions or set(next_divisions) <= set(completed):
        return "response_aggregator"

    # Get pending divisions
    pending = [d for d in next_divisions if d not in completed]

    # Return single or multiple destinations
    if len(pending) == 1:
        return f"{pending[0]}_supervisor"
    return [f"{d}_supervisor" for d in pending]


def get_agent_for_task(division: Division, task_type: TaskType) -> str:
    """
    Get the specific agent within a division for a task type.

    Args:
        division: The division handling the task
        task_type: The classified task type

    Returns:
        Agent name within the division
    """
    agent_mappings: dict[Division, dict[TaskType, str]] = {
        Division.STRATEGIC_PLANNING: {
            TaskType.PROMOTION_PLANNING: "promotion_planner",
            TaskType.TIMELINE_MANAGEMENT: "timeline_manager",
            TaskType.BUDGET_ALLOCATION: "budget_allocator",
        },
        Division.MARKET_INTELLIGENCE: {
            TaskType.NEWS_SCOUTING: "industry_news_scout",
            TaskType.COMPETITOR_ANALYSIS: "competitor_watcher",
            TaskType.INGREDIENT_TRENDS: "ingredient_trend_analyst",
            TaskType.SEASONAL_ANALYSIS: "seasonal_pattern_analyst",
        },
        Division.CHANNEL_MANAGEMENT: {
            TaskType.CHANNEL_STATUS: "cross_channel_syncer",
            TaskType.PRICE_SYNC: "cross_channel_syncer",
            TaskType.INVENTORY_CHECK: "cross_channel_syncer",
            TaskType.CROSS_CHANNEL: "cross_channel_syncer",
        },
        Division.ANALYTICS: {
            TaskType.SENTIMENT_ANALYSIS: "review_sentiment_analyst",
            TaskType.PROMOTION_REVIEW: "promotion_reviewer",
            TaskType.BUNDLE_ANALYSIS: "bundle_analyzer",
            TaskType.MARGIN_CALCULATION: "margin_calculator",
            TaskType.STOCKOUT_PREDICTION: "stockout_predictor",
            TaskType.INFLUENCER_ROI: "influencer_roi_analyst",
            TaskType.ATTRIBUTION: "attribution_analyst",
        },
        Division.OPERATIONS: {
            TaskType.INVENTORY_MONITORING: "inventory_checker",
            TaskType.PRICE_MONITORING: "price_monitor",
            TaskType.CHECKLIST_VALIDATION: "checklist_manager",
        },
    }

    division_agents = agent_mappings.get(division, {})
    return division_agents.get(task_type, "supervisor")
