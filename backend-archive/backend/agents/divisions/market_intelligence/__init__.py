"""Market Intelligence Division - News, competitors, ingredients, and seasonal analysis."""

from backend.agents.divisions.market_intelligence.supervisor import (
    MarketIntelligenceSupervisor,
    create_market_intelligence_division,
)
from backend.agents.divisions.market_intelligence.news_scout import IndustryNewsScout
from backend.agents.divisions.market_intelligence.competitor_watcher import CompetitorWatcher
from backend.agents.divisions.market_intelligence.ingredient_analyst import IngredientTrendAnalyst
from backend.agents.divisions.market_intelligence.seasonal_analyst import SeasonalPatternAnalyst

__all__ = [
    "MarketIntelligenceSupervisor",
    "IndustryNewsScout",
    "CompetitorWatcher",
    "IngredientTrendAnalyst",
    "SeasonalPatternAnalyst",
    "create_market_intelligence_division",
]
