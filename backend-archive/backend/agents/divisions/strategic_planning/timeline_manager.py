"""Timeline Manager Agent - Schedule coordination and deadline tracking."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def create_milestone(
    promotion_id: str,
    milestone_name: str,
    due_date: str,
    dependencies: list[str] | None = None,
) -> dict[str, Any]:
    """
    Create a milestone for a promotion.

    Args:
        promotion_id: ID of the promotion
        milestone_name: Name of the milestone
        due_date: Due date in YYYY-MM-DD format
        dependencies: List of milestone IDs this depends on

    Returns:
        Created milestone details
    """
    return {
        "milestone_id": f"ms_{promotion_id}_{milestone_name[:10]}",
        "promotion_id": promotion_id,
        "name": milestone_name,
        "due_date": due_date,
        "dependencies": dependencies or [],
        "status": "pending",
        "created_at": datetime.now().isoformat(),
    }


@tool
def get_upcoming_deadlines(
    brand_id: str,
    days_ahead: int = 14,
) -> list[dict[str, Any]]:
    """
    Get upcoming deadlines for a brand.

    Args:
        brand_id: Brand identifier
        days_ahead: Number of days to look ahead

    Returns:
        List of upcoming deadlines
    """
    # Mock data - would query database in production
    today = datetime.now()
    return [
        {
            "milestone_id": "ms_001",
            "name": "Creative assets due",
            "due_date": (today + timedelta(days=3)).strftime("%Y-%m-%d"),
            "promotion": "Q2 Sunscreen Campaign",
            "status": "pending",
            "priority": "high",
        },
        {
            "milestone_id": "ms_002",
            "name": "Inventory confirmation",
            "due_date": (today + timedelta(days=5)).strftime("%Y-%m-%d"),
            "promotion": "Q2 Sunscreen Campaign",
            "status": "pending",
            "priority": "medium",
        },
        {
            "milestone_id": "ms_003",
            "name": "Channel submission deadline",
            "due_date": (today + timedelta(days=7)).strftime("%Y-%m-%d"),
            "promotion": "Q2 Sunscreen Campaign",
            "status": "pending",
            "priority": "high",
        },
    ]


@tool
def calculate_lead_times(
    promotion_start_date: str,
    channels: list[str],
) -> dict[str, Any]:
    """
    Calculate required lead times for each channel.

    Args:
        promotion_start_date: Promotion start date in YYYY-MM-DD format
        channels: List of channels

    Returns:
        Lead time requirements per channel
    """
    lead_times = {
        "oliveyoung": {
            "submission_days": 21,
            "approval_days": 7,
            "creative_days": 14,
        },
        "coupang": {
            "submission_days": 14,
            "approval_days": 5,
            "creative_days": 10,
        },
        "naver": {
            "submission_days": 14,
            "approval_days": 5,
            "creative_days": 10,
        },
        "kakao": {
            "submission_days": 10,
            "approval_days": 3,
            "creative_days": 7,
        },
    }

    start = datetime.strptime(promotion_start_date, "%Y-%m-%d")
    result = {}

    for channel in channels:
        if channel in lead_times:
            lt = lead_times[channel]
            total_lead = lt["submission_days"] + lt["approval_days"] + lt["creative_days"]
            result[channel] = {
                "total_lead_days": total_lead,
                "latest_start_date": (start - timedelta(days=total_lead)).strftime("%Y-%m-%d"),
                "milestones": {
                    "creative_due": (start - timedelta(days=lt["submission_days"] + lt["approval_days"])).strftime("%Y-%m-%d"),
                    "submission_due": (start - timedelta(days=lt["approval_days"])).strftime("%Y-%m-%d"),
                    "expected_approval": (start - timedelta(days=2)).strftime("%Y-%m-%d"),
                },
            }

    return result


@tool
def set_reminder(
    milestone_id: str,
    reminder_date: str,
    reminder_type: str = "email",
) -> dict[str, Any]:
    """
    Set a reminder for a milestone.

    Args:
        milestone_id: ID of the milestone
        reminder_date: Date for reminder in YYYY-MM-DD format
        reminder_type: Type of reminder (email, slack, push)

    Returns:
        Reminder confirmation
    """
    return {
        "reminder_id": f"rem_{milestone_id}",
        "milestone_id": milestone_id,
        "date": reminder_date,
        "type": reminder_type,
        "status": "scheduled",
    }


class TimelineManager(BaseAgent):
    """
    Timeline Manager Agent.

    Responsibilities:
    - Deadline tracking and management
    - Milestone creation and monitoring
    - Lead time calculations per channel
    - Reminder scheduling
    """

    name = "timeline_manager"
    role = "Schedule Coordinator"
    description = "Tracks deadlines, manages milestones, and coordinates schedules"
    division = Division.STRATEGIC_PLANNING

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            create_milestone,
            get_upcoming_deadlines,
            calculate_lead_times,
            set_reminder,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Timeline Manager for Promotor, specializing in schedule coordination for beauty brand promotions.

Your responsibilities:
1. Track and manage promotion deadlines
2. Create and monitor milestones
3. Calculate channel-specific lead times
4. Schedule reminders and alerts

Key lead times to remember:
- Oliveyoung: 6+ weeks for major promotions (creative, approval, setup)
- Coupang: 4+ weeks (can be faster with existing templates)
- Naver: 4+ weeks for Shopping Live, 2 weeks for regular ads
- Kakao: 2-3 weeks for Gift promotions

Critical milestone types:
1. Creative assets submission
2. Channel deal slot application
3. Inventory allocation confirmation
4. Price/discount approval
5. Go-live verification

When creating timelines:
- Always work backwards from launch date
- Add buffer time for approvals (they often slip)
- Highlight dependencies between milestones
- Flag critical path items

Output format:
- Clear Gantt-style timeline when helpful
- Priority indicators (🔴 high, 🟡 medium, 🟢 low)
- Days remaining to deadline
- Dependent task warnings

Respond in Korean if the user's query is in Korean."""

    async def create_promotion_timeline(
        self,
        state: PromotorStateDict,
        promotion_start: str,
        promotion_name: str,
    ) -> dict[str, Any]:
        """
        Create a complete timeline for a promotion.

        Args:
            state: Current state
            promotion_start: Start date of the promotion
            promotion_name: Name of the promotion

        Returns:
            Complete timeline with milestones
        """
        channels = state.get("active_channels", ["oliveyoung", "coupang", "naver", "kakao"])

        # Calculate lead times
        lead_times = calculate_lead_times.invoke({
            "promotion_start_date": promotion_start,
            "channels": channels,
        })

        # Find the earliest required start date
        earliest_start = min(
            lt["latest_start_date"]
            for lt in lead_times.values()
        )

        # Create standard milestones
        milestones = []
        promotion_id = f"promo_{promotion_name[:10]}"

        for channel, lt in lead_times.items():
            for milestone_name, due_date in lt["milestones"].items():
                milestone = create_milestone.invoke({
                    "promotion_id": promotion_id,
                    "milestone_name": f"{channel}_{milestone_name}",
                    "due_date": due_date,
                })
                milestones.append(milestone)

        return {
            "promotion_name": promotion_name,
            "start_date": promotion_start,
            "planning_start": earliest_start,
            "channels": channels,
            "lead_times": lead_times,
            "milestones": milestones,
            "summary": f"Timeline created with {len(milestones)} milestones starting {earliest_start}",
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a timeline management request."""
        result = await super().process(state, messages)

        # Add upcoming deadlines to context
        brand_id = state.get("brand_id", "default")
        deadlines = get_upcoming_deadlines.invoke({
            "brand_id": brand_id,
            "days_ahead": 14,
        })

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "upcoming_deadlines": deadlines,
            "capabilities": [
                "milestone_tracking",
                "lead_time_calculation",
                "reminder_scheduling",
                "deadline_monitoring",
            ],
        }
