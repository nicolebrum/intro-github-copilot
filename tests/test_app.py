from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == activities


def test_signup_for_activity():
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "newstudent@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up newstudent@mergington.edu for Chess Club"
    }
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_400():
    email = "duplicate@mergington.edu"

    first_response = client.post(
        "/activities/Programming Class/signup",
        params={"email": email},
    )
    assert first_response.status_code == 200

    second_response = client.post(
        "/activities/Programming Class/signup",
        params={"email": email},
    )

    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up for this activity"


def test_signup_for_missing_activity_returns_404():
    response = client.post(
        "/activities/Nonexistent Activity/signup",
        params={"email": "test@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant():
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_non_registered_email_returns_404():
    response = client.delete(
        "/activities/Programming Class/participants",
        params={"email": "absent@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not registered for this activity"


def test_unregister_missing_activity_returns_404():
    response = client.delete(
        "/activities/Unknown Activity/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
