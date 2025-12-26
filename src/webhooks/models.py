from pydantic import BaseModel, Field
from typing import Dict, Any
import secrets

class WebhookTrigger(BaseModel):
    id: str
    organization_id: str
    workflow_id: str
    name: str
    secret: str = Field(default_factory=lambda: secrets.token_hex(32))
    validation_rules: Dict[str, Any] = Field(default_factory=dict)
