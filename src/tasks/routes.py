from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from src.core.security import get_current_user
from src.core.firebase import get_db
from src.core.roles import OrgRole, require_org_role
from src.tasks.models import TaskInDB
from src.tasks.execution import execute_task
from datetime import datetime

router = APIRouter()

@router.post("/{org_id}/workflows/{workflow_id}/run", response_model=TaskInDB, dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN, OrgRole.EDITOR]))])
def run_workflow(
    org_id: str,
    workflow_id: str,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Run a workflow and create a task."""
    workflow_ref = db.collection('organizations').document(org_id).collection('workflows').document(workflow_id)
    workflow = workflow_ref.get()
    if not workflow.exists:
        raise HTTPException(status_code=404, detail="Workflow not found")

    task_ref = db.collection('organizations').document(org_id).collection('tasks').document()
    task_id = task_ref.id

    now = datetime.utcnow()
    task_data = {
        'id': task_id,
        'workflow_id': workflow_id,
        'organization_id': org_id,
        'status': 'queued',
        'logs': [],
        'created_at': now,
        'updated_at': now
    }

    task_ref.set(task_data)
    
    task = TaskInDB(**task_data)

    # In a real-world application, you would use a proper background task queue
    # like Celery or ARQ. For this example, we use FastAPI's BackgroundTasks.
    background_tasks.add_task(execute_task, task)

    return task

@router.get("/{org_id}/tasks/{task_id}", response_model=TaskInDB, dependencies=[Depends(require_org_role([OrgRole.OWNER, OrgRole.ADMIN, OrgRole.EDITOR, OrgRole.VIEWER]))])
def get_task(
    org_id: str,
    task_id: str,
    db = Depends(get_db)
):
    """Get a specific task from an organization."""
    task_ref = db.collection('organizations').document(org_id).collection('tasks').document(task_id)
    task = task_ref.get()
    if not task.exists:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskInDB(**task.to_dict())
