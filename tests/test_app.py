import uuid

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_successful_for_valid_activity():
    # Arrange
    email = f"signup-{uuid.uuid4().hex}@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_duplicate_signup_is_rejected():
    # Arrange
    email = f"duplicate-{uuid.uuid4().hex}@mergington.edu"
    activity_name = "Chess Club"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_participant_can_be_unregistered():
    # Arrange
    email = f"remove-{uuid.uuid4().hex}@mergington.edu"
    activity_name = "Programming Class"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]


def test_missing_activity_returns_not_found():
    # Arrange
    email = f"missing-activity-{uuid.uuid4().hex}@mergington.edu"
    activity_name = "Unknown Activity"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
