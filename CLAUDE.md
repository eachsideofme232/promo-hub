# CLAUDE.md - Promotor AI Agent Guidelines

This document provides essential context for AI assistants working on the Promotor codebase.

## Project Overview

Promotor is a **Bloomberg Terminal-style Beauty Brand Promotion Manager powered by AI Agents**. It's a multi-agent system designed for managing K-beauty (Korean beauty) brand promotions across multiple e-commerce channels (Oliveyoung, Coupang, Naver, Kakao).

The system orchestrates **21 specialized AI agents** organized into **5 divisions** to handle strategic planning, market intelligence, channel management, analytics, and operations.

## Technology Stack

### Backend (Python)
- **Framework**: FastAPI 0.115+ with async support
- **Agent Orchestration**: LangChain 0.3+ and LangGraph 0.2+ (graph-based multi-agent coordination)
- **LLM Providers**: OpenAI (gpt-4o, gpt-4o-mini) and Anthropic Claude
- **Database**: PostgreSQL 15 (via Supabase) with SQLAlchemy 2.0 + AsyncPG
- **Cache/Queue**: Redis 7 for caching and Celery broker
- **Vector Store**: Pinecone for semantic search embeddings
- **Task Queue**: Celery 5.4+ with Redis
- **Web Scraping**: Playwright with stealth mode, httpx, BeautifulSoup4
- **ML/NLP**: PyTorch, Transformers, sentence-transformers, Prophet, scikit-learn

### Frontend (Next.js/React)
- **Framework**: Next.js 14.2.0 (App Router)
- **UI Components**: Radix UI (Dialog, Dropdown, Tabs, Tooltip, Scroll)
- **State Management**: Zustand 4.5
- **Charts**: Recharts 2.12
- **Real-time**: Socket.IO 4.7
- **Styling**: Tailwind CSS 3.4
- **Icons**: Lucide React

## Directory Structure

```
/home/user/promotor/
├── backend/                              # Python FastAPI backend
│   ├── agents/                           # Multi-agent system
│   │   ├── base.py                       # BaseAgent & BaseDivisionSupervisor classes
│   │   ├── chief_coordinator.py          # Main orchestrator agent
│   │   ├── divisions/                    # 5 specialized divisions
│   │   │   ├── strategic_planning/       # 3 agents: planner, timeline, budget
│   │   │   ├── market_intelligence/      # 4 agents: news, competitor, ingredient, seasonal
│   │   │   ├── channel_management/       # 5 agents: oliveyoung, coupang, naver, kakao, syncer
│   │   │   ├── analytics/                # 7 agents: sentiment, review, bundle, margin, etc.
│   │   │   └── operations/               # 3 agents: price, inventory, checklist
│   │   └── tools/                        # Shared agent tools
│   │       └── common_tools.py           # Utilities (currency, dates, caching, logging)
│   ├── api/                              # FastAPI routes
│   │   ├── main.py                       # App entry point (CORS, lifespan)
│   │   ├── websocket.py                  # WebSocket handlers
│   │   └── routes/                       # API route modules
│   │       ├── chat.py                   # /api/chat endpoints
│   │       ├── agents.py                 # /api/agents endpoints
│   │       ├── dashboard.py              # /api/dashboard endpoints
│   │       └── health.py                 # Health check
│   ├── graph/                            # LangGraph orchestration
│   │   ├── state.py                      # Central state (TypedDict)
│   │   ├── routing.py                    # Task classification & routing
│   │   └── main_graph.py                 # Graph construction & execution
│   └── config.py                         # Environment configuration (Pydantic)
├── frontend/                             # Next.js React frontend
│   ├── src/
│   │   ├── app/                          # Next.js App Router pages
│   │   └── components/dashboard/         # Terminal-style UI components
├── docker-compose.yml                    # Multi-container orchestration
├── pyproject.toml                        # Python project config
└── .env.example                          # Environment variables template
```

## Development Commands

### Backend Development
```bash
# Install dependencies
pip install -e ".[dev]"

# Run development server
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000

# Run Celery worker (background tasks)
celery -A backend.tasks.celery_app worker --loglevel=info

# Run Celery beat (scheduled tasks)
celery -A backend.tasks.celery_app beat --loglevel=info
```

### Frontend Development
```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Lint code
npm run lint
```

### Docker Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Rebuild specific service
docker-compose up -d --build backend
```

### Code Quality
```bash
# Python linting (Ruff)
ruff check backend/
ruff format backend/

# Python type checking (MyPy)
mypy backend/

# Run tests
pytest tests/
```

## Code Conventions

### Python Style
- **Line length**: 100 characters
- **Python version**: 3.11+
- **Linting**: Ruff with rules E, F, I, N, W, UP (E501 ignored)
- **Type checking**: MyPy strict mode enabled
- **Imports**: Use `from __future__ import annotations` for forward references
- **Async**: Prefer async functions for I/O operations

### Agent Implementation Pattern
Every agent follows this structure:

```python
class SpecializedAgent(BaseAgent):
    name = "agent_name"
    role = "Agent Role Description"
    description = "What this agent does"
    division = Division.DIVISION_NAME

    def __init__(self, llm: BaseChatModel, tools: Sequence[BaseTool] | None = None):
        default_tools = [tool1, tool2, ...]
        super().__init__(llm, default_tools + (tools or []))

    @property
    def system_prompt(self) -> str:
        return """Detailed system prompt defining agent behavior..."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        result = await super().process(state, messages)
        return {..., "division": self.division.value}
```

### State Management (LangGraph)
- Central state is defined in `backend/graph/state.py` as `PromotorStateDict`
- Uses `add_messages` reducer for conversation history
- State includes: messages, routing info, task classification, division results, error handling
- Always use TypedDict for LangGraph compatibility

### API Route Pattern
```python
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/")
async def endpoint_name(request: RequestModel) -> ResponseModel:
    # Implementation
    pass
```

## Key Architectural Patterns

### Multi-Agent Hierarchy
1. **Chief Coordinator** (top-level) - Analyzes requests, classifies tasks, routes to divisions
2. **Division Supervisors** (5 total) - Coordinate agents within their division
3. **Specialized Agents** (21 total) - Process specific task types

### Task Classification & Routing
- Keyword-based classification in `backend/graph/routing.py`
- Routes to single or multiple divisions based on query patterns
- Supports multi-division workflows for complex tasks

### Cost Optimization (Model Tiers)
```python
Tier1_free: Database queries, API calls, cache retrieval (no LLM)
Tier2_cheap: gpt-4o-mini or claude-3-haiku for routine tasks
Tier3_full: gpt-4o or claude-3-5-sonnet for complex analysis
```

## API Endpoints

```
POST   /api/chat/                    # Send message to agent system
POST   /api/chat/stream              # Stream agent responses (SSE)
GET    /api/chat/history/{conv_id}   # Get conversation history
DELETE /api/chat/history/{conv_id}   # Clear conversation

GET    /api/agents/                  # List all agents
GET    /api/agents/{division}        # Get agents for division
GET    /api/agents/{division}/{name} # Get specific agent details

GET    /api/dashboard/metrics        # Dashboard KPIs
GET    /api/dashboard/channels       # Channel overview
GET    /api/dashboard/alerts         # Active alerts
GET    /api/dashboard/promotions     # Active/upcoming promotions

GET    /health                       # Health check
```

## Environment Variables

Required environment variables (see `.env.example`):

```bash
# LLM API Keys
OPENAI_API_KEY=
ANTHROPIC_API_KEY=

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/promotor
SUPABASE_URL=
SUPABASE_KEY=

# Redis
REDIS_URL=redis://localhost:6379

# Vector Store
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=

# Channel APIs (optional)
COUPANG_ACCESS_KEY=
COUPANG_SECRET_KEY=
NAVER_CLIENT_ID=
NAVER_CLIENT_SECRET=
KAKAO_ADMIN_KEY=
```

## Enums and Constants

### Divisions (`backend/graph/state.py`)
- `STRATEGIC_PLANNING` - Promotion planning, timelines, budgets
- `MARKET_INTELLIGENCE` - News, competitors, ingredients, seasonal trends
- `CHANNEL_MANAGEMENT` - Oliveyoung, Coupang, Naver, Kakao operations
- `ANALYTICS` - Sentiment, margins, bundles, attribution, predictions
- `OPERATIONS` - Price monitoring, inventory, checklists

### Channels
- `OLIVEYOUNG` - Korea's largest H&B retailer
- `COUPANG` - Korea's largest e-commerce (Rocket delivery)
- `NAVER` - Smart Store marketplace
- `KAKAO` - Kakao shopping/gifts

### Task Types (20+)
See `backend/graph/state.py` for full TaskType enum including:
- `PROMOTION_PLANNING`, `TIMELINE_MANAGEMENT`, `BUDGET_ALLOCATION`
- `NEWS_SCOUTING`, `COMPETITOR_ANALYSIS`, `INGREDIENT_TRENDS`
- `SENTIMENT_ANALYSIS`, `MARGIN_CALCULATION`, `STOCKOUT_PREDICTION`
- And more...

## Korean Language Support

This codebase has extensive Korean language support:
- Keyword matching includes Korean terms (e.g., "프로모션", "계획", "재고")
- Currency formatting: Korean won (원, 만, 억)
- Korean date/calendar events (Chuseok, Lunar New Year, etc.)
- Korean NLP processing for sentiment analysis

## Common Tasks

### Adding a New Agent
1. Create agent file in appropriate division: `backend/agents/divisions/{division}/{agent_name}.py`
2. Inherit from `BaseAgent` and implement required properties
3. Define tools using `@tool` decorator
4. Register agent with the division supervisor
5. Update routing in `backend/graph/routing.py` if needed

### Adding a New API Endpoint
1. Create route in `backend/api/routes/` or add to existing router
2. Define Pydantic models for request/response
3. Include router in `backend/api/main.py`

### Modifying LangGraph Flow
1. Update state in `backend/graph/state.py` if needed
2. Modify routing logic in `backend/graph/routing.py`
3. Update graph construction in `backend/graph/main_graph.py`

## Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=backend

# Run async tests
pytest tests/ -v  # asyncio_mode="auto" is configured
```

## Docker Services

The `docker-compose.yml` defines:
- `backend` - FastAPI app (port 8000)
- `frontend` - Next.js app (port 3000)
- `db` - PostgreSQL 15 (port 5432)
- `redis` - Redis 7 (port 6379)
- `celery_worker` - Background task processor
- `celery_beat` - Scheduled task scheduler

## Notes for AI Assistants

1. **Always check existing patterns** - This codebase has consistent patterns; follow them when adding new code
2. **Async first** - Use `async/await` for I/O operations
3. **Type safety** - Use type hints everywhere; MyPy strict mode is enabled
4. **Korean support** - When adding features, consider both English and Korean users
5. **Cost optimization** - Consider which model tier is appropriate for new features
6. **State management** - Always work through `PromotorStateDict` for LangGraph operations
7. **Tool definitions** - Use LangChain's `@tool` decorator for agent tools
