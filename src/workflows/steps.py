from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union

class LLMStep(BaseModel):
    type: str = "llm"
    agent_id: str
    prompt: str

class APIStep(BaseModel):
    type: str = "api"
    url: str
    method: str
    headers: Optional[Dict[str, str]] = None
    body: Optional[Dict[str, Any]] = None

class ConditionStep(BaseModel):
    type: str = "condition"
    variable: str
    operator: str
    value: Any

class DelayStep(BaseModel):
    type: str = "delay"
    seconds: int

class WorkflowStep(BaseModel):
    id: str
    type: str
    config: Union[LLMStep, APIStep, ConditionStep, DelayStep]
