"""Pytest configuration and fixtures for e2e tests."""

import os
import pytest
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@pytest.fixture(scope="session")
def backend_url():
    """Backend API base URL."""
    return os.getenv("BACKEND_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def api_client(backend_url):
    """HTTP client for API requests."""
    with httpx.Client(base_url=backend_url, timeout=30.0) as client:
        yield client


@pytest.fixture(scope="session")
def async_api_client(backend_url):
    """Async HTTP client for API requests."""
    return httpx.AsyncClient(base_url=backend_url, timeout=30.0)


@pytest.fixture
def openai_api_key():
    """Get OpenAI API key from environment."""
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        pytest.skip("OPENAI_API_KEY not set")
    return key
