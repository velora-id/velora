from enum import Enum
from functools import wraps
from typing import List, Optional
from fastapi import Depends, HTTPException, Request

from src.core.security import get_current_user
from src.core.firebase import get_db

# Global Roles
class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"

# Organization Roles
class OrgRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"

def get_user_roles(uid: str) -> List[Role]:
    """Fetches user's global roles from Firestore."""
    db = get_db()
    user_doc = db.collection(u'users').document(uid).get()
    
    if user_doc.exists:
        user_data = user_doc.to_dict()
        if user_data and 'roles' in user_data:
            return [Role(role) for role in user_data['roles'] if role in Role.__members__.values()]
    return [Role.USER] # Default role

def require_role(required_role: Role):
    """Dependency to check for a global user role."""
    def role_checker(current_user: dict = Depends(get_current_user)):
        user_roles = get_user_roles(current_user['uid'])
        if required_role not in user_roles:
            raise HTTPException(
                status_code=403, detail="You do not have permission to access this resource."
            )
        return current_user
    return role_checker

def get_user_org_role(uid: str, org_id: str) -> Optional[OrgRole]:
    """Fetches a user's role within a specific organization."""
    db = get_db()
    member_ref = db.collection('organizations').document(org_id).collection('members').document(uid)
    member_doc = member_ref.get()
    if member_doc.exists:
        member_data = member_doc.to_dict()
        return OrgRole(member_data.get('role'))
    return None

def require_org_role(required_roles: List[OrgRole]):
    """
    Dependency to check if a user has one of the required roles in an organization.
    It retrieves the org_id from the path parameters.
    """
    def role_checker(
        request: Request,
        current_user: dict = Depends(get_current_user)
    ):
        org_id = request.path_params.get("org_id")
        if not org_id:
            raise HTTPException(
                status_code=500, detail="Could not determine organization ID from request."
            )

        user_org_role = get_user_org_role(current_user['uid'], org_id)

        if user_org_role is None:
            raise HTTPException(
                status_code=403, detail="You are not a member of this organization."
            )

        if user_org_role not in required_roles:
            raise HTTPException(
                status_code=403, detail="Your role does not grant you permission for this action."
            )
        
        return current_user
    return role_checker
