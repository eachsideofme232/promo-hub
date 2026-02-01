"""Product and inventory models."""

import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import Base, TimestampMixin, UUIDMixin


class InventoryStatus(str, enum.Enum):
    """Inventory status levels."""

    HEALTHY = "healthy"
    LOW_STOCK = "low_stock"
    CRITICAL = "critical"
    OUT_OF_STOCK = "out_of_stock"


class Product(Base, UUIDMixin, TimestampMixin):
    """Product model."""

    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    brand: Mapped[str] = mapped_column(String(100), nullable=False)
    sku: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    map_price: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Relationships
    inventories: Mapped[list["Inventory"]] = relationship(
        "Inventory",
        back_populates="product",
        cascade="all, delete-orphan",
    )


class Inventory(Base, UUIDMixin, TimestampMixin):
    """Inventory model per channel."""

    __tablename__ = "inventories"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    channel: Mapped[str] = mapped_column(String(50), nullable=False)
    current_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    daily_sales_avg: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    status: Mapped[InventoryStatus] = mapped_column(
        Enum(InventoryStatus),
        default=InventoryStatus.HEALTHY,
        nullable=False,
    )

    # Relationships
    product: Mapped["Product"] = relationship(
        "Product",
        back_populates="inventories",
    )
