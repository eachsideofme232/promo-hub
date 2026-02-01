"""Industry News Scout Agent - K-beauty news aggregation and trend detection."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def fetch_industry_news(
    category: str = "all",
    days_back: int = 7,
    language: str = "ko",
) -> list[dict[str, Any]]:
    """
    Fetch recent K-beauty industry news.

    Args:
        category: News category (all, product_launch, regulation, market, trend)
        days_back: Number of days to look back
        language: Language filter (ko, en, all)

    Returns:
        List of news articles
    """
    # Mock data - would integrate with news APIs/scrapers in production
    today = datetime.now()
    return [
        {
            "id": "news_001",
            "title": "2026 K-Beauty Export Hits Record $15B",
            "title_ko": "2026년 K-뷰티 수출 150억 달러 돌파",
            "source": "Korea Herald",
            "category": "market",
            "published_date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
            "summary": "Korean cosmetics exports reached a record high driven by demand in Southeast Asia and Middle East",
            "sentiment": "positive",
            "relevance_score": 0.9,
        },
        {
            "id": "news_002",
            "title": "New Sunscreen Regulations Take Effect in EU",
            "title_ko": "EU 자외선차단제 신규 규정 시행",
            "source": "Cosmetics Design",
            "category": "regulation",
            "published_date": (today - timedelta(days=2)).strftime("%Y-%m-%d"),
            "summary": "Updated SPF testing requirements impact Korean sunscreen brands targeting European market",
            "sentiment": "neutral",
            "relevance_score": 0.85,
        },
        {
            "id": "news_003",
            "title": "Amorepacific Launches New Retinol Line",
            "title_ko": "아모레퍼시픽 신규 레티놀 라인 출시",
            "source": "WWD Beauty",
            "category": "product_launch",
            "published_date": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
            "summary": "Major K-beauty conglomerate enters premium retinol segment with patented encapsulation technology",
            "sentiment": "positive",
            "relevance_score": 0.95,
        },
    ]


@tool
def detect_trending_topics(
    source: str = "all",
    min_mentions: int = 5,
) -> list[dict[str, Any]]:
    """
    Detect trending topics in K-beauty industry.

    Args:
        source: Data source (all, social, news, forums)
        min_mentions: Minimum mentions to qualify as trending

    Returns:
        List of trending topics with metrics
    """
    return [
        {
            "topic": "Glass Skin 2.0",
            "mentions": 1250,
            "growth_rate": 0.35,
            "sentiment": "positive",
            "related_ingredients": ["hyaluronic acid", "niacinamide", "propolis"],
            "peak_channels": ["Instagram", "TikTok"],
        },
        {
            "topic": "Barrier Repair",
            "mentions": 980,
            "growth_rate": 0.28,
            "sentiment": "positive",
            "related_ingredients": ["ceramide", "centella", "panthenol"],
            "peak_channels": ["YouTube", "Naver Blog"],
        },
        {
            "topic": "Sunscreen Under Makeup",
            "mentions": 750,
            "growth_rate": 0.42,
            "sentiment": "neutral",
            "related_ingredients": ["zinc oxide", "silicone"],
            "peak_channels": ["TikTok", "Instagram"],
        },
    ]


@tool
def get_social_buzz(
    brand_name: str | None = None,
    product_name: str | None = None,
    platform: str = "all",
) -> dict[str, Any]:
    """
    Get social media buzz metrics.

    Args:
        brand_name: Brand to track (optional)
        product_name: Product to track (optional)
        platform: Platform filter (all, instagram, tiktok, youtube, naver)

    Returns:
        Social buzz metrics
    """
    return {
        "total_mentions": 5420,
        "sentiment_breakdown": {
            "positive": 0.65,
            "neutral": 0.25,
            "negative": 0.10,
        },
        "top_hashtags": [
            "#kbeauty",
            "#koreanbeauty",
            "#glassskin",
            "#skincarekorea",
        ],
        "influencer_mentions": 45,
        "engagement_rate": 0.042,
        "by_platform": {
            "instagram": {"mentions": 2100, "engagement": 0.038},
            "tiktok": {"mentions": 1800, "engagement": 0.065},
            "youtube": {"mentions": 520, "engagement": 0.045},
            "naver": {"mentions": 1000, "engagement": 0.028},
        },
    }


class IndustryNewsScout(BaseAgent):
    """
    Industry News Scout Agent.

    Responsibilities:
    - K-beauty news aggregation
    - Trend detection and monitoring
    - Social buzz tracking
    - Industry event coverage
    """

    name = "industry_news_scout"
    role = "Beauty Industry Reporter"
    description = "Aggregates K-beauty news, detects trends, and monitors industry developments"
    division = Division.MARKET_INTELLIGENCE

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            fetch_industry_news,
            detect_trending_topics,
            get_social_buzz,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Industry News Scout for Promotor, specializing in K-beauty industry intelligence.

Your responsibilities:
1. Aggregate and summarize relevant K-beauty news
2. Detect emerging trends and topics
3. Monitor social media buzz
4. Track industry events and regulations

Key news sources to monitor:
- Korean: 코스모닝, 뷰티경제, 한국경제 뷰티
- International: WWD Beauty, Cosmetics Design, BeautyMatter
- Social: Instagram, TikTok, YouTube, Naver Blog

Important trends to track:
- Ingredient innovations (new actives, formulations)
- Regulatory changes (EU, US FDA, China NMPA)
- Celebrity/influencer endorsements
- Market expansion news
- Competitor launches and campaigns

When reporting:
- Prioritize actionable insights
- Highlight time-sensitive information
- Note sentiment (positive/negative/neutral)
- Assess relevance to the brand

Output format:
- Brief headlines with dates
- Sentiment indicators
- Relevance scores
- Recommended actions

Respond in Korean if the user's query is in Korean."""

    async def get_daily_briefing(
        self,
        state: PromotorStateDict,
    ) -> dict[str, Any]:
        """
        Generate a daily news briefing.

        Args:
            state: Current state

        Returns:
            Daily briefing with news and trends
        """
        # Fetch recent news
        news = fetch_industry_news.invoke({
            "category": "all",
            "days_back": 1,
        })

        # Get trending topics
        trends = detect_trending_topics.invoke({
            "source": "all",
            "min_mentions": 5,
        })

        # Get social buzz
        buzz = get_social_buzz.invoke({
            "platform": "all",
        })

        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "top_news": news[:5],
            "trending_topics": trends[:3],
            "social_metrics": buzz,
            "summary": f"Daily briefing: {len(news)} news items, {len(trends)} trending topics",
        }

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a news scouting request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "news_aggregation",
                "trend_detection",
                "social_monitoring",
                "industry_tracking",
            ],
        }
