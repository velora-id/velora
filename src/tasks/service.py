from .models import Task

async def create_task(db, organization_id: str, task_data: dict) -> Task:
    """Creates a new task in Firestore."""
    ref = db.collection('organizations').document(organization_id).collection('tasks').add(task_data)
    task_data['id'] = ref[1].id
    return Task(**task_data)
