from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_delete_participant_removes_email_from_activity():
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in response.json()["participants"]

    # Restore state for the rest of the suite.
    client.post("/activities/Chess Club/signup?email=michael@mergington.edu")


def test_delete_participant_by_query_param_removes_email_from_activity():
    response = client.delete("/activities/Chess Club/participants?email=michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in response.json()["participants"]

    client.post("/activities/Chess Club/signup?email=michael@mergington.edu")


def test_delete_missing_participant_returns_404():
    response = client.delete("/activities/Chess Club/participants?email=does-not-exist@mergington.edu")

    assert response.status_code == 404
