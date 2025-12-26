
from pydantic import BaseModel, Field
from typing import Optional
from src.core.roles import OrgRole

class Organization(BaseModel):
    name: str
    description: Optional[str] = None

class OrganizationCreate(Organization):
    pass

class OrganizationInDB(Organization):
    id: str
    owner_id: str

class MemberInvite(BaseModel):
    email: str
    role: OrgRole
