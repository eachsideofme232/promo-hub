"""Central state management for Promotor multi-agent system."""

from __future__ import annotations

import operator
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Sequence

from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class Division(str, Enum):
    """Available divisions in the Promotor system."""

    STRATEGIC_PLANNING = "strategic_planning"
    MARKET_INTELLIGENCE = "market_intelligence"
    CHANNEL_MANAGEMENT = "channel_management"
    ANALYTICS = "analytics"
    OPERATIONS = "operations"


class TaskType(str, Enum):
    """Types of tasks that can be processed."""

    # Strategic Planning
    PROMOTION_PLANNING = "promotion_planning"
    TIMELINE_MANAGEMENT = "timeline_management"
    BUDGET_ALLOCATION = "budget_allocation"

    # Market Intelligence
    NEWS_SCOUTING = "news_scouting"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    INGREDIENT_TRENDS = "ingredient_trends"
    SEASONAL_ANALYSIS = "seasonal_analysis"

    # Channel Management
    CHANNEL_STATUS = "channel_status"
    PRICE_SYNC = "price_sync"
    INVENTORY_CHECK = "inventory_check"
    CROSS_CHANNEL = "cross_channel"

    # Analytics
    SENTIMENT_ANALYSIS = "sentiment_analysis"
    PROMOTION_REVIEW = "promotion_review"
    BUNDLE_ANALYSIS = "bundle_analysis"
    MARGIN_CALCULATION = "margin_calculation"
    STOCKOUT_PREDICTION = "stockout_prediction"
    INFLUENCER_ROI = "influencer_roi"
    ATTRIBUTION = "attribution"

    # Operations
    INVENTORY_MONITORING = "inventory_monitoring"
    PRICE_MONITORING = "price_monitoring"
    CHECKLIST_VALIDATION = "checklist_validation"

    # General
    GENERAL_QUERY = "general_query"
    MULTI_DIVISION = "multi_division"


class Channel(str, Enum):
    """E-commerce channels supported by Promotor."""

    OLIVEYOUNG = "oliveyoung"
    COUPANG = "coupang"
    NAVER = "naver"
    KAKAO = "kakao"


@dataclass
class DivisionResult:
    """Result from a division's processing."""

    division: Division
    agent_name: str
    result: Any
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    error: str | None = None
    token_usage: int = 0


@dataclass
class DashboardMetrics:
    """Real-time metrics for the dashboard."""

    total_sales: float = 0.0
    active_promotions: int = 0
    pending_alerts: int = 0
    channel_status: dict[str, bool] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)


class PromotorState:
    """
    Central state shared across all agents in the Promotor system.

    This TypedDict-compatible class maintains the conversation history,
    current processing context, and results from all divisions.
    """

    messages: Annotated[Sequence[BaseMessage], add_messages]
    """Conversation history with automatic message addition."""

    current_division: Division | None
    """The division currently processing the request."""

    current_agent: str | None
    """The specific agent within the division handling the task."""

    user_id: str
    """Identifier for the current user."""

    brand_id: str
    """Identifier for the brand being managed."""

    active_channels: list[Channel]
    """List of active e-commerce channels for this brand."""

    task_type: TaskType
    """Classification of the current task."""

    division_results: dict[str, DivisionResult]
    """Results collected from each division's processing."""

    dashboard_metrics: DashboardMetrics
    """Current dashboard metrics."""

    # Routing control
    next_divisions: list[Division]
    """Divisions that should process next (for parallel execution)."""

    completed_divisions: list[Division]
    """Divisions that have completed processing."""

    # Token optimization
    use_mini_model: bool
    """Whether to use the smaller/cheaper model for this task."""

    cache_key: str | None
    """Key for caching this request's result."""

    # Error handling
    error: str | None
    """Any error that occurred during processing."""

    retry_count: int
    """Number of retries attempted."""


# Type alias for LangGraph compatibility
from typing import TypedDict


class PromotorStateDict(TypedDict, total=False):
    """TypedDict version of PromotorState for LangGraph compatibility."""

    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_division: str | None
    current_agent: str | None
    user_id: str
    brand_id: str
    active_channels: list[str]
    task_type: str
    division_results: dict[str, Any]
    dashboard_metrics: dict[str, Any]
    next_divisions: list[str]
    completed_divisions: list[str]
    use_mini_model: bool
    cache_key: str | None
    error: str | None
    retry_count: int


def create_initial_state(
    user_id: str,
    brand_id: str,
    active_channels: list[str] | None = None,
) -> PromotorStateDict:
    """Create initial state for a new conversation."""
    return PromotorStateDict(
        messages=[],
        current_division=None,
        current_agent=None,
        user_id=user_id,
        brand_id=brand_id,
        active_channels=active_channels or ["oliveyoung", "coupang", "naver", "kakao"],
        task_type=TaskType.GENERAL_QUERY.value,
        division_results={},
        dashboard_metrics={
            "total_sales": 0.0,
            "active_promotions": 0,
            "pending_alerts": 0,
            "channel_status": {
                "oliveyoung": True,
                "coupang": True,
                "naver": True,
                "kakao": False,
            },
            "last_updated": datetime.now().isoformat(),
        },
        next_divisions=[],
        completed_divisions=[],
        use_mini_model=False,
        cache_key=None,
        error=None,
        retry_count=0,
    )


def merge_division_results(
    existing: dict[str, Any],
    new_results: dict[str, Any],
) -> dict[str, Any]:
    """Merge new division results with existing ones."""
    merged = existing.copy()
    merged.update(new_results)
    return merged


# Reducer for division results
def add_division_results(
    left: dict[str, Any],
    right: dict[str, Any],
) -> dict[str, Any]:
    """Reducer function for accumulating division results."""
    return merge_division_results(left, right)
