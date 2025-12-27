from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
from uuid import uuid4

def generate_uuid() -> str:
    return str(uuid4())

class AgentFeedback(BaseModel):
    """Feedback from a single agent."""
    agent_name: str
    summary: str
    issues: list[dict[str, Any]] = []
    score: int | None = None
    rewritten_content: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class HumanAction(BaseModel):
    """Record of a human decision."""
    decision: str = Field(..., description="accept or reject")
    comment: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    suggestion_id: str | None = None

class ReviewSession(BaseModel):
    """A complete content review session."""
    id: str = Field(default_factory=generate_uuid)
    content: str
    content_title: str | None = None
    status: str = Field(default="pending", description="pending, reviewing, completed")
    agent_results: dict[str, AgentFeedback] = Field(default_factory=dict)
    human_actions: list[HumanAction] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ContentEmbedding(BaseModel):
    """Vector embedding for content."""
    id: str = Field(default_factory=generate_uuid)
    content: str
    embedding: list[float]
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
