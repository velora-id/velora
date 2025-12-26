from fastapi import APIRouter, Depends, HTTPException
from .models import OrganizationCreate, OrganizationInDB, MemberInvite
from src.core.security import get_current_user
from src.core.firebase import get_db, get_auth
from src.core.roles import OrgRole, require_org_role
from typing import List

router = APIRouter()

@router.post("/", response_model=OrganizationInDB)
def create_organization(
    org_create: OrganizationCreate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Create a new organization."""
    # Create a new document in the 'organizations' collection
    org_ref = db.collection('organizations').document()
    org_id = org_ref.id

    # Set the organization data
    org_data = org_create.dict()
    org_data['owner_id'] = current_user['uid']
    org_data['id'] = org_id
    org_ref.set(org_data)

    # Add the owner as a member with the 'owner' role
    org_ref.collection('members').document(current_user['uid']).set({
        'role': 'owner'
    })

    return OrganizationInDB(**org_data)

@router.get("/", response_model=List[OrganizationInDB])
def list_organizations(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """List all organizations for the current user."""
    user_id = current_user['uid']
    orgs = []

    # Query for organizations where the user is a member
    memberships = db.collection_group('members').where('user_id', '==', user_id).stream()
    for member in memberships:
        org_ref = member.reference.parent.parent
        org_doc = org_ref.get()
        if org_doc.exists:
            orgs.append(OrganizationInDB(**org_doc.to_dict()))

    return orgs

@router.post("/{org_id}/members/invite", dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN]))])
def invite_member(
    org_id: str,
    invite: MemberInvite,
    db = Depends(get_db)
):
    """Invite a user to an organization by email."""
    try:
        user = get_auth().get_user_by_email(invite.email)
    except Exception:
        raise HTTPException(
            status_code=404, detail=f"User with email {invite.email} not found."
        )

    # Add user to the members subcollection
    db.collection('organizations').document(org_id).collection('members').document(user.uid).set({
        'role': invite.role.value
    })

    return {"message": f"User {invite.email} invited to organization {org_id} with role {invite.role.value}"}
