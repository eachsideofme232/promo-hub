# Promotor

**Bloomberg Terminal-style Beauty Brand Promotion Manager powered by AI Agents**

A multi-agent system for managing K-beauty brand promotions across Oliveyoung, Coupang, Naver, and Kakao channels.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-14.2-black.svg)

---

## Features

- **21 AI Agents** organized into 5 specialized divisions
- **Multi-channel management** - Oliveyoung, Coupang, Naver, Kakao
- **Bloomberg Terminal-style UI** - Dark theme with real-time dashboard
- **Korean language support** - Full Korean NLP and keyword matching
- **Cost-optimized** - Tiered model usage (GPT-4o-mini for routine, GPT-4o for complex)

---

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API key (required)

### 1. Clone the Repository

```bash
git clone https://github.com/eachsideofme232/promotor.git
cd promotor
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

```bash
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Install Backend Dependencies

**Option A: Full installation (includes ML/NLP)**
```bash
pip install -e .
```

**Option B: Core only (lighter, faster install)**
```bash
pip install fastapi uvicorn langchain-core langchain langgraph httpx python-dotenv
```

### 4. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 5. Run the Application

**Terminal 1 - Backend:**
```bash
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 6. Open in Browser

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Usage Guide

### Dashboard Navigation

Use keyboard shortcuts or click the buttons at the bottom:

| Shortcut | Panel       | Description                          |
|----------|-------------|--------------------------------------|
| Alt+1    | Help        | Keyboard shortcuts and commands      |
| Alt+2    | Calendar    | AI Assistant chat (default)          |
| Alt+3    | Analytics   | Performance metrics and charts       |
| Alt+4    | Channels    | Channel status and management        |
| Alt+5    | Inventory   | Stock monitoring and alerts          |
| Alt+6    | Budget      | Budget allocation and tracking       |
| Alt+7    | Competitors | Competitive intelligence             |
| Alt+8    | Settings    | System configuration                 |

### AI Assistant Commands

Type in the chat input to interact with the AI agents:

```
"Plan Q2 sunscreen promotions"
"Check Oliveyoung rankings"
"Analyze last month's performance"
"Show inventory alerts"
"What are competitors doing?"
```

Korean language is also supported:

```
"다음 분기 프로모션 계획 세워줘"
"올리브영 순위 확인해줘"
"재고 현황 알려줘"
```

---

## Architecture

### Agent Divisions

```
                    Chief Coordinator
                          │
    ┌─────────┬───────────┼───────────┬─────────┐
    │         │           │           │         │
Strategic  Market    Channel    Analytics  Operations
Planning   Intel    Management
(3 agents) (4 agents) (5 agents) (7 agents) (3 agents)
```

| Division | Agents | Responsibilities |
|----------|--------|------------------|
| Strategic Planning | 3 | Promotion planning, timelines, budgets |
| Market Intelligence | 4 | News, competitors, ingredients, trends |
| Channel Management | 5 | Oliveyoung, Coupang, Naver, Kakao ops |
| Analytics | 7 | Sentiment, margins, bundles, forecasting |
| Operations | 3 | Inventory, pricing, checklists |

### Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, LangChain, LangGraph |
| Frontend | Next.js 14, Tailwind CSS, Radix UI |
| LLM | OpenAI GPT-4o / Anthropic Claude |
| Database | PostgreSQL (optional) |
| Cache | Redis (optional) |

---

## API Reference

### Chat

```bash
# Send a message
curl -X POST http://localhost:8000/api/chat/ \
  -H "Content-Type: application/json" \
  -d '{"message": "Plan Q2 promotions", "user_id": "user1", "brand_id": "brand1"}'
```

### Agents

```bash
# List all agents
curl http://localhost:8000/api/agents/

# List agents by division
curl http://localhost:8000/api/agents/strategic_planning
```

### Dashboard

```bash
# Get metrics
curl http://localhost:8000/api/dashboard/metrics

# Get channel status
curl http://localhost:8000/api/dashboard/channels

# Get alerts
curl http://localhost:8000/api/dashboard/alerts
```

---

## Development

### Running Tests

```bash
# Run all e2e tests
pytest tests/e2e/ -v

# Run with coverage
pytest tests/ --cov=backend
```

### Code Quality

```bash
# Python linting
ruff check backend/
ruff format backend/

# Type checking
mypy backend/
```

### Docker (Full Stack)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down
```

---

## Project Structure

```
promotor/
├── backend/
│   ├── agents/              # 21 AI agents in 5 divisions
│   ├── api/                 # FastAPI routes
│   ├── graph/               # LangGraph orchestration
│   └── config.py            # Configuration
├── frontend/
│   └── src/
│       ├── app/             # Next.js pages
│       └── components/      # Dashboard UI components
├── tests/
│   └── e2e/                 # End-to-end tests
├── docker-compose.yml
├── pyproject.toml
└── .env.example
```

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `ANTHROPIC_API_KEY` | No | Anthropic API key (optional) |
| `DATABASE_URL` | No | PostgreSQL connection string |
| `REDIS_URL` | No | Redis connection string |

See `.env.example` for full list.

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

- Built with [LangChain](https://langchain.com/) and [LangGraph](https://langchain-ai.github.io/langgraph/)
- UI inspired by Bloomberg Terminal
- Designed for K-beauty brand managers
