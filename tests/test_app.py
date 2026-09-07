from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def reset_activity(activity_name: str, participants=None):
    app_module.activities[activity_name]["participants"] = participants or []


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "student@example.edu"
    reset_activity(activity_name, [email])

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant():
    activity_name = "Chess Club"
    email = "student@example.edu"
    reset_activity(activity_name, [email])

    response = client.delete(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email not in app_module.activities[activity_name]["participants"]
