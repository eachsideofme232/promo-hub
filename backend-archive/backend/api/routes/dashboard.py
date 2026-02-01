"""Dashboard endpoints for metrics and real-time data."""

from datetime import date, datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.db.session import get_db
from backend.models import Alert, CalendarEvent, Inventory, Promotion
from backend.models.alert import AlertSeverity
from backend.models.promotion import PromotionStatus

router = APIRouter()


class ChannelStatus(BaseModel):
    """Channel status model."""

    name: str
    status: str  # "online", "offline", "degraded"
    last_sync: str
    metrics: dict[str, Any]


class DashboardMetrics(BaseModel):
    """Dashboard metrics model."""

    total_sales: float
    active_promotions: int
    pending_alerts: int
    channel_status: dict[str, bool]


@router.get("/metrics")
async def get_dashboard_metrics(db: AsyncSession = Depends(get_db)):
    """Get main dashboard metrics."""
    # Count active promotions
    active_promos_query = select(func.count(Promotion.id)).where(
        Promotion.status == PromotionStatus.ACTIVE
    )
    active_promos_result = await db.execute(active_promos_query)
    active_promos = active_promos_result.scalar() or 0

    # Count scheduled promotions
    scheduled_promos_query = select(func.count(Promotion.id)).where(
        Promotion.status == PromotionStatus.SCHEDULED
    )
    scheduled_promos_result = await db.execute(scheduled_promos_query)
    scheduled_promos = scheduled_promos_result.scalar() or 0

    # Count pending alerts by severity
    alerts_query = select(Alert).where(Alert.acknowledged == False)  # noqa: E712
    alerts_result = await db.execute(alerts_query)
    alerts = alerts_result.scalars().all()

    critical_count = sum(1 for a in alerts if a.severity == AlertSeverity.CRITICAL)
    warning_count = sum(1 for a in alerts if a.severity == AlertSeverity.WARNING)

    return {
        "timestamp": datetime.now().isoformat(),
        "metrics": {
            "total_sales": {
                "value": 0,
                "change": 0.0,
                "period": "7d",
            },
            "active_promotions": {
                "value": active_promos + scheduled_promos,
                "by_channel": {
                    "oliveyoung": 0,
                    "coupang": 0,
                    "naver": 0,
                    "kakao": 0,
                },
            },
            "pending_alerts": {
                "value": len(alerts),
                "by_severity": {
                    "critical": critical_count,
                    "warning": warning_count,
                },
            },
            "channel_health": {
                "oliveyoung": {"status": "online", "sync_status": "current"},
                "coupang": {"status": "online", "sync_status": "current"},
                "naver": {"status": "online", "sync_status": "current"},
                "kakao": {"status": "online", "sync_status": "current"},
            },
        },
    }


@router.get("/channels")
async def get_channel_overview():
    """Get overview of all channels."""
    return {
        "timestamp": datetime.now().isoformat(),
        "channels": [
            {
                "name": "Oliveyoung",
                "code": "oliveyoung",
                "status": "online",
                "metrics": {
                    "gmv_7d": 0,
                    "orders_7d": 0,
                    "active_deals": 0,
                    "ranking_position": None,
                },
            },
            {
                "name": "Coupang",
                "code": "coupang",
                "status": "online",
                "metrics": {
                    "gmv_7d": 0,
                    "orders_7d": 0,
                    "active_deals": 0,
                    "rocket_status": "healthy",
                },
            },
            {
                "name": "Naver",
                "code": "naver",
                "status": "online",
                "metrics": {
                    "gmv_7d": 0,
                    "orders_7d": 0,
                    "store_grade": None,
                    "live_scheduled": 0,
                },
            },
            {
                "name": "Kakao",
                "code": "kakao",
                "status": "online",
                "metrics": {
                    "gmv_7d": 0,
                    "orders_7d": 0,
                    "gift_ranking": None,
                    "channel_friends": 0,
                },
            },
        ],
    }


@router.get("/alerts")
async def get_active_alerts(db: AsyncSession = Depends(get_db)):
    """Get active alerts."""
    query = (
        select(Alert)
        .where(Alert.acknowledged == False)  # noqa: E712
        .order_by(Alert.severity, Alert.created_at.desc())
    )
    result = await db.execute(query)
    alerts = result.scalars().all()

    return {
        "timestamp": datetime.now().isoformat(),
        "total": len(alerts),
        "alerts": [
            {
                "id": str(alert.id),
                "type": alert.alert_type.value,
                "severity": alert.severity.value,
                "title": alert.title,
                "message": alert.message,
                "channel": alert.channel,
                "acknowledged": alert.acknowledged,
                "created_at": alert.created_at.isoformat(),
            }
            for alert in alerts
        ],
    }


@router.get("/promotions")
async def get_active_promotions(db: AsyncSession = Depends(get_db)):
    """Get active and upcoming promotions."""
    today = date.today()

    # Get active promotions
    active_query = (
        select(Promotion)
        .where(Promotion.status == PromotionStatus.ACTIVE)
        .options(selectinload(Promotion.budgets))
    )
    active_result = await db.execute(active_query)
    active_promos = active_result.scalars().all()

    # Get scheduled (upcoming) promotions
    scheduled_query = (
        select(Promotion)
        .where(Promotion.status.in_([PromotionStatus.SCHEDULED, PromotionStatus.DRAFT]))
        .where(Promotion.start_date >= today)
        .options(selectinload(Promotion.budgets))
        .order_by(Promotion.start_date)
    )
    scheduled_result = await db.execute(scheduled_query)
    upcoming_promos = scheduled_result.scalars().all()

    def format_promotion(promo: Promotion) -> dict[str, Any]:
        total_budget = sum(b.total_amount for b in promo.budgets)
        return {
            "id": str(promo.id),
            "name": promo.name,
            "description": promo.description,
            "status": promo.status.value,
            "type": promo.promotion_type.value,
            "channels": promo.channels,
            "start_date": promo.start_date.isoformat(),
            "end_date": promo.end_date.isoformat(),
            "discount_rate": promo.discount_rate,
            "gmv_target": promo.gmv_target,
            "gmv_actual": promo.gmv_actual,
            "total_budget": total_budget,
        }

    return {
        "timestamp": datetime.now().isoformat(),
        "active": [format_promotion(p) for p in active_promos],
        "upcoming": [format_promotion(p) for p in upcoming_promos],
    }


@router.get("/calendar")
async def get_promotion_calendar(
    year: int | None = None,
    month: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Get promotion calendar view."""
    today = date.today()
    target_year = year or today.year
    target_month = month or today.month

    # Get events for the target month (and adjacent months for context)
    query = select(CalendarEvent).options(selectinload(CalendarEvent.promotion))

    result = await db.execute(query)
    events = result.scalars().all()

    def format_event(event: CalendarEvent) -> dict[str, Any]:
        # Determine display type based on event type
        display_type = "event"
        if event.event_type.value in ["promotion_start", "promotion_end"]:
            display_type = "promotion"
        elif event.event_type.value == "deadline":
            display_type = "deadline"

        status = None
        if event.promotion:
            status = event.promotion.status.value

        return {
            "id": str(event.id),
            "date": event.date.isoformat(),
            "type": display_type,
            "event_type": event.event_type.value,
            "title": event.title,
            "description": event.description,
            "status": status,
            "promotion_id": str(event.promotion_id) if event.promotion_id else None,
        }

    return {
        "timestamp": datetime.now().isoformat(),
        "view": "month",
        "current_month": f"{target_year:04d}-{target_month:02d}",
        "events": [format_event(e) for e in events],
    }


@router.get("/promotions/{promotion_id}")
async def get_promotion_detail(promotion_id: str, db: AsyncSession = Depends(get_db)):
    """Get detailed promotion information including milestones and budgets."""
    try:
        promo_uuid = UUID(promotion_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid promotion ID format")

    query = (
        select(Promotion)
        .where(Promotion.id == promo_uuid)
        .options(
            selectinload(Promotion.milestones),
            selectinload(Promotion.budgets),
            selectinload(Promotion.calendar_events),
        )
    )
    result = await db.execute(query)
    promo = result.scalar_one_or_none()

    if not promo:
        raise HTTPException(status_code=404, detail="Promotion not found")

    return {
        "id": str(promo.id),
        "name": promo.name,
        "description": promo.description,
        "status": promo.status.value,
        "type": promo.promotion_type.value,
        "channels": promo.channels,
        "start_date": promo.start_date.isoformat(),
        "end_date": promo.end_date.isoformat(),
        "discount_rate": promo.discount_rate,
        "gmv_target": promo.gmv_target,
        "gmv_actual": promo.gmv_actual,
        "milestones": [
            {
                "id": str(m.id),
                "name": m.name,
                "due_date": m.due_date.isoformat(),
                "status": m.status.value,
                "priority": m.priority.value,
            }
            for m in promo.milestones
        ],
        "budgets": [
            {
                "id": str(b.id),
                "channel": b.channel,
                "total_amount": b.total_amount,
                "advertising": b.advertising,
                "discounts": b.discounts,
                "influencer": b.influencer,
                "creative": b.creative,
            }
            for b in promo.budgets
        ],
        "events": [
            {
                "id": str(e.id),
                "date": e.date.isoformat(),
                "event_type": e.event_type.value,
                "title": e.title,
            }
            for e in promo.calendar_events
        ],
    }


@router.get("/inventory")
async def get_inventory_status(db: AsyncSession = Depends(get_db)):
    """Get inventory status across all channels."""
    query = select(Inventory).options(selectinload(Inventory.product))
    result = await db.execute(query)
    inventories = result.scalars().all()

    # Group by status
    status_counts = {
        "healthy": 0,
        "low_stock": 0,
        "critical": 0,
        "out_of_stock": 0,
    }

    items = []
    for inv in inventories:
        status_counts[inv.status.value] += 1
        items.append({
            "id": str(inv.id),
            "product_id": str(inv.product_id),
            "product_name": inv.product.name,
            "product_sku": inv.product.sku,
            "channel": inv.channel,
            "current_stock": inv.current_stock,
            "daily_sales_avg": inv.daily_sales_avg,
            "days_of_stock": (
                inv.current_stock // inv.daily_sales_avg
                if inv.daily_sales_avg > 0
                else None
            ),
            "status": inv.status.value,
        })

    return {
        "timestamp": datetime.now().isoformat(),
        "summary": status_counts,
        "items": items,
    }


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str, db: AsyncSession = Depends(get_db)):
    """Acknowledge an alert."""
    try:
        alert_uuid = UUID(alert_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid alert ID format")

    query = select(Alert).where(Alert.id == alert_uuid)
    result = await db.execute(query)
    alert = result.scalar_one_or_none()

    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.acknowledged = True
    await db.commit()

    return {
        "alert_id": alert_id,
        "acknowledged": True,
        "acknowledged_at": datetime.now().isoformat(),
    }
