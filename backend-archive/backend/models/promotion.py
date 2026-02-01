"""Promotion-related models."""

import enum
import uuid
from datetime import date

from sqlalchemy import BigInteger, Date, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSON, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base, TimestampMixin, UUIDMixin


class PromotionStatus(str, enum.Enum):
    """Status of a promotion."""

    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PromotionType(str, enum.Enum):
    """Type of promotion."""

    FLASH_SALE = "flash_sale"
    SEASONAL = "seasonal"
    BUNDLE = "bundle"
    BRAND_EVENT = "brand_event"
    CHANNEL_EXCLUSIVE = "channel_exclusive"


class EventType(str, enum.Enum):
    """Type of calendar event."""

    PROMOTION_START = "promotion_start"
    PROMOTION_END = "promotion_end"
    DEADLINE = "deadline"
    EVENT = "event"
    MILESTONE = "milestone"


class MilestoneStatus(str, enum.Enum):
    """Status of a milestone."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    OVERDUE = "overdue"


class Priority(str, enum.Enum):
    """Priority level."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Promotion(Base, UUIDMixin, TimestampMixin):
    """Promotion model."""

    __tablename__ = "promotions"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[PromotionStatus] = mapped_column(
        Enum(PromotionStatus),
        default=PromotionStatus.DRAFT,
        nullable=False,
    )
    promotion_type: Mapped[PromotionType] = mapped_column(
        Enum(PromotionType),
        default=PromotionType.SEASONAL,
        nullable=False,
    )
    channels: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    discount_rate: Mapped[str | None] = mapped_column(String(50), nullable=True)
    gmv_target: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    gmv_actual: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    # Relationships
    calendar_events: Mapped[list["CalendarEvent"]] = relationship(
        "CalendarEvent",
        back_populates="promotion",
        cascade="all, delete-orphan",
    )
    milestones: Mapped[list["Milestone"]] = relationship(
        "Milestone",
        back_populates="promotion",
        cascade="all, delete-orphan",
    )
    budgets: Mapped[list["Budget"]] = relationship(
        "Budget",
        back_populates="promotion",
        cascade="all, delete-orphan",
    )


class CalendarEvent(Base, UUIDMixin):
    """Calendar event model."""

    __tablename__ = "calendar_events"

    promotion_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("promotions.id", ondelete="CASCADE"),
        nullable=True,
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType),
        default=EventType.EVENT,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    promotion: Mapped["Promotion | None"] = relationship(
        "Promotion",
        back_populates="calendar_events",
    )


class Milestone(Base, UUIDMixin, TimestampMixin):
    """Milestone model for promotion timeline."""

    __tablename__ = "milestones"

    promotion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("promotions.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[MilestoneStatus] = mapped_column(
        Enum(MilestoneStatus),
        default=MilestoneStatus.PENDING,
        nullable=False,
    )
    priority: Mapped[Priority] = mapped_column(
        Enum(Priority),
        default=Priority.MEDIUM,
        nullable=False,
    )
    dependencies: Mapped[list | None] = mapped_column(JSON, nullable=True)

    # Relationships
    promotion: Mapped["Promotion"] = relationship(
        "Promotion",
        back_populates="milestones",
    )


class Budget(Base, UUIDMixin, TimestampMixin):
    """Budget allocation model."""

    __tablename__ = "budgets"

    promotion_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("promotions.id", ondelete="CASCADE"),
        nullable=False,
    )
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    total_amount: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    advertising: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    discounts: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    influencer: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)
    creative: Mapped[int] = mapped_column(BigInteger, default=0, nullable=False)

    # Relationships
    promotion: Mapped["Promotion"] = relationship(
        "Promotion",
        back_populates="budgets",
    )
