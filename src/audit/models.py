from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class AuditLog(BaseModel):
    id: str
    user_id: str
    action: str
    timestamp: datetime
    details: Dict[str, Any]

class AuditLogInDB(AuditLog):
    pass
