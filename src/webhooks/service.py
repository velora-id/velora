import uuid
from typing import List, Optional
from src.core.firebase import get_db
from .models import WebhookTrigger

def create_webhook_trigger(db, webhook_trigger_data: WebhookTrigger) -> WebhookTrigger:
    """Creates a new webhook trigger in the root webhook_triggers collection."""
    trigger_id = str(uuid.uuid4())
    webhook_trigger_data.id = trigger_id
    db.collection('webhook_triggers').document(trigger_id).set(webhook_trigger_data.dict())
    return webhook_trigger_data

def get_webhook_trigger_by_id(db, webhook_trigger_id: str) -> Optional[WebhookTrigger]:
    """Retrieves a webhook trigger from Firestore by its ID."""
    ref = db.collection('webhook_triggers').document(webhook_trigger_id).get()
    if ref.exists:
        return WebhookTrigger(**ref.to_dict())
    return None

def list_webhook_triggers_by_org(db, organization_id: str) -> List[WebhookTrigger]:
    """Lists all webhook triggers for an organization."""
    refs = db.collection('webhook_triggers').where('organization_id', '==', organization_id).stream()
    webhook_triggers = []
    for ref in refs:
        webhook_triggers.append(WebhookTrigger(**ref.to_dict()))
    return webhook_triggers

def update_webhook_trigger(db, webhook_trigger_id: str, webhook_trigger_data: dict) -> WebhookTrigger:
    """Updates a webhook trigger in Firestore."""
    webhook_trigger_data['id'] = webhook_trigger_id
    db.collection('webhook_triggers').document(webhook_trigger_id).set(webhook_trigger_data, merge=True)
    updated_doc = db.collection('webhook_triggers').document(webhook_trigger_id).get()
    return WebhookTrigger(**updated_doc.to_dict())

def delete_webhook_trigger(db, webhook_trigger_id: str):
    """Deletes a webhook trigger from Firestore."""
    db.collection('webhook_triggers').document(webhook_trigger_id).delete()
