import secrets
from typing import Optional

from src.core.firebase import get_db

API_KEY_PREFIX = "velora-"


def generate_api_key(db, organization_id: str) -> str:
    """Generates a new API key for an organization and stores it in Firestore."""
    api_key = f"{API_KEY_PREFIX}{secrets.token_urlsafe(32)}"
    db.collection("api_keys").document(api_key).set({"organization_id": organization_id})
    return api_key


def get_organization_by_api_key(db, api_key: str) -> Optional[str]:
    """Retrieves the organization ID associated with a given API key."""
    ref = db.collection("api_keys").document(api_key).get()
    if ref.exists:
        return ref.to_dict().get("organization_id")
    return None


def delete_api_key(db, api_key: str):
    """Deletes an API key from Firestore."""
    db.collection("api_keys").document(api_key).delete()
