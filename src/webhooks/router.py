from fastapi import APIRouter, Depends, HTTPException, Request, Header
from typing import List
import hmac
import hashlib

from src.core.firebase import get_db
from src.tasks.service import create_task
from .models import WebhookTrigger
from .service import (
    create_webhook_trigger,
    get_webhook_trigger_by_id,
    list_webhook_triggers_by_org,
    update_webhook_trigger,
    delete_webhook_trigger,
)

router = APIRouter(
    prefix="/webhooks",
    tags=["webhooks"],
)


async def verify_signature(
    request: Request,
    trigger_id: str,
    x_signature: str = Header(...),
    db=Depends(get_db),
):
    """Verifies the signature of the webhook payload."""
    webhook_trigger = get_webhook_trigger_by_id(db, trigger_id)
    if not webhook_trigger:
        raise HTTPException(status_code=404, detail="Webhook trigger not found")

    body = await request.body()
    expected_signature = hmac.new(
        webhook_trigger.secret.encode(), body, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, x_signature):
        raise HTTPException(status_code=403, detail="Invalid signature")


@router.post("/trigger/{trigger_id}", status_code=202, dependencies=[Depends(verify_signature)])
async def trigger_webhook(trigger_id: str, request: Request, db=Depends(get_db)):
    """Triggers a workflow from a webhook."""
    webhook_trigger = get_webhook_trigger_by_id(db, trigger_id)
    if not webhook_trigger:
        # This should not be reached if verify_signature is working correctly
        raise HTTPException(status_code=404, detail="Webhook trigger not found")

    # TODO: Implement validation logic based on webhook_trigger.validation_rules

    payload = await request.json()

    task_data = {
        "workflow_id": webhook_trigger.workflow_id,
        "status": "queued",
        "payload": payload,
    }

    await create_task(db, webhook_trigger.organization_id, task_data)

    return {"status": "accepted"}


@router.post("/{organization_id}", response_model=WebhookTrigger, status_code=201)
async def http_create_webhook_trigger(
    organization_id: str, webhook_data: WebhookTrigger, db=Depends(get_db)
):
    """Creates a new webhook trigger for an organization."""
    webhook_data.organization_id = organization_id
    return create_webhook_trigger(db, webhook_data)


@router.get("/{organization_id}", response_model=List[WebhookTrigger])
async def http_list_webhook_triggers(organization_id: str, db=Depends(get_db)):
    """Lists all webhook triggers for an organization."""
    return list_webhook_triggers_by_org(db, organization_id)


@router.get("/{organization_id}/{trigger_id}", response_model=WebhookTrigger)
async def http_get_webhook_trigger(organization_id: str, trigger_id: str, db=Depends(get_db)):
    """Gets a specific webhook trigger."""
    # Although we can get it by ID, we check org for authorization purposes
    webhook_trigger = get_webhook_trigger_by_id(db, trigger_id)
    if not webhook_trigger or webhook_trigger.organization_id != organization_id:
        raise HTTPException(status_code=404, detail="Webhook trigger not found")
    return webhook_trigger


@router.put("/{organization_id}/{trigger_id}", response_model=WebhookTrigger)
async def http_update_webhook_trigger(
    organization_id: str, trigger_id: str, webhook_data: dict, db=Depends(get_db)
):
    """Updates a webhook trigger."""
    webhook_trigger = get_webhook_trigger_by_id(db, trigger_id)
    if not webhook_trigger or webhook_trigger.organization_id != organization_id:
        raise HTTPException(status_code=404, detail="Webhook trigger not found")
    return update_webhook_trigger(db, trigger_id, webhook_data)


@router.delete("/{organization_id}/{trigger_id}", status_code=204)
async def http_delete_webhook_trigger(organization_id: str, trigger_id: str, db=Depends(get_db)):
    """Deletes a webhook trigger."""
    webhook_trigger = get_webhook_trigger_by_id(db, trigger_id)
    if not webhook_trigger or webhook_trigger.organization_id != organization_id:
        raise HTTPException(status_code=404, detail="Webhook trigger not found")
    delete_webhook_trigger(db, trigger_id)
    return
