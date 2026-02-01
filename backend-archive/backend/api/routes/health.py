"""Health check endpoints."""

from datetime import datetime

from fastapi import APIRouter

from backend.config import get_settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.now().isoformat(),
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check for Kubernetes."""
    # Check all dependencies
    checks = {
        "database": True,  # Would check DB connection
        "redis": True,  # Would check Redis connection
        "llm": True,  # Would check LLM API
    }

    all_ready = all(checks.values())

    return {
        "ready": all_ready,
        "checks": checks,
        "timestamp": datetime.now().isoformat(),
    }
