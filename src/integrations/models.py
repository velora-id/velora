from pydantic import BaseModel, Field
from typing import Dict, Any

class Integration(BaseModel):
    id: str
    organization_id: str
    name: str
    type: str
    config: Dict[str, Any]
