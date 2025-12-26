from pydantic import BaseModel
from datetime import datetime

class CreditBalance(BaseModel):
    organization_id: str
    balance: int
    last_updated: datetime

class TopUp(BaseModel):
    id: str
    organization_id: str
    amount: int
    created_at: datetime
