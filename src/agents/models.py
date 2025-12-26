from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class Agent(BaseModel):
    name: str
    type: str
    system_prompt: str
    model: str
    config: Dict[str, Any]
    status: str

class AgentCreate(Agent):
    pass

class AgentInDB(Agent):
    id: str
    organization_id: str
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class AgentVersion(Agent):
    version: int
    updated_at: datetime
