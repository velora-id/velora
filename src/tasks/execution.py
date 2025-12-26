from .models import TaskInDB
from src.core.firebase import get_db
from datetime import datetime

def execute_task(task: TaskInDB):
    """Executes a task and updates its status and logs."""
    print(f"Executing task {task.id} for workflow {task.workflow_id}")
    db = get_db()
    task_ref = db.collection('organizations').document(task.organization_id).collection('tasks').document(task.id)

    # Simulate task execution
    task_ref.update({
        'status': 'running',
        'updated_at': datetime.utcnow()
    })

    # Simulate a successful execution
    task_ref.update({
        'status': 'success',
        'updated_at': datetime.utcnow()
    })
