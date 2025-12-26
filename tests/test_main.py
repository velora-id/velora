from fastapi.testclient import TestClient
from src.main import app  # Import your FastAPI app

client = TestClient(app)

def test_health_check():
    """Tests if the /health endpoint returns a 200 OK status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
