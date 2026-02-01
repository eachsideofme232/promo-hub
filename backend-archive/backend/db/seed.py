"""Seed script for sample K-beauty promotion data."""

import asyncio
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.session import async_session, engine
from backend.models import (
    Alert,
    Base,
    Budget,
    CalendarEvent,
    Inventory,
    Milestone,
    Product,
    Promotion,
)
from backend.models.alert import AlertSeverity, AlertType
from backend.models.inventory import InventoryStatus
from backend.models.promotion import (
    EventType,
    MilestoneStatus,
    Priority,
    PromotionStatus,
    PromotionType,
)


async def create_tables() -> None:
    """Create all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")


async def drop_tables() -> None:
    """Drop all tables (for reset)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("Tables dropped successfully.")


async def seed_products(session: AsyncSession) -> dict[str, Product]:
    """Create sample K-beauty products."""
    products_data = [
        {
            "name": "히알루론산 토너",
            "category": "스킨케어",
            "brand": "글로우랩",
            "sku": "GL-HT-150",
            "price": 28000,
            "map_price": 25000,
        },
        {
            "name": "레티놀 나이트크림",
            "category": "스킨케어",
            "brand": "글로우랩",
            "sku": "GL-RN-050",
            "price": 45000,
            "map_price": 40000,
        },
        {
            "name": "비타민C 세럼",
            "category": "스킨케어",
            "brand": "글로우랩",
            "sku": "GL-VC-030",
            "price": 38000,
            "map_price": 34000,
        },
        {
            "name": "선크림 SPF50+",
            "category": "선케어",
            "brand": "글로우랩",
            "sku": "GL-SC-050",
            "price": 25000,
            "map_price": 22000,
        },
        {
            "name": "클렌징밤",
            "category": "클렌징",
            "brand": "글로우랩",
            "sku": "GL-CB-100",
            "price": 32000,
            "map_price": 28000,
        },
    ]

    products = {}
    for data in products_data:
        product = Product(**data)
        session.add(product)
        products[data["sku"]] = product

    await session.flush()
    print(f"Created {len(products)} products.")
    return products


async def seed_inventories(session: AsyncSession, products: dict[str, Product]) -> None:
    """Create sample inventory data per channel."""
    channels = ["oliveyoung", "coupang", "naver", "kakao"]
    inventory_data = [
        # Hyaluronic Toner
        {"sku": "GL-HT-150", "oliveyoung": (500, 25, InventoryStatus.HEALTHY)},
        {"sku": "GL-HT-150", "coupang": (300, 30, InventoryStatus.HEALTHY)},
        {"sku": "GL-HT-150", "naver": (150, 10, InventoryStatus.HEALTHY)},
        {"sku": "GL-HT-150", "kakao": (80, 5, InventoryStatus.LOW_STOCK)},
        # Retinol Night Cream
        {"sku": "GL-RN-050", "oliveyoung": (200, 15, InventoryStatus.HEALTHY)},
        {"sku": "GL-RN-050", "coupang": (45, 12, InventoryStatus.CRITICAL)},
        {"sku": "GL-RN-050", "naver": (100, 8, InventoryStatus.HEALTHY)},
        # Vitamin C Serum
        {"sku": "GL-VC-030", "oliveyoung": (350, 20, InventoryStatus.HEALTHY)},
        {"sku": "GL-VC-030", "coupang": (0, 18, InventoryStatus.OUT_OF_STOCK)},
        {"sku": "GL-VC-030", "naver": (120, 7, InventoryStatus.HEALTHY)},
        # Sunscreen
        {"sku": "GL-SC-050", "oliveyoung": (600, 40, InventoryStatus.HEALTHY)},
        {"sku": "GL-SC-050", "coupang": (400, 35, InventoryStatus.HEALTHY)},
        {"sku": "GL-SC-050", "naver": (200, 15, InventoryStatus.HEALTHY)},
        {"sku": "GL-SC-050", "kakao": (100, 8, InventoryStatus.HEALTHY)},
        # Cleansing Balm
        {"sku": "GL-CB-100", "oliveyoung": (250, 12, InventoryStatus.HEALTHY)},
        {"sku": "GL-CB-100", "coupang": (35, 10, InventoryStatus.CRITICAL)},
    ]

    count = 0
    for data in inventory_data:
        sku = data["sku"]
        product = products[sku]
        for channel in channels:
            if channel in data:
                stock, daily_avg, status = data[channel]
                inventory = Inventory(
                    product_id=product.id,
                    channel=channel,
                    current_stock=stock,
                    daily_sales_avg=daily_avg,
                    status=status,
                )
                session.add(inventory)
                count += 1

    await session.flush()
    print(f"Created {count} inventory records.")


async def seed_promotions(session: AsyncSession) -> dict[str, Promotion]:
    """Create sample promotions."""
    promotions_data = [
        {
            "name": "설 선물세트 프로모션",
            "description": "설날 맞이 프리미엄 선물세트 할인 행사",
            "status": PromotionStatus.SCHEDULED,
            "promotion_type": PromotionType.SEASONAL,
            "channels": ["kakao", "naver"],
            "start_date": date(2026, 2, 1),
            "end_date": date(2026, 2, 15),
            "discount_rate": "15%",
            "gmv_target": 150000000,  # 1.5억원
            "gmv_actual": None,
        },
        {
            "name": "봄맞이 수분케어 기획전",
            "description": "봄철 건조함 대비 수분케어 라인 기획전",
            "status": PromotionStatus.DRAFT,
            "promotion_type": PromotionType.SEASONAL,
            "channels": ["oliveyoung", "coupang"],
            "start_date": date(2026, 3, 1),
            "end_date": date(2026, 3, 15),
            "discount_rate": "20%",
            "gmv_target": 200000000,  # 2억원
            "gmv_actual": None,
        },
        {
            "name": "올리브영 페스타 참여",
            "description": "올리브영 대규모 세일 이벤트 참여",
            "status": PromotionStatus.DRAFT,
            "promotion_type": PromotionType.CHANNEL_EXCLUSIVE,
            "channels": ["oliveyoung"],
            "start_date": date(2026, 4, 1),
            "end_date": date(2026, 4, 7),
            "discount_rate": "25%",
            "gmv_target": 100000000,  # 1억원
            "gmv_actual": None,
        },
    ]

    promotions = {}
    for data in promotions_data:
        promotion = Promotion(**data)
        session.add(promotion)
        promotions[data["name"]] = promotion

    await session.flush()
    print(f"Created {len(promotions)} promotions.")
    return promotions


async def seed_calendar_events(
    session: AsyncSession, promotions: dict[str, Promotion]
) -> None:
    """Create calendar events for promotions and deadlines."""
    events_data = [
        # Lunar New Year Promotion Events
        {
            "promotion": "설 선물세트 프로모션",
            "date": date(2026, 2, 1),
            "event_type": EventType.PROMOTION_START,
            "title": "설 선물세트 시작",
            "description": "카카오, 네이버 동시 런칭",
        },
        {
            "promotion": "설 선물세트 프로모션",
            "date": date(2026, 2, 15),
            "event_type": EventType.PROMOTION_END,
            "title": "설 선물세트 종료",
            "description": None,
        },
        # Spring Hydration Events
        {
            "promotion": "봄맞이 수분케어 기획전",
            "date": date(2026, 3, 1),
            "event_type": EventType.PROMOTION_START,
            "title": "봄 수분케어 시작",
            "description": "올리브영, 쿠팡 동시 런칭",
        },
        {
            "promotion": "봄맞이 수분케어 기획전",
            "date": date(2026, 3, 15),
            "event_type": EventType.PROMOTION_END,
            "title": "봄 수분케어 종료",
            "description": None,
        },
        # Oliveyoung Festa Events
        {
            "promotion": "올리브영 페스타 참여",
            "date": date(2026, 4, 1),
            "event_type": EventType.PROMOTION_START,
            "title": "올리브영 페스타 시작",
            "description": "25% 할인 행사",
        },
        {
            "promotion": "올리브영 페스타 참여",
            "date": date(2026, 4, 7),
            "event_type": EventType.PROMOTION_END,
            "title": "올리브영 페스타 종료",
            "description": None,
        },
        # Standalone Deadlines (no promotion)
        {
            "promotion": None,
            "date": date(2026, 2, 10),
            "event_type": EventType.DEADLINE,
            "title": "Q2 기획 제출 마감",
            "description": "2분기 프로모션 기획안 제출",
        },
        {
            "promotion": None,
            "date": date(2026, 3, 20),
            "event_type": EventType.DEADLINE,
            "title": "올리브영 페스타 신청 마감",
            "description": "올리브영 페스타 참여 신청 마감일",
        },
        {
            "promotion": None,
            "date": date(2026, 2, 25),
            "event_type": EventType.EVENT,
            "title": "인플루언서 미팅",
            "description": "봄 시즌 협업 인플루언서 선정 미팅",
        },
    ]

    count = 0
    for data in events_data:
        promo_name = data.pop("promotion")
        promotion_id = promotions[promo_name].id if promo_name else None
        event = CalendarEvent(promotion_id=promotion_id, **data)
        session.add(event)
        count += 1

    await session.flush()
    print(f"Created {count} calendar events.")


async def seed_milestones(session: AsyncSession, promotions: dict[str, Promotion]) -> None:
    """Create milestones for promotions."""
    milestones_data = [
        # 설 선물세트 프로모션
        {
            "promotion": "설 선물세트 프로모션",
            "name": "상품 기획 완료",
            "due_date": date(2026, 1, 15),
            "status": MilestoneStatus.COMPLETE,
            "priority": Priority.HIGH,
        },
        {
            "promotion": "설 선물세트 프로모션",
            "name": "패키지 디자인 확정",
            "due_date": date(2026, 1, 20),
            "status": MilestoneStatus.COMPLETE,
            "priority": Priority.HIGH,
        },
        {
            "promotion": "설 선물세트 프로모션",
            "name": "재고 입고 완료",
            "due_date": date(2026, 1, 28),
            "status": MilestoneStatus.IN_PROGRESS,
            "priority": Priority.HIGH,
        },
        {
            "promotion": "설 선물세트 프로모션",
            "name": "채널 상품 등록",
            "due_date": date(2026, 1, 30),
            "status": MilestoneStatus.PENDING,
            "priority": Priority.MEDIUM,
        },
        # 봄맞이 수분케어 기획전
        {
            "promotion": "봄맞이 수분케어 기획전",
            "name": "기획안 작성",
            "due_date": date(2026, 2, 1),
            "status": MilestoneStatus.PENDING,
            "priority": Priority.HIGH,
        },
        {
            "promotion": "봄맞이 수분케어 기획전",
            "name": "예산 승인",
            "due_date": date(2026, 2, 10),
            "status": MilestoneStatus.PENDING,
            "priority": Priority.HIGH,
        },
        {
            "promotion": "봄맞이 수분케어 기획전",
            "name": "크리에이티브 제작",
            "due_date": date(2026, 2, 20),
            "status": MilestoneStatus.PENDING,
            "priority": Priority.MEDIUM,
        },
        # 올리브영 페스타
        {
            "promotion": "올리브영 페스타 참여",
            "name": "참여 신청서 제출",
            "due_date": date(2026, 3, 20),
            "status": MilestoneStatus.PENDING,
            "priority": Priority.HIGH,
        },
        {
            "promotion": "올리브영 페스타 참여",
            "name": "할인 상품 선정",
            "due_date": date(2026, 3, 25),
            "status": MilestoneStatus.PENDING,
            "priority": Priority.MEDIUM,
        },
    ]

    count = 0
    for data in milestones_data:
        promo_name = data.pop("promotion")
        promotion_id = promotions[promo_name].id
        milestone = Milestone(promotion_id=promotion_id, **data)
        session.add(milestone)
        count += 1

    await session.flush()
    print(f"Created {count} milestones.")


async def seed_budgets(session: AsyncSession, promotions: dict[str, Promotion]) -> None:
    """Create budget allocations for promotions."""
    budgets_data = [
        # 설 선물세트 프로모션 - Kakao
        {
            "promotion": "설 선물세트 프로모션",
            "channel": "kakao",
            "total_amount": 30000000,  # 3천만원
            "advertising": 15000000,
            "discounts": 10000000,
            "influencer": 3000000,
            "creative": 2000000,
        },
        # 설 선물세트 프로모션 - Naver
        {
            "promotion": "설 선물세트 프로모션",
            "channel": "naver",
            "total_amount": 25000000,  # 2천5백만원
            "advertising": 12000000,
            "discounts": 8000000,
            "influencer": 3000000,
            "creative": 2000000,
        },
        # 봄맞이 수분케어 기획전 - Oliveyoung
        {
            "promotion": "봄맞이 수분케어 기획전",
            "channel": "oliveyoung",
            "total_amount": 50000000,  # 5천만원
            "advertising": 20000000,
            "discounts": 20000000,
            "influencer": 5000000,
            "creative": 5000000,
        },
        # 봄맞이 수분케어 기획전 - Coupang
        {
            "promotion": "봄맞이 수분케어 기획전",
            "channel": "coupang",
            "total_amount": 40000000,  # 4천만원
            "advertising": 18000000,
            "discounts": 15000000,
            "influencer": 4000000,
            "creative": 3000000,
        },
        # 올리브영 페스타 참여
        {
            "promotion": "올리브영 페스타 참여",
            "channel": "oliveyoung",
            "total_amount": 35000000,  # 3천5백만원
            "advertising": 10000000,
            "discounts": 20000000,
            "influencer": 3000000,
            "creative": 2000000,
        },
    ]

    count = 0
    for data in budgets_data:
        promo_name = data.pop("promotion")
        promotion_id = promotions[promo_name].id
        budget = Budget(promotion_id=promotion_id, **data)
        session.add(budget)
        count += 1

    await session.flush()
    print(f"Created {count} budget records.")


async def seed_alerts(session: AsyncSession) -> None:
    """Create sample alerts."""
    alerts_data = [
        {
            "alert_type": AlertType.INVENTORY,
            "severity": AlertSeverity.CRITICAL,
            "title": "비타민C 세럼 품절",
            "message": "쿠팡 채널에서 비타민C 세럼(GL-VC-030)이 품절되었습니다. 긴급 재고 보충이 필요합니다.",
            "channel": "coupang",
            "acknowledged": False,
        },
        {
            "alert_type": AlertType.INVENTORY,
            "severity": AlertSeverity.CRITICAL,
            "title": "레티놀 크림 재고 부족",
            "message": "쿠팡 채널의 레티놀 나이트크림 재고가 3일 분량만 남았습니다.",
            "channel": "coupang",
            "acknowledged": False,
        },
        {
            "alert_type": AlertType.INVENTORY,
            "severity": AlertSeverity.WARNING,
            "title": "클렌징밤 재고 주의",
            "message": "쿠팡 채널의 클렌징밤 재고가 낮습니다. 재고 보충을 검토해주세요.",
            "channel": "coupang",
            "acknowledged": False,
        },
        {
            "alert_type": AlertType.INVENTORY,
            "severity": AlertSeverity.WARNING,
            "title": "히알루론산 토너 재고 주의",
            "message": "카카오 채널의 히알루론산 토너 재고가 낮습니다. 16일 분량만 남았습니다.",
            "channel": "kakao",
            "acknowledged": False,
        },
        {
            "alert_type": AlertType.PROMOTION,
            "severity": AlertSeverity.INFO,
            "title": "설 프로모션 D-3",
            "message": "설 선물세트 프로모션 시작까지 3일 남았습니다. 최종 점검을 진행해주세요.",
            "channel": None,
            "acknowledged": False,
        },
    ]

    count = 0
    for data in alerts_data:
        alert = Alert(**data)
        session.add(alert)
        count += 1

    await session.flush()
    print(f"Created {count} alerts.")


async def seed_all() -> None:
    """Run all seed functions."""
    print("Starting database seed...")

    async with async_session() as session:
        # Create products first
        products = await seed_products(session)

        # Create inventories for products
        await seed_inventories(session, products)

        # Create promotions
        promotions = await seed_promotions(session)

        # Create calendar events
        await seed_calendar_events(session, promotions)

        # Create milestones
        await seed_milestones(session, promotions)

        # Create budgets
        await seed_budgets(session, promotions)

        # Create alerts
        await seed_alerts(session)

        await session.commit()

    print("\nSeed completed successfully!")


async def reset_and_seed() -> None:
    """Drop all tables, recreate them, and seed data."""
    print("Resetting database...")
    await drop_tables()
    await create_tables()
    await seed_all()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        asyncio.run(reset_and_seed())
    elif len(sys.argv) > 1 and sys.argv[1] == "--create-tables":
        asyncio.run(create_tables())
    else:
        print("Usage:")
        print("  python -m backend.db.seed --create-tables  # Create tables only")
        print("  python -m backend.db.seed --reset          # Drop, create tables, and seed data")
