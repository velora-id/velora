from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
from .models import Plan, Subscription
from src.core.firebase import get_db
from src.core.roles import require_org_role, OrgRole
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/billing",
    tags=["billing"],
)

@router.get("/plans", response_model=List[Plan])
def list_plans(db = Depends(get_db)):
    """List all available subscription plans."""
    plans_ref = db.collection('plans').stream()
    plans = []
    for doc in plans_ref:
        plan_data = doc.to_dict()
        plan_data['id'] = doc.id
        plans.append(Plan(**plan_data))
    return plans

@router.post("/{organization_id}/subscribe", response_model=Subscription, dependencies=[Depends(require_org_role([OrgRole.OWNER]))])
def subscribe_to_plan(organization_id: str, plan_id: str, db = Depends(get_db)):
    """Subscribe an organization to a new plan."""
    plan_ref = db.collection('plans').document(plan_id).get()
    if not plan_ref.exists:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan_data = plan_ref.to_dict()
    now = datetime.utcnow()
    subscription_data = {
        "plan_id": plan_id,
        "organization_id": organization_id,
        "status": "active",
        "created_at": now,
        "current_period_start": now,
        "current_period_end": now + timedelta(days=30), # Assuming a 30-day billing cycle
        "quotas": plan_data.get("quotas")
    }
    
    subscription_ref = db.collection(f'organizations/{organization_id}/subscriptions').document()
    subscription_data["id"] = subscription_ref.id
    subscription_ref.set(subscription_data)

    return Subscription(**subscription_data)

@router.post("/{organization_id}/subscriptions/{subscription_id}/cancel", dependencies=[Depends(require_org_role([OrgRole.OWNER]))])
def cancel_subscription(organization_id: str, subscription_id: str, db = Depends(get_db)):
    """Cancel an active subscription for an organization."""
    subscription_ref = db.collection(f'organizations/{organization_id}/subscriptions').document(subscription_id)
    subscription = subscription_ref.get()

    if not subscription.exists:
        raise HTTPException(status_code=404, detail="Subscription not found")

    subscription_ref.update({"status": "canceled"})

    return {"message": "Subscription canceled successfully"}

@router.post("/webhook")
async def handle_stripe_webhook(request: Request):
    """Handle incoming webhooks from payment providers like Stripe."""
    payload = await request.json()
    # For now, just log the payload
    print(f"Received webhook payload: {payload}")
    return {"status": "received"}
