import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_organization(mocker):
    """Tests organization creation with a mocked Firebase backend."""
    # Mock authentication and Firestore
    mock_verify_token = mocker.patch("firebase_admin.auth.verify_id_token")
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")

    # Simulate an authenticated user
    decoded_token = {"uid": "test_owner_uid"}
    mock_verify_token.return_value = decoded_token

    # Mock Firestore interactions
    mock_org_collection = mocker.MagicMock()
    mock_firestore_client.return_value.collection.return_value = mock_org_collection
    mock_org_ref = mocker.MagicMock()
    mock_org_ref.id = "new_org_id"
    mock_org_collection.add.return_value = (None, mock_org_ref) # Firestore `add` returns a tuple

    # Make the request to create an organization
    headers = {"Authorization": "Bearer mock_token"}
    response = client.post("/organizations", json={"name": "Test Org"}, headers=headers)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "Organization created successfully", "organization_id": "new_org_id"}

    # Verify Firestore calls
    mock_firestore_client.return_value.collection.assert_any_call("organizations")

def test_list_user_organizations(mocker):
    """Tests listing organizations for the current user."""
    mock_verify_token = mocker.patch("firebase_admin.auth.verify_id_token")
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")

    decoded_token = {"uid": "test_user_uid"}
    mock_verify_token.return_value = decoded_token

    # Mock Firestore query results
    mock_stream = mocker.MagicMock()
    mock_doc1 = mocker.MagicMock()
    mock_doc1.to_dict.return_value = {"name": "Org 1"}
    mock_doc1.id = "org1"
    mock_doc2 = mocker.MagicMock()
    mock_doc2.to_dict.return_value = {"name": "Org 2"}
    mock_doc2.id = "org2"
    mock_stream.stream.return_value = [mock_doc1, mock_doc2]
    mock_firestore_client.return_value.collection.return_value.where.return_value = mock_stream

    headers = {"Authorization": "Bearer mock_token"}
    response = client.get("/organizations", headers=headers)

    assert response.status_code == 200
    assert response.json() == [{"id": "org1", "name": "Org 1"}, {"id": "org2", "name": "Org 2"}]

def test_invite_member(mocker):
    """Tests inviting a new member to an organization."""
    mock_verify_token = mocker.patch("firebase_admin.auth.verify_id_token")
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")
    mock_auth = mocker.patch("firebase_admin.auth")

    # Simulate an admin user
    decoded_token = {"uid": "test_admin_uid"}
    mock_verify_token.return_value = decoded_token

    # Simulate getting the invited user by email
    mock_user = mocker.MagicMock()
    mock_user.uid = "new_member_uid"
    mock_auth.get_user_by_email.return_value = mock_user

    # Mock Firestore
    mock_members_collection = mocker.MagicMock()
    mock_firestore_client.return_value.collection.return_value.document.return_value.collection.return_value = mock_members_collection

    headers = {"Authorization": "Bearer mock_token"}
    response = client.post(
        "/organizations/test_org_id/members",
        json={"email": "new_member@example.com", "role": "editor"},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Member invited successfully"}
    mock_members_collection.document.assert_called_with("new_member_uid")

