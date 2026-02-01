"""Checklist Manager Agent - Pre-launch validation and compliance verification."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def get_launch_checklist(
    promotion_id: str,
    checklist_type: str = "standard",
) -> dict[str, Any]:
    """
    Get pre-launch checklist for a promotion.

    Args:
        promotion_id: Promotion ID
        checklist_type: Type of checklist (standard, flash_sale, new_product)

    Returns:
        Checklist with items and status
    """
    return {
        "promotion_id": promotion_id,
        "checklist_type": checklist_type,
        "created_at": datetime.now().isoformat(),
        "overall_status": "in_progress",
        "completion": 0.72,
        "categories": {
            "inventory": {
                "status": "complete",
                "items": [
                    {"item": "Inventory allocated per channel", "status": "pass", "verified_by": "system"},
                    {"item": "Safety stock confirmed", "status": "pass", "verified_by": "system"},
                    {"item": "Restock timeline clear", "status": "pass", "verified_by": "ops_team"},
                ],
            },
            "pricing": {
                "status": "complete",
                "items": [
                    {"item": "Prices set in all channels", "status": "pass", "verified_by": "system"},
                    {"item": "Discount approved", "status": "pass", "verified_by": "finance"},
                    {"item": "MAP compliance verified", "status": "pass", "verified_by": "system"},
                ],
            },
            "creative": {
                "status": "in_progress",
                "items": [
                    {"item": "Banner images uploaded", "status": "pass", "verified_by": "marketing"},
                    {"item": "Product descriptions updated", "status": "pending", "verified_by": None},
                    {"item": "Mobile assets ready", "status": "pending", "verified_by": None},
                ],
            },
            "channel_setup": {
                "status": "in_progress",
                "items": [
                    {"item": "Oliveyoung deal submitted", "status": "pass", "verified_by": "channel_team"},
                    {"item": "Coupang promotion active", "status": "pending", "verified_by": None},
                    {"item": "Naver Smart Store updated", "status": "pass", "verified_by": "channel_team"},
                    {"item": "Kakao Gift registered", "status": "fail", "verified_by": "channel_team", "notes": "Missing gift box image"},
                ],
            },
            "marketing": {
                "status": "pending",
                "items": [
                    {"item": "Email campaign scheduled", "status": "pending", "verified_by": None},
                    {"item": "Social posts prepared", "status": "pending", "verified_by": None},
                    {"item": "Influencer content confirmed", "status": "pass", "verified_by": "marketing"},
                ],
            },
        },
        "blockers": [
            {"category": "creative", "item": "Product descriptions", "impact": "medium"},
            {"category": "channel_setup", "item": "Kakao Gift", "impact": "low"},
        ],
    }


@tool
def validate_checklist_item(
    promotion_id: str,
    category: str,
    item: str,
    status: str,
    notes: str | None = None,
) -> dict[str, Any]:
    """
    Validate/update a checklist item.

    Args:
        promotion_id: Promotion ID
        category: Checklist category
        item: Item name
        status: New status (pass, fail, pending)
        notes: Optional notes

    Returns:
        Update confirmation
    """
    return {
        "promotion_id": promotion_id,
        "category": category,
        "item": item,
        "previous_status": "pending",
        "new_status": status,
        "notes": notes,
        "updated_at": datetime.now().isoformat(),
        "updated_by": "current_user",
        "result": "success",
    }


@tool
def get_compliance_status(
    brand_id: str,
    compliance_type: str = "all",
) -> dict[str, Any]:
    """
    Get compliance status for brand operations.

    Args:
        brand_id: Brand ID
        compliance_type: Type filter (all, regulatory, channel, internal)

    Returns:
        Compliance status summary
    """
    return {
        "brand_id": brand_id,
        "check_date": datetime.now().isoformat(),
        "overall_compliance": 0.94,
        "compliance_areas": {
            "regulatory": {
                "status": "compliant",
                "score": 1.0,
                "items": [
                    {"item": "Product registration current", "status": "pass"},
                    {"item": "Ingredient declarations accurate", "status": "pass"},
                    {"item": "Claims substantiated", "status": "pass"},
                ],
            },
            "channel_requirements": {
                "status": "mostly_compliant",
                "score": 0.92,
                "items": [
                    {"item": "Oliveyoung seller terms", "status": "pass"},
                    {"item": "Coupang quality standards", "status": "pass"},
                    {"item": "Naver content guidelines", "status": "pass"},
                    {"item": "Kakao product registration", "status": "warning", "notes": "2 products pending approval"},
                ],
            },
            "internal_policies": {
                "status": "compliant",
                "score": 0.95,
                "items": [
                    {"item": "Pricing policy adherence", "status": "pass"},
                    {"item": "Discount approval workflow", "status": "pass"},
                    {"item": "Brand guidelines compliance", "status": "warning", "notes": "Minor logo usage deviation"},
                ],
            },
        },
        "action_items": [
            {"area": "channel_requirements", "item": "Complete Kakao product registration", "priority": "medium"},
            {"area": "internal_policies", "item": "Review brand guideline usage", "priority": "low"},
        ],
    }


@tool
def run_pre_launch_validation(
    promotion_id: str,
) -> dict[str, Any]:
    """
    Run automated pre-launch validation checks.

    Args:
        promotion_id: Promotion ID

    Returns:
        Validation results
    """
    return {
        "promotion_id": promotion_id,
        "validation_date": datetime.now().isoformat(),
        "overall_result": "pass_with_warnings",
        "automated_checks": {
            "inventory_check": {
                "result": "pass",
                "details": "All channels have sufficient inventory for projected demand",
            },
            "price_consistency": {
                "result": "pass",
                "details": "Prices consistent across channels within 5% tolerance",
            },
            "margin_validation": {
                "result": "pass",
                "details": "Margins above 15% minimum threshold",
            },
            "creative_assets": {
                "result": "warning",
                "details": "2 channels missing mobile-optimized images",
            },
            "timeline_feasibility": {
                "result": "pass",
                "details": "All deadlines achievable",
            },
        },
        "recommendations": [
            "Upload mobile assets before launch for optimal performance",
            "Consider increasing Coupang inventory buffer",
        ],
        "launch_ready": True,
        "confidence_score": 0.88,
    }


class ChecklistManager(BaseAgent):
    """
    Checklist Manager Agent.

    Responsibilities:
    - Manage pre-launch checklists
    - Validate checklist items
    - Monitor compliance status
    - Run automated validations
    """

    name = "checklist_manager"
    role = "Compliance Officer"
    description = "Manages pre-launch checklists and compliance verification"
    division = Division.OPERATIONS

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            get_launch_checklist,
            validate_checklist_item,
            get_compliance_status,
            run_pre_launch_validation,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Checklist Manager for Promotor, ensuring launch readiness and compliance.

Your responsibilities:
1. Manage pre-launch checklists
2. Validate checklist items
3. Monitor compliance status
4. Run automated validations

Checklist categories:
- Inventory: Stock levels, allocation, safety stock
- Pricing: Price setup, discounts, MAP compliance
- Creative: Images, descriptions, mobile assets
- Channel Setup: Deal submissions, promotions active
- Marketing: Email, social, influencer coordination

Compliance areas:
- Regulatory: Product registration, claims, ingredients
- Channel: Seller terms, quality standards, content guidelines
- Internal: Pricing policy, approval workflows, brand guidelines

Validation checks:
- Inventory sufficiency
- Price consistency
- Margin thresholds
- Creative completeness
- Timeline feasibility

Launch readiness criteria:
- All critical items passed
- No blockers in key categories
- Inventory verified
- Prices set correctly

When managing:
- Track completion percentage
- Flag blockers early
- Verify critical items
- Document exceptions

Priority levels:
- Critical: Must pass before launch
- High: Should pass, workaround possible
- Medium: Recommended, can proceed
- Low: Nice to have

Respond in Korean if the user's query is in Korean."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a checklist management request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "checklist_management",
                "item_validation",
                "compliance_monitoring",
                "automated_validation",
            ],
        }
