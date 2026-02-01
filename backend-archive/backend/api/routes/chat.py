"""Chat endpoints for AI agent interactions."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message model."""

    role: str = Field(..., description="Message role (user, assistant, system)")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


class ChatRequest(BaseModel):
    """Chat request model."""

    message: str = Field(..., description="User message")
    user_id: str = Field(default="default_user")
    brand_id: str = Field(default="default_brand")
    active_channels: list[str] = Field(
        default=["oliveyoung", "coupang", "naver", "kakao"]
    )
    conversation_id: str | None = Field(default=None)


class ChatResponse(BaseModel):
    """Chat response model."""

    message: str
    conversation_id: str
    divisions_used: list[str]
    processing_time_ms: float
    token_usage: dict[str, int] | None = None


class StreamChunk(BaseModel):
    """Streaming response chunk."""

    type: str  # "text", "division_start", "division_end", "complete"
    content: str
    division: str | None = None


@router.post("/", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a message to the AI agent system.

    The Chief Coordinator will analyze the message and route it
    to appropriate divisions for processing.
    """
    import time

    start_time = time.time()

    try:
        # Import here to avoid circular imports
        from backend.graph.main_graph import process_request

        # Process the request through the agent system
        result = await process_request(
            query=request.message,
            user_id=request.user_id,
            brand_id=request.brand_id,
            active_channels=request.active_channels,
        )

        # Extract response
        messages = result.get("messages", [])
        response_content = ""
        if messages:
            last_message = messages[-1]
            response_content = (
                last_message.content
                if hasattr(last_message, "content")
                else str(last_message)
            )

        processing_time = (time.time() - start_time) * 1000

        return ChatResponse(
            message=response_content or "Request processed successfully.",
            conversation_id=request.conversation_id or f"conv_{int(time.time())}",
            divisions_used=result.get("completed_divisions", []),
            processing_time_ms=processing_time,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def stream_message(request: ChatRequest):
    """
    Stream a message response from the AI agent system.

    Returns Server-Sent Events for real-time updates.
    """
    from fastapi.responses import StreamingResponse

    async def generate():
        # Simulated streaming response
        yield f"data: {StreamChunk(type='division_start', content='Processing...', division='chief_coordinator').model_dump_json()}\n\n"

        # In production, this would stream actual agent responses
        import asyncio

        await asyncio.sleep(0.5)
        yield f"data: {StreamChunk(type='text', content='Analyzing your request...').model_dump_json()}\n\n"

        await asyncio.sleep(0.5)
        yield f"data: {StreamChunk(type='division_end', content='Complete', division='chief_coordinator').model_dump_json()}\n\n"

        yield f"data: {StreamChunk(type='complete', content='Done').model_dump_json()}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )


@router.get("/history/{conversation_id}")
async def get_conversation_history(conversation_id: str):
    """Get conversation history by ID."""
    # Would fetch from database
    return {
        "conversation_id": conversation_id,
        "messages": [],
        "created_at": datetime.now().isoformat(),
    }


@router.delete("/history/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear a conversation's history."""
    # Would delete from database
    return {"deleted": True, "conversation_id": conversation_id}
