import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.fixture
def mock_firebase(mocker):
    """Centralized fixture for mocking Firebase services."""
    mock_auth = mocker.patch("firebase_admin.auth.verify_id_token")
    mock_firestore = mocker.patch("firebase_admin.firestore.client")
    
    decoded_token = {"uid": "test_user_uid"}
    mock_auth.return_value = decoded_token
    
    return mock_auth, mock_firestore

def test_create_workflow(mock_firebase):
    """Tests the creation of a new workflow."""
    _, mock_firestore = mock_firebase

    mock_workflows_collection = mocker.MagicMock()
    mock_workflow_ref = mocker.MagicMock()
    mock_workflow_ref.id = "new_workflow_id"
    mock_workflows_collection.add.return_value = (None, mock_workflow_ref)
    mock_firestore.return_value.collection.return_value.document.return_value.collection.return_value = mock_workflows_collection

    headers = {"Authorization": "Bearer mock_token"}
    workflow_data = {
        "name": "Test Workflow",
        "steps": [{"type": "llm", "prompt": "Hello"}]
    }
    response = client.post("/organizations/test_org_id/workflows", json=workflow_data, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Workflow created successfully", "workflow_id": "new_workflow_id"}

def test_get_workflow(mock_firebase):
    """Tests retrieving a single workflow."""
    _, mock_firestore = mock_firebase

    mock_doc_snapshot = mocker.MagicMock()
    mock_doc_snapshot.exists = True
    mock_doc_snapshot.to_dict.return_value = {"name": "Test Workflow"}
    mock_doc_snapshot.id = "test_workflow_id"
    mock_firestore.return_value.collection.return_value.document.return_value.get.return_value = mock_doc_snapshot

    headers = {"Authorization": "Bearer mock_token"}
    response = client.get("/organizations/test_org_id/workflows/test_workflow_id", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"id": "test_workflow_id", "name": "Test Workflow"}

# Placeholder for the run workflow test
