from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Quota(BaseModel):
    requests: int

class Plan(BaseModel):
    id: str
    name: str
    price: float
    features: List[str]
    quotas: Quota

class Subscription(BaseModel):
    id: str
    plan_id: str
    organization_id: str
    status: str # e.g., active, canceled, past_due
    created_at: datetime
    current_period_start: datetime
    current_period_end: datetime
