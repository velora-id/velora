from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from .steps import WorkflowStep

class Workflow(BaseModel):
    name: str
    description: str
    status: str
    steps: List[WorkflowStep]
    estimated_time_saved: int = 5

class WorkflowCreate(Workflow):
    pass

class WorkflowInDB(Workflow):
    id: str
    organization_id: str
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class WorkflowVersion(Workflow):
    version: int
    updated_at: datetime
