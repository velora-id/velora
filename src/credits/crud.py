from datetime import datetime
from src.core.firebase import get_db
from .models import CreditBalance

LOW_BALANCE_THRESHOLD = 10

def get_credit_balance(organization_id: str, db) -> CreditBalance:
    """Get the credit balance for an organization."""
    credit_ref = db.collection(f'organizations/{organization_id}/credits').document('balance')
    credit_doc = credit_ref.get()
    if not credit_doc.exists:
        return CreditBalance(organization_id=organization_id, balance=0, last_updated=datetime.utcnow())
    return CreditBalance(**credit_doc.to_dict())

def deduct_credits(organization_id: str, amount: int, db) -> None:
    """Deduct credits from an organization's balance."""
    balance_ref = db.collection(f'organizations/{organization_id}/credits').document('balance')
    balance_doc = balance_ref.get()
    if not balance_doc.exists:
        raise ValueError("Credit balance not found for organization")

    current_balance = balance_doc.to_dict().get('balance', 0)
    new_balance = current_balance - amount
    if new_balance < 0:
        raise ValueError("Insufficient credits")

    balance_ref.update({"balance": new_balance, "last_updated": datetime.utcnow()})

    # Check for low balance and send an alert
    if new_balance < LOW_BALANCE_THRESHOLD:
        send_low_balance_alert(organization_id, new_balance)


def send_low_balance_alert(organization_id: str, balance: int) -> None:
    """Send a low balance alert if the balance is below a threshold."""
    # In a real-world scenario, this would be an async task that sends an email
    # or a notification to the organization's administrator.
    print(f"Warning: Low credit balance for organization {organization_id}. Current balance: {balance}")
