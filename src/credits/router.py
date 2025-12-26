from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .models import CreditBalance, TopUp
from src.core.firebase import get_db
from src.core.roles import require_org_role, OrgRole
from datetime import datetime

router = APIRouter(
    prefix="/credits",
    tags=["credits"],
    dependencies=[Depends(require_org_role(OrgRole.OWNER))]
)

@router.get("/{organization_id}", response_model=CreditBalance)
def get_credit_balance(organization_id: str, db = Depends(get_db)):
    """Get the credit balance for an organization."""
    credit_ref = db.collection(f'organizations/{organization_id}/credits').document('balance')
    credit_doc = credit_ref.get()
    if not credit_doc.exists:
        return CreditBalance(organization_id=organization_id, balance=0, last_updated=datetime.utcnow())
    return CreditBalance(**credit_doc.to_dict())

@router.post("/{organization_id}/top-up", response_model=TopUp)
def top_up_credits(organization_id: str, amount: int, db = Depends(get_db)):
    """Top-up the credit balance for an organization."""
    # In a real application, this would involve a payment gateway.
    # For now, we'll just add a record and update the balance.
    now = datetime.utcnow()
    top_up_ref = db.collection(f'organizations/{organization_id}/top_ups').document()
    top_up_data = {
        "id": top_up_ref.id,
        "organization_id": organization_id,
        "amount": amount,
        "created_at": now
    }
    top_up_ref.set(top_up_data)

    balance_ref = db.collection(f'organizations/{organization_id}/credits').document('balance')
    balance_doc = balance_ref.get()
    if not balance_doc.exists:
        balance_ref.set({"balance": amount, "last_updated": now, "organization_id": organization_id})
    else:
        balance_ref.update({"balance": balance_doc.to_dict()['balance'] + amount, "last_updated": now})
    
    return TopUp(**top_up_data)
