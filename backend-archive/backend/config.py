"""Configuration settings for Promotor backend."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "Promotor"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: Literal["development", "staging", "production"] = "development"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # LLM Configuration
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    default_llm_provider: Literal["openai", "anthropic"] = "openai"
    default_model: str = "gpt-4o"
    mini_model: str = "gpt-4o-mini"  # For cost optimization

    # Database (Supabase/PostgreSQL)
    database_url: str = ""
    supabase_url: str = ""
    supabase_key: str = ""

    # Redis
    redis_url: str = "redis://localhost:6379"
    cache_ttl_seconds: int = 3600  # 1 hour default

    # Vector Store (Pinecone)
    pinecone_api_key: str = ""
    pinecone_environment: str = ""
    pinecone_index_name: str = "promotor-vectors"

    # Scraping Configuration
    scraping_proxy_url: str | None = None
    scraping_base_delay: float = 3.0
    scraping_max_requests_per_hour: int = 100

    # Channel API Keys
    coupang_access_key: str = ""
    coupang_secret_key: str = ""
    naver_client_id: str = ""
    naver_client_secret: str = ""
    kakao_admin_key: str = ""

    # Celery
    celery_broker_url: str = Field(default="redis://localhost:6379/0")
    celery_result_backend: str = Field(default="redis://localhost:6379/0")

    # Token Cost Optimization
    enable_caching: bool = True
    enable_tiered_models: bool = True
    background_job_interval_hours: int = 4


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Scraping configurations per channel
CHANNEL_SCRAPING_CONFIG = {
    "oliveyoung": {
        "base_delay": 5,
        "random_delay": (2, 8),
        "max_requests_per_hour": 50,
        "use_proxy": True,
    },
    "coupang": {
        "base_delay": 3,
        "random_delay": (1, 5),
        "max_requests_per_hour": 100,
        "use_proxy": False,  # Prefer official API
    },
    "naver": {
        "base_delay": 3,
        "random_delay": (1, 4),
        "max_requests_per_hour": 100,
        "use_proxy": False,  # Prefer official API
    },
    "kakao": {
        "base_delay": 2,
        "random_delay": (1, 3),
        "max_requests_per_hour": 150,
        "use_proxy": False,  # Prefer official API
    },
}

# Model tier configuration for cost optimization
MODEL_TIERS = {
    "tier1_free": {
        "description": "No LLM call - database queries, API calls, cache retrieval",
        "tasks": ["price_check", "inventory_status", "simple_metrics", "cached_data"],
    },
    "tier2_cheap": {
        "model": "gpt-4o-mini",  # or "claude-3-haiku"
        "description": "Small model for routine tasks",
        "tasks": ["classification", "simple_summarization", "data_formatting", "validation"],
    },
    "tier3_full": {
        "model": "gpt-4o",  # or "claude-3-5-sonnet"
        "description": "Full model for complex analysis",
        "tasks": ["complex_analysis", "strategic_planning", "multi_step_reasoning", "user_response"],
    },
}
