"""Common tools shared across all agents."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta
from typing import Any

from langchain_core.tools import tool


@tool
def cache_result(
    key: str,
    value: Any,
    ttl_seconds: int = 3600,
) -> dict[str, Any]:
    """
    Cache a result for later retrieval.

    Args:
        key: Cache key
        value: Value to cache
        ttl_seconds: Time to live in seconds

    Returns:
        Cache confirmation
    """
    # In production, this would use Redis
    cache_key = hashlib.md5(key.encode()).hexdigest()
    return {
        "status": "cached",
        "key": cache_key,
        "expires_at": (datetime.now() + timedelta(seconds=ttl_seconds)).isoformat(),
    }


@tool
def get_cached_result(
    key: str,
) -> dict[str, Any] | None:
    """
    Retrieve a cached result.

    Args:
        key: Cache key

    Returns:
        Cached value or None
    """
    # In production, this would query Redis
    return None  # Cache miss


@tool
def log_agent_action(
    agent_name: str,
    action_type: str,
    details: dict[str, Any],
) -> dict[str, Any]:
    """
    Log an agent action for auditing.

    Args:
        agent_name: Name of the agent
        action_type: Type of action performed
        details: Action details

    Returns:
        Log confirmation
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "action": action_type,
        "details": details,
    }
    # In production, this would write to a logging service
    return {"logged": True, "entry_id": hashlib.md5(json.dumps(log_entry).encode()).hexdigest()[:12]}


@tool
def format_korean_currency(
    amount: float,
    include_symbol: bool = True,
) -> str:
    """
    Format a number as Korean Won currency.

    Args:
        amount: Amount to format
        include_symbol: Whether to include ₩ symbol

    Returns:
        Formatted currency string
    """
    if amount >= 100_000_000:
        formatted = f"{amount / 100_000_000:.1f}억"
    elif amount >= 10_000:
        formatted = f"{amount / 10_000:.0f}만"
    else:
        formatted = f"{amount:,.0f}"

    return f"₩{formatted}" if include_symbol else formatted


@tool
def format_percentage(
    value: float,
    decimal_places: int = 1,
) -> str:
    """
    Format a decimal as percentage.

    Args:
        value: Decimal value (0.25 = 25%)
        decimal_places: Number of decimal places

    Returns:
        Formatted percentage string
    """
    return f"{value * 100:.{decimal_places}f}%"


@tool
def calculate_date_range(
    period: str,
    reference_date: str | None = None,
) -> dict[str, str]:
    """
    Calculate date range from period string.

    Args:
        period: Period string (7d, 30d, Q1, Q2, etc.)
        reference_date: Optional reference date (defaults to today)

    Returns:
        Start and end dates
    """
    ref = datetime.strptime(reference_date, "%Y-%m-%d") if reference_date else datetime.now()

    period_lower = period.lower()

    if period_lower.endswith("d"):
        days = int(period_lower[:-1])
        start = ref - timedelta(days=days)
        end = ref
    elif period_lower.startswith("q"):
        quarter = int(period_lower[1])
        year = ref.year
        quarter_starts = {1: 1, 2: 4, 3: 7, 4: 10}
        start = datetime(year, quarter_starts[quarter], 1)
        if quarter == 4:
            end = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end = datetime(year, quarter_starts[quarter] + 3, 1) - timedelta(days=1)
    elif period_lower == "ytd":
        start = datetime(ref.year, 1, 1)
        end = ref
    elif period_lower == "mtd":
        start = datetime(ref.year, ref.month, 1)
        end = ref
    else:
        # Default to 30 days
        start = ref - timedelta(days=30)
        end = ref

    return {
        "start_date": start.strftime("%Y-%m-%d"),
        "end_date": end.strftime("%Y-%m-%d"),
        "days": (end - start).days,
    }


# Utility functions (not tools, but helper functions)

def create_query_hash(query: str, params: dict[str, Any]) -> str:
    """Create a hash for caching queries."""
    content = f"{query}:{json.dumps(params, sort_keys=True)}"
    return hashlib.md5(content.encode()).hexdigest()


def is_korean(text: str) -> bool:
    """Check if text contains Korean characters."""
    for char in text:
        if "\uac00" <= char <= "\ud7a3":
            return True
    return False


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def parse_price(price_str: str) -> float:
    """Parse Korean price string to float."""
    # Remove currency symbols and commas
    cleaned = price_str.replace("₩", "").replace(",", "").replace("원", "").strip()

    # Handle Korean number suffixes
    if "억" in cleaned:
        parts = cleaned.split("억")
        return float(parts[0]) * 100_000_000 + (float(parts[1]) if parts[1] else 0)
    elif "만" in cleaned:
        parts = cleaned.split("만")
        return float(parts[0]) * 10_000 + (float(parts[1]) if parts[1] else 0)

    return float(cleaned)
