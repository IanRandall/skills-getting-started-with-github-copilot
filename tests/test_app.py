from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(app_module, "activities", deepcopy(app_module.activities))
    return TestClient(app_module.app)


def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert "Chess Club" in response.json()
    assert "michael@mergington.edu" in response.json()["Chess Club"]["participants"]


def test_signup_adds_student_to_activity(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "new-student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up new-student@mergington.edu for Chess Club"
    }
    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert "new-student@mergington.edu" in participants


def test_signup_duplicate_student_returns_400(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student is already signed up for this activity"
    }


def test_signup_for_unknown_activity_returns_404(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "new-student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_delete_participant_removes_email_from_activity(client):
    response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")

    assert response.status_code == 200
    assert "michael@mergington.edu" not in response.json()["participants"]


def test_delete_participant_by_query_param_removes_email_from_activity(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in response.json()["participants"]


def test_delete_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "does-not-exist@mergington.edu"},
    )

    assert response.status_code == 404


def test_delete_participant_from_unknown_activity_returns_404(client):
    response = client.delete(
        "/activities/Unknown Club/participants",
        params={"email": "new-student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
