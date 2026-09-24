import uuid

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    email = f"duplicate-{uuid.uuid4().hex}@mergington.edu"
    activity_name = "Chess Club"

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert second_response.status_code == 400
    assert "already signed up" in second_response.json()["detail"].lower()

    cleanup_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert cleanup_response.status_code == 200


def test_participant_can_be_unregistered():
    email = f"remove-{uuid.uuid4().hex}@mergington.edu"
    activity_name = "Programming Class"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert unregister_response.status_code == 200
    assert f"Removed {email} from {activity_name}" in unregister_response.json()["message"]

    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity_name]["participants"]
