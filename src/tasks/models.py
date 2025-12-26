from pydantic import BaseModel
from typing import Dict, Any

class Task(BaseModel):
    id: str
    workflow_id: str
    status: str
    payload: Dict[str, Any]

class TaskInDB(Task):
    pass
