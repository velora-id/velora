from src.core.firebase import get_db
from .models import Integration
from typing import List

def create_integration(db, organization_id: str, integration_data: Integration) -> Integration:
    """Creates a new integration in Firestore."""
    ref = db.collection('organizations').document(organization_id).collection('integrations').add(integration_data.dict())
    integration_data.id = ref[1].id
    return integration_data

def get_integration(db, organization_id: str, integration_id: str) -> Integration:
    """Retrieves an integration from Firestore."""
    ref = db.collection('organizations').document(organization_id).collection('integrations').document(integration_id).get()
    if ref.exists:
        return Integration(**ref.to_dict())
    return None

def list_integrations(db, organization_id: str) -> List[Integration]:
    """Lists all integrations for an organization."""
    refs = db.collection('organizations').document(organization_id).collection('integrations').stream()
    integrations = []
    for ref in refs:
        integrations.append(Integration(**ref.to_dict()))
    return integrations

def update_integration(db, organization_id: str, integration_id: str, integration_data: Integration) -> Integration:
    """Updates an integration in Firestore."""
    db.collection('organizations').document(organization_id).collection('integrations').document(integration_id).set(integration_data.dict())
    return integration_data

def delete_integration(db, organization_id: str, integration_id: str):
    """Deletes an integration from Firestore."""
    db.collection('organizations').document(organization_id).collection('integrations').document(integration_id).delete()
