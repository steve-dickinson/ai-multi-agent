from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from uuid import uuid4

def generate_uuid() -> str:
    return str(uuid4())

class AgentFeedback(BaseModel):
    """Feedback from a single agent."""
    agent_name: str
    summary: str
    issues: List[Dict[str, Any]] = []
    score: Optional[int] = None
    rewritten_content: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class HumanAction(BaseModel):
    """Record of a human decision."""
    decision: str = Field(..., description="accept or reject")
    comment: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    suggestion_id: Optional[str] = None

class ReviewSession(BaseModel):
    """A complete content review session."""
    id: str = Field(default_factory=generate_uuid)
    content: str
    content_title: Optional[str] = None
    status: str = Field(default="pending", description="pending, reviewing, completed")
    agent_results: Dict[str, AgentFeedback] = Field(default_factory=dict)
    human_actions: List[HumanAction] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ContentEmbedding(BaseModel):
    """Vector embedding for content."""
    id: str = Field(default_factory=generate_uuid)
    content: str
    embedding: List[float]
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
