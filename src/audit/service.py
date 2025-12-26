from datetime import datetime

def log_activity(db, organization_id: str, user_id: str, action: str, details: dict):
    """Logs a user activity to the audit trail."""
    log_entry = {
        "timestamp": datetime.utcnow(),
        "user_id": user_id,
        "action": action,
        "details": details,
    }
    db.collection(f"organizations/{organization_id}/audit_logs").add(log_entry)
