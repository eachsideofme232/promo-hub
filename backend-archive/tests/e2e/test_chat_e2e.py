"""End-to-end tests for chat functionality with LLM integration."""

import pytest


class TestChatEndpoint:
    """Test chat API endpoints."""

    def test_chat_basic_message(self, api_client):
        """Test sending a basic chat message."""
        response = api_client.post(
            "/api/chat/",
            json={
                "message": "Hello, what can you help me with?",
                "user_id": "test_user",
                "brand_id": "test_brand",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "conversation_id" in data

    def test_chat_promotion_planning_query(self, api_client):
        """Test a promotion planning query routes to correct division."""
        response = api_client.post(
            "/api/chat/",
            json={
                "message": "Plan Q2 sunscreen promotions",
                "user_id": "test_user",
                "brand_id": "test_brand",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        # Should route to strategic planning division
        if "divisions_used" in data:
            assert "strategic_planning" in data["divisions_used"]

    def test_chat_channel_query(self, api_client):
        """Test a channel-specific query."""
        response = api_client.post(
            "/api/chat/",
            json={
                "message": "Check Oliveyoung rankings",
                "user_id": "test_user",
                "brand_id": "test_brand",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_chat_analytics_query(self, api_client):
        """Test an analytics query."""
        response = api_client.post(
            "/api/chat/",
            json={
                "message": "Analyze last month's promotion performance",
                "user_id": "test_user",
                "brand_id": "test_brand",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_chat_inventory_query(self, api_client):
        """Test an inventory/operations query."""
        response = api_client.post(
            "/api/chat/",
            json={
                "message": "Show inventory alerts",
                "user_id": "test_user",
                "brand_id": "test_brand",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_chat_competitor_query(self, api_client):
        """Test a competitor analysis query."""
        response = api_client.post(
            "/api/chat/",
            json={
                "message": "What are competitors doing this week?",
                "user_id": "test_user",
                "brand_id": "test_brand",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_chat_korean_message(self, api_client):
        """Test chat with Korean language input."""
        response = api_client.post(
            "/api/chat/",
            json={
                "message": "다음 분기 프로모션 계획 세워줘",
                "user_id": "test_user",
                "brand_id": "test_brand",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_chat_missing_message_returns_error(self, api_client):
        """Test that missing message field returns error."""
        response = api_client.post(
            "/api/chat/",
            json={
                "user_id": "test_user",
                "brand_id": "test_brand",
            },
        )
        assert response.status_code == 422  # Validation error


class TestChatHistory:
    """Test chat history endpoints."""

    def test_get_conversation_history(self, api_client):
        """Test getting conversation history."""
        # First create a conversation
        create_response = api_client.post(
            "/api/chat/",
            json={
                "message": "Hello",
                "user_id": "test_user",
                "brand_id": "test_brand",
            },
        )
        assert create_response.status_code == 200
        conv_id = create_response.json().get("conversation_id")

        if conv_id:
            # Then get history
            response = api_client.get(f"/api/chat/history/{conv_id}")
            assert response.status_code == 200
            data = response.json()
            assert "messages" in data

    def test_delete_conversation(self, api_client):
        """Test deleting a conversation."""
        # First create a conversation
        create_response = api_client.post(
            "/api/chat/",
            json={
                "message": "Hello",
                "user_id": "test_user",
                "brand_id": "test_brand",
            },
        )
        assert create_response.status_code == 200
        conv_id = create_response.json().get("conversation_id")

        if conv_id:
            # Then delete it
            response = api_client.delete(f"/api/chat/history/{conv_id}")
            assert response.status_code in [200, 204]
