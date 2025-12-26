from fastapi import APIRouter, Depends, HTTPException
from .models import AgentCreate, AgentInDB, Agent, AgentVersion
from src.core.security import get_current_user
from src.core.firebase import get_db
from src.core.roles import OrgRole, require_org_role
from typing import List
from datetime import datetime

router = APIRouter()

@router.post("/{org_id}/agents", response_model=AgentInDB, dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN]))])
def create_agent(
    org_id: str,
    agent_create: AgentCreate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Create a new agent in an organization."""
    agent_ref = db.collection('organizations').document(org_id).collection('agents').document()
    agent_id = agent_ref.id

    now = datetime.utcnow()
    agent_data = agent_create.dict()
    agent_data['id'] = agent_id
    agent_data['organization_id'] = org_id
    agent_data['version'] = 1
    agent_data['created_at'] = now
    agent_data['updated_at'] = now
    
    agent_ref.set(agent_data)

    return AgentInDB(**agent_data)

@router.get("/{org_id}/agents", response_model=List[AgentInDB], dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN, OrgRole.EDITOR, OrgRole.VIEWER]))])
def list_agents(
    org_id: str,
    db = Depends(get_db)
):
    """List all agents in an organization."""
    agents_ref = db.collection('organizations').document(org_id).collection('agents')
    agents = [AgentInDB(**doc.to_dict()) for doc in agents_ref.stream()]
    return agents

@router.get("/{org_id}/agents/{agent_id}", response_model=AgentInDB, dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN, OrgRole.EDITOR, OrgRole.VIEWER]))])
def get_agent(
    org_id: str,
    agent_id: str,
    db = Depends(get_db)
):
    """Get a specific agent from an organization."""
    agent_ref = db.collection('organizations').document(org_id).collection('agents').document(agent_id)
    agent = agent_ref.get()
    if not agent.exists:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentInDB(**agent.to_dict())

@router.put("/{org_id}/agents/{agent_id}", response_model=AgentInDB, dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN]))])
def update_agent(
    org_id: str,
    agent_id: str,
    agent_update: Agent,
    db = Depends(get_db)
):
    """Update an agent in an organization."""
    agent_ref = db.collection('organizations').document(org_id).collection('agents').document(agent_id)
    current_agent_doc = agent_ref.get()
    if not current_agent_doc.exists:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    current_agent_data = current_agent_doc.to_dict()
    current_version = current_agent_data.get('version', 1)

    # Create a version history document
    version_ref = agent_ref.collection('versions').document(str(current_version))
    version_data = AgentVersion(**current_agent_data)
    version_ref.set(version_data.dict())

    # Update the main agent document
    now = datetime.utcnow()
    updated_data = agent_update.dict()
    updated_data['version'] = current_version + 1
    updated_data['updated_at'] = now

    agent_ref.update(updated_data)

    # Return the updated agent
    final_agent_data = agent_ref.get().to_dict()
    return AgentInDB(**final_agent_data)

@router.delete("/{org_id}/agents/{agent_id}", status_code=204, dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN]))])
def delete_agent(
    org_id: str,
    agent_id: str,
    db = Depends(get_db)
):
    """Delete an agent from an organization."""
    agent_ref = db.collection('organizations').document(org_id).collection('agents').document(agent_id)
    if not agent_ref.get().exists:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Note: You might want to also delete the 'versions' subcollection.
    # This is a more complex operation and is not implemented here for simplicity.
    agent_ref.delete()
    return
