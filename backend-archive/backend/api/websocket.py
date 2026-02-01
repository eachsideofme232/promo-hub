"""WebSocket handlers for real-time updates."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime
from typing import Any

from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Manages WebSocket connections."""

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        if client_id not in self.active_connections:
            self.active_connections[client_id] = []
        self.active_connections[client_id].append(websocket)

    def disconnect(self, websocket: WebSocket, client_id: str):
        """Remove a WebSocket connection."""
        if client_id in self.active_connections:
            self.active_connections[client_id].remove(websocket)
            if not self.active_connections[client_id]:
                del self.active_connections[client_id]

    async def send_personal_message(self, message: dict[str, Any], client_id: str):
        """Send message to a specific client."""
        if client_id in self.active_connections:
            message_json = json.dumps(message)
            for connection in self.active_connections[client_id]:
                await connection.send_text(message_json)

    async def broadcast(self, message: dict[str, Any]):
        """Broadcast message to all connected clients."""
        message_json = json.dumps(message)
        for connections in self.active_connections.values():
            for connection in connections:
                await connection.send_text(message_json)


# Global connection manager
manager = ConnectionManager()


async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time updates."""
    await manager.connect(websocket, client_id)

    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connected",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat(),
        })

        while True:
            # Receive messages from client
            data = await websocket.receive_json()

            message_type = data.get("type")

            if message_type == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat(),
                })

            elif message_type == "subscribe":
                # Subscribe to specific updates
                channels = data.get("channels", [])
                await websocket.send_json({
                    "type": "subscribed",
                    "channels": channels,
                })

            elif message_type == "chat":
                # Handle chat messages
                message = data.get("message", "")
                # Process through agent system and stream response
                await stream_agent_response(websocket, message, client_id)

    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)


async def stream_agent_response(
    websocket: WebSocket,
    message: str,
    client_id: str,
):
    """Stream agent response through WebSocket."""
    # Send processing start
    await websocket.send_json({
        "type": "processing_start",
        "timestamp": datetime.now().isoformat(),
    })

    # Simulate streaming response
    # In production, this would stream actual agent output
    divisions = ["strategic_planning", "market_intelligence", "channel_management"]

    for division in divisions:
        await websocket.send_json({
            "type": "division_processing",
            "division": division,
            "status": "started",
        })

        await asyncio.sleep(0.5)  # Simulated processing time

        await websocket.send_json({
            "type": "division_processing",
            "division": division,
            "status": "completed",
            "result": f"Division {division} processed successfully",
        })

    # Send final response
    await websocket.send_json({
        "type": "processing_complete",
        "response": "Your request has been processed across multiple divisions.",
        "divisions_used": divisions,
        "timestamp": datetime.now().isoformat(),
    })


async def broadcast_alert(alert: dict[str, Any]):
    """Broadcast an alert to all connected clients."""
    await manager.broadcast({
        "type": "alert",
        "alert": alert,
        "timestamp": datetime.now().isoformat(),
    })


async def broadcast_metric_update(metric_type: str, data: dict[str, Any]):
    """Broadcast a metric update to all connected clients."""
    await manager.broadcast({
        "type": "metric_update",
        "metric_type": metric_type,
        "data": data,
        "timestamp": datetime.now().isoformat(),
    })
