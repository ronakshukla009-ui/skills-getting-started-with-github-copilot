from fastapi.testclient import TestClient


def test_unregister_removes_participant(client: TestClient, activity_store):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}",
    }
    assert email not in activity_store[activity_name]["participants"]


def test_unregister_rejects_unknown_activity(client: TestClient):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_rejects_participant_not_registered(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity",
    }


def test_unregister_requires_email(client: TestClient):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister")

    # Assert
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "email"]


def test_participant_can_signup_again_after_unregistering(
    client: TestClient,
    activity_store,
):
    # Arrange
    activity_name = "Programming Class"
    email = "returning.student@mergington.edu"
    initial_signup = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    unregister = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email},
    )

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert initial_signup.status_code == 200
    assert unregister.status_code == 200
    assert response.status_code == 200
    assert email in activity_store[activity_name]["participants"]
