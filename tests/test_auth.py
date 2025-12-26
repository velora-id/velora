import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_register_user(mocker):
    """Tests user registration with a mocked Firebase backend."""
    # Mock the Firebase Admin SDK
    mock_create_user = mocker.patch("firebase_admin.auth.create_user")
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")

    # Define the mock user object returned by Firebase
    mock_user = mocker.Mock()
    mock_user.uid = "test_uid"
    mock_user.email = "test@example.com"
    mock_create_user.return_value = mock_user

    # Mock the Firestore document reference and set method
    mock_doc_ref = mocker.Mock()
    mock_firestore_client.return_value.collection.return_value.document.return_value = mock_doc_ref

    # Make the request to the registration endpoint
    response = client.post("/auth/register", json={"email": "test@example.com", "password": "password"})

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully", "uid": "test_uid"}
    mock_create_user.assert_called_once_with(email="test@example.com", password="password")
    mock_firestore_client.return_value.collection.assert_called_once_with("users")
    mock_doc_ref.set.assert_called_once_with({"email": "test@example.com", "role": "user"})

def test_get_me(mocker):
    """Tests the /auth/me endpoint with a mocked Firebase backend."""
    # Mock the Firebase Admin SDK
    mock_verify_token = mocker.patch("firebase_admin.auth.verify_id_token")
    mock_firestore_client = mocker.patch("firebase_admin.firestore.client")

    # Define the mock decoded token and user data
    decoded_token = {"uid": "test_uid"}
    mock_verify_token.return_value = decoded_token

    mock_doc_ref = mocker.Mock()
    mock_doc_snapshot = mocker.Mock()
    mock_doc_snapshot.exists = True
    mock_doc_snapshot.to_dict.return_value = {"email": "test@example.com", "role": "admin"}
    mock_doc_ref.get.return_value = mock_doc_snapshot
    mock_firestore_client.return_value.collection.return_value.document.return_value = mock_doc_ref

    # Make the request to the /auth/me endpoint
    headers = {"Authorization": "Bearer mock_token"}
    response = client.get("/auth/me", headers=headers)

    # Assertions
    assert response.status_code == 200
    assert response.json() == {"uid": "test_uid", "email": "test@example.com", "role": "admin"}
    mock_verify_token.assert_called_once_with("mock_token")
    mock_firestore_client.return_value.collection.assert_called_once_with("users")
