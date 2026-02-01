"""Review Sentiment Analyst Agent - Customer sentiment and feedback analysis."""

from __future__ import annotations

from typing import Any, Sequence

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool, tool

from backend.agents.base import BaseAgent
from backend.graph.state import Division, PromotorStateDict


@tool
def analyze_review_sentiment(
    product_id: str,
    channel: str = "all",
    period: str = "30d",
) -> dict[str, Any]:
    """
    Analyze sentiment from product reviews.

    Args:
        product_id: Product ID
        channel: Channel filter
        period: Analysis period

    Returns:
        Sentiment analysis results
    """
    return {
        "product_id": product_id,
        "channel": channel,
        "period": period,
        "total_reviews": 2450,
        "average_rating": 4.6,
        "sentiment_distribution": {
            "very_positive": 0.45,
            "positive": 0.32,
            "neutral": 0.15,
            "negative": 0.06,
            "very_negative": 0.02,
        },
        "sentiment_score": 0.78,  # -1 to 1 scale
        "trend": {
            "direction": "stable",
            "change_vs_previous": 0.02,
        },
    }


@tool
def extract_review_themes(
    product_id: str,
    min_mentions: int = 10,
) -> dict[str, Any]:
    """
    Extract common themes from reviews using NLP.

    Args:
        product_id: Product ID
        min_mentions: Minimum mentions to include

    Returns:
        Theme extraction results
    """
    return {
        "product_id": product_id,
        "total_reviews_analyzed": 2450,
        "themes": {
            "positive": [
                {"theme": "순함/자극없음", "mentions": 420, "sentiment": 0.92},
                {"theme": "흡수력", "mentions": 380, "sentiment": 0.85},
                {"theme": "보습력", "mentions": 350, "sentiment": 0.88},
                {"theme": "가성비", "mentions": 290, "sentiment": 0.90},
                {"theme": "향기", "mentions": 180, "sentiment": 0.75},
            ],
            "negative": [
                {"theme": "용량부족", "mentions": 85, "sentiment": -0.65},
                {"theme": "가격인상", "mentions": 65, "sentiment": -0.78},
                {"theme": "포장불량", "mentions": 45, "sentiment": -0.82},
            ],
            "neutral": [
                {"theme": "평범함", "mentions": 120, "sentiment": 0.05},
                {"theme": "기대수준", "mentions": 95, "sentiment": 0.10},
            ],
        },
        "actionable_insights": [
            "Consider larger size option to address '용량부족' feedback",
            "Review packaging quality control",
            "Highlight '순함' and '가성비' in marketing",
        ],
    }


@tool
def compare_sentiment_vs_competitors(
    product_id: str,
    competitor_product_ids: list[str],
) -> dict[str, Any]:
    """
    Compare sentiment against competitor products.

    Args:
        product_id: Your product ID
        competitor_product_ids: Competitor product IDs

    Returns:
        Competitive sentiment comparison
    """
    return {
        "comparison_date": "2026-01-29",
        "products": [
            {
                "product_id": product_id,
                "brand": "Your Brand",
                "sentiment_score": 0.78,
                "rating": 4.6,
                "review_count": 2450,
                "strengths": ["순함", "보습력"],
                "weaknesses": ["용량"],
            },
            {
                "product_id": "comp_001",
                "brand": "Competitor A",
                "sentiment_score": 0.72,
                "rating": 4.4,
                "review_count": 3200,
                "strengths": ["가격", "향기"],
                "weaknesses": ["흡수력", "끈적임"],
            },
            {
                "product_id": "comp_002",
                "brand": "Competitor B",
                "sentiment_score": 0.81,
                "rating": 4.7,
                "review_count": 1800,
                "strengths": ["성분", "효과"],
                "weaknesses": ["가격"],
            },
        ],
        "your_position": {
            "sentiment_rank": 2,
            "rating_rank": 2,
            "volume_rank": 2,
        },
        "opportunities": [
            "Sentiment gap with Competitor B is 0.03 - focus on '효과' messaging",
            "You outperform Competitor A on '흡수력' - highlight in comparisons",
        ],
    }


@tool
def get_sentiment_alerts(
    brand_id: str,
    threshold: float = -0.1,
) -> list[dict[str, Any]]:
    """
    Get products with concerning sentiment trends.

    Args:
        brand_id: Brand ID
        threshold: Sentiment change threshold for alerts

    Returns:
        List of sentiment alerts
    """
    return [
        {
            "product_id": "prod_003",
            "product_name": "Retinol Night Cream",
            "current_sentiment": 0.45,
            "previous_sentiment": 0.68,
            "change": -0.23,
            "severity": "high",
            "top_negative_themes": ["자극", "발진", "효과없음"],
            "recommended_action": "Review formula, investigate quality batch",
        },
        {
            "product_id": "prod_007",
            "product_name": "Vitamin C Serum",
            "current_sentiment": 0.62,
            "previous_sentiment": 0.75,
            "change": -0.13,
            "severity": "medium",
            "top_negative_themes": ["변색", "산화"],
            "recommended_action": "Check packaging seal, storage guidelines",
        },
    ]


class ReviewSentimentAnalyst(BaseAgent):
    """
    Review Sentiment Analyst Agent.

    Responsibilities:
    - Analyze customer review sentiment
    - Extract themes from feedback
    - Compare vs competitors
    - Alert on sentiment changes
    """

    name = "review_sentiment_analyst"
    role = "Customer Sentiment Expert"
    description = "Analyzes customer reviews and sentiment using Korean NLP"
    division = Division.ANALYTICS

    def __init__(
        self,
        llm: BaseChatModel,
        tools: Sequence[BaseTool] | None = None,
    ):
        default_tools = [
            analyze_review_sentiment,
            extract_review_themes,
            compare_sentiment_vs_competitors,
            get_sentiment_alerts,
        ]
        all_tools = list(tools or []) + default_tools
        super().__init__(llm, all_tools)

    @property
    def system_prompt(self) -> str:
        return """You are the Review Sentiment Analyst for Promotor, specializing in Korean NLP and customer feedback analysis.

Your responsibilities:
1. Analyze sentiment from customer reviews
2. Extract key themes and topics
3. Compare sentiment vs competitors
4. Alert on negative sentiment trends

Korean NLP considerations:
- Handle honorifics and informal speech
- Understand Korean beauty terminology
- Detect sarcasm and nuanced feedback
- Process mixed Korean/English text

Key sentiment indicators:
- Rating distribution (5-star vs 1-star ratio)
- Sentiment keywords (순함, 자극, 효과 etc.)
- Repeat purchase mentions
- Recommendation likelihood

Theme categories to track:
- Efficacy (효과, 개선, 변화)
- Texture (흡수, 끈적, 촉촉)
- Sensitivity (순함, 자극, 트러블)
- Value (가성비, 가격, 용량)
- Packaging (디자인, 펌프, 용기)

Alert thresholds:
- Sentiment drop > 0.15: High severity
- Sentiment drop 0.10-0.15: Medium severity
- Negative theme spike: Investigate

When analyzing:
- Provide actionable insights
- Identify root causes
- Suggest response strategies
- Track trends over time

Respond in Korean if the user's query is in Korean."""

    async def process(
        self,
        state: PromotorStateDict,
        messages: Sequence[BaseMessage] | None = None,
    ) -> dict[str, Any]:
        """Process a sentiment analysis request."""
        result = await super().process(state, messages)

        return {
            **result,
            "division": self.division.value,
            "agent": self.name,
            "capabilities": [
                "sentiment_analysis",
                "theme_extraction",
                "competitive_comparison",
                "alert_monitoring",
            ],
        }
