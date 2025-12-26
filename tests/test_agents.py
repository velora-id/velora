import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_create_agent(mocker):
    """Tests the creation of a new AI agent."""
    mock_verify_token = mocker.patch("firebase_admin.auth.verify_id_token")
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")

    decoded_token = {"uid": "test_user_uid"}
    mock_verify_token.return_value = decoded_token

    mock_agents_collection = mocker.MagicMock()
    mock_agent_ref = mocker.MagicMock()
    mock_agent_ref.id = "new_agent_id"
    mock_agents_collection.add.return_value = (None, mock_agent_ref)
    mock_firestore_client.return_value.collection.return_value.document.return_value.collection.return_value = mock_agents_collection

    headers = {"Authorization": "Bearer mock_token"}
    agent_data = {
        "name": "Test Agent",
        "type": "chatbot",
        "system_prompt": "You are a helpful assistant.",
        "model": "gpt-3.5-turbo",
        "config": {},
        "status": "active",
    }
    response = client.post("/organizations/test_org_id/agents", json=agent_data, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"message": "Agent created successfully", "agent_id": "new_agent_id"}

def test_get_agent(mocker):
    """Tests retrieving a single AI agent."""
    mock_verify_token = mocker.patch("firebase_admin.auth.verify_id_token")
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")

    decoded_token = {"uid": "test_user_uid"}
    mock_verify_token.return_value = decoded_token

    mock_doc_snapshot = mocker.MagicMock()
    mock_doc_snapshot.exists = True
    mock_doc_snapshot.to_dict.return_value = {"name": "Test Agent"}
    mock_doc_snapshot.id = "test_agent_id"
    mock_firestore_client.return_value.collection.return_value.document.return_value.get.return_value = mock_doc_snapshot

    headers = {"Authorization": "Bearer mock_token"}
    response = client.get("/organizations/test_org_id/agents/test_agent_id", headers=headers)

    assert response.status_code == 200
    assert response.json() == {"id": "test_agent_id", "name": "Test Agent"}

# Additional tests for update and delete can be added here
