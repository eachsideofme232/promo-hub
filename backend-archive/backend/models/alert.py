"""Alert model."""

import enum

from sqlalchemy import Boolean, Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.models.base import Base, TimestampMixin, UUIDMixin


class AlertType(str, enum.Enum):
    """Type of alert."""

    INVENTORY = "inventory"
    PRICE = "price"
    CHANNEL = "channel"
    PROMOTION = "promotion"
    SYSTEM = "system"


class AlertSeverity(str, enum.Enum):
    """Severity level of alert."""

    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


class Alert(Base, UUIDMixin, TimestampMixin):
    """Alert model."""

    __tablename__ = "alerts"

    alert_type: Mapped[AlertType] = mapped_column(
        Enum(AlertType),
        default=AlertType.SYSTEM,
        nullable=False,
    )
    severity: Mapped[AlertSeverity] = mapped_column(
        Enum(AlertSeverity),
        default=AlertSeverity.INFO,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str | None] = mapped_column(String(50), nullable=True)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
