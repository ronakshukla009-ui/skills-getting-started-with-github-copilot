from fastapi.testclient import TestClient


def test_root_redirects_to_static_app(client: TestClient):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_seeded_activities(client: TestClient):
    # Arrange
    expected_activity = "Chess Club"
    expected_participants = {
        "michael@mergington.edu",
        "daniel@mergington.edu",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert expected_activity in response_data
    assert set(response_data[expected_activity]["participants"]) == expected_participants


def test_get_activities_returns_required_fields(client: TestClient):
    # Arrange
    required_fields = {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    for activity in response.json().values():
        assert required_fields <= activity.keys()
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)
