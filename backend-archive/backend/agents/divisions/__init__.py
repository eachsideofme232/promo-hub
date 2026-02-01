"""Division supervisors and agents for Promotor."""

from backend.agents.divisions.analytics import AnalyticsSupervisor
from backend.agents.divisions.channel_management import ChannelManagementSupervisor
from backend.agents.divisions.market_intelligence import MarketIntelligenceSupervisor
from backend.agents.divisions.operations import OperationsSupervisor
from backend.agents.divisions.strategic_planning import StrategicPlanningSupervisor

__all__ = [
    "StrategicPlanningSupervisor",
    "MarketIntelligenceSupervisor",
    "ChannelManagementSupervisor",
    "AnalyticsSupervisor",
    "OperationsSupervisor",
]
