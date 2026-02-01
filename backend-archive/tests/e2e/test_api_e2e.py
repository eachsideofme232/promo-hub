"""End-to-end tests for API endpoints."""

import pytest


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, api_client):
        """Test that health endpoint returns OK."""
        response = api_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestAgentsEndpoint:
    """Test agents API endpoints."""

    def test_list_all_agents(self, api_client):
        """Test listing all agents."""
        response = api_client.get("/api/agents/")
        assert response.status_code == 200
        data = response.json()
        assert "divisions" in data
        assert "total_agents" in data
        # Should have 21 agents across 5 divisions
        assert data["total_agents"] == 21
        assert len(data["divisions"]) == 5

    def test_list_agents_by_division(self, api_client):
        """Test listing agents for a specific division."""
        divisions = [
            "strategic_planning",
            "market_intelligence",
            "channel_management",
            "analytics",
            "operations",
        ]

        for division in divisions:
            response = api_client.get(f"/api/agents/{division}")
            assert response.status_code == 200
            data = response.json()
            assert "agents" in data
            assert len(data["agents"]) > 0

    def test_invalid_division_returns_error(self, api_client):
        """Test that invalid division returns error message."""
        response = api_client.get("/api/agents/invalid_division")
        assert response.status_code == 200
        data = response.json()
        assert "error" in data


class TestDashboardEndpoint:
    """Test dashboard API endpoints."""

    def test_get_metrics(self, api_client):
        """Test getting dashboard metrics."""
        response = api_client.get("/api/dashboard/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data
        assert "total_sales" in data["metrics"]
        assert "active_promotions" in data["metrics"]

    def test_get_channels(self, api_client):
        """Test getting channel overview."""
        response = api_client.get("/api/dashboard/channels")
        assert response.status_code == 200
        data = response.json()
        assert "channels" in data
        # Should have 4 channels
        assert len(data["channels"]) == 4

    def test_get_alerts(self, api_client):
        """Test getting active alerts."""
        response = api_client.get("/api/dashboard/alerts")
        assert response.status_code == 200
        data = response.json()
        assert "alerts" in data

    def test_get_promotions(self, api_client):
        """Test getting promotions."""
        response = api_client.get("/api/dashboard/promotions")
        assert response.status_code == 200
        data = response.json()
        assert "active" in data
        assert "upcoming" in data
