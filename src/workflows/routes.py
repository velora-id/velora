from fastapi import APIRouter, Depends, HTTPException, Request
from .models import WorkflowCreate, WorkflowInDB, Workflow, WorkflowVersion
from src.core.security import get_current_user
from src.core.firebase import get_db
from src.core.roles import OrgRole, require_org_role
from typing import List, Dict, Any
from datetime import datetime
from .execute import execute_workflow

router = APIRouter()

@router.post("/{org_id}/workflows", response_model=WorkflowInDB, dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN]))])
def create_workflow(
    org_id: str,
    workflow_create: WorkflowCreate,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Create a new workflow in an organization."""
    workflow_ref = db.collection('organizations').document(org_id).collection('workflows').document()
    workflow_id = workflow_ref.id

    now = datetime.utcnow()
    workflow_data = workflow_create.dict()
    workflow_data['id'] = workflow_id
    workflow_data['organization_id'] = org_id
    workflow_data['version'] = 1
    workflow_data['created_at'] = now
    workflow_data['updated_at'] = now
    
    workflow_ref.set(workflow_data)

    return WorkflowInDB(**workflow_data)

@router.get("/{org_id}/workflows", response_model=List[WorkflowInDB], dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN, OrgRole.EDITOR, OrgRole.VIEWER]))])
def list_workflows(
    org_id: str,
    db = Depends(get_db)
):
    """List all workflows in an organization."""
    workflows_ref = db.collection('organizations').document(org_id).collection('workflows')
    workflows = [WorkflowInDB(**doc.to_dict()) for doc in workflows_ref.stream()]
    return workflows

@router.get("/{org_id}/workflows/{workflow_id}", response_model=WorkflowInDB, dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN, OrgRole.EDITOR, OrgRole.VIEWER]))])
def get_workflow(
    org_id: str,
    workflow_id: str,
    db = Depends(get_db)
):
    """Get a specific workflow from an organization."""
    workflow_ref = db.collection('organizations').document(org_id).collection('workflows').document(workflow_id)
    workflow = workflow_ref.get()
    if not workflow.exists:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return WorkflowInDB(**workflow.to_dict())

@router.put("/{org_id}/workflows/{workflow_id}", response_model=WorkflowInDB, dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN]))])
def update_workflow(
    org_id: str,
    workflow_id: str,
    workflow_update: Workflow,
    db = Depends(get_db)
):
    """Update a workflow in an organization."""
    workflow_ref = db.collection('organizations').document(org_id).collection('workflows').document(workflow_id)
    current_workflow_doc = workflow_ref.get()
    if not current_workflow_doc.exists:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    current_workflow_data = current_workflow_doc.to_dict()
    current_version = current_workflow_data.get('version', 1)

    # Create a version history document
    version_ref = workflow_ref.collection('versions').document(str(current_version))
    version_data = WorkflowVersion(**current_workflow_data)
    version_ref.set(version_data.dict())

    # Update the main workflow document
    now = datetime.utcnow()
    updated_data = workflow_update.dict()
    updated_data['version'] = current_version + 1
    updated_data['updated_at'] = now

    workflow_ref.update(updated_data)

    # Return the updated workflow
    final_workflow_data = workflow_ref.get().to_dict()
    return WorkflowInDB(**final_workflow_data)

@router.delete("/{org_id}/workflows/{workflow_id}", status_code=204, dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN]))])
def delete_workflow(
    org_id: str,
    workflow_id: str,
    db = Depends(get_db)
):
    """Delete a workflow from an organization."""
    workflow_ref = db.collection('organizations').document(org_id).collection('workflows').document(workflow_id)
    if not workflow_ref.get().exists:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow_ref.delete()
    return

@router.post("/{org_id}/workflows/{workflow_id}/run", dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN, OrgRole.EDITOR]))])
async def run_workflow(
    org_id: str,
    workflow_id: str,
    request: Request,
    db = Depends(get_db)
):
    """Run a workflow and create a task."""
    payload = await request.json()
    execute_workflow(db, org_id, workflow_id, payload)
    return {"message": "Workflow execution started."}
