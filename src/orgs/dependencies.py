from fastapi import Depends, HTTPException, Path
from src.core.firebase import get_db
from src.core.security import get_current_user

def org_access_dependency(
    organization_id: str = Path(...),
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """
    Dependency to check if a user has access to a given organization.
    Raises a 403 Forbidden error if the user is not a member of the organization.
    """
    member_ref = db.collection('organizations').document(organization_id).collection('members').document(current_user['uid'])
    member_doc = member_ref.get()

    if not member_doc.exists:
        raise HTTPException(
            status_code=403,
            detail="User does not have access to this organization."
        )
