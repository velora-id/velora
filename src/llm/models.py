from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LLMUsage(BaseModel):
    id: str
    organization_id: str
    agent_id: str
    workflow_id: str
    task_id: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
