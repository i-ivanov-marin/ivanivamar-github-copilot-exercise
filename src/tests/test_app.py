from src.app import activities


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    body = response.json()
    assert "Chess Club" in body
    assert body["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_success(client):
    response = client.post(
        "/activities/Chess Club/signup", params={"email": "new@mergington.edu"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Signed up new@mergington.edu for Chess Club"}
    assert "new@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity_returns_404(client):
    response = client.post(
        "/activities/Not A Real Club/signup", params={"email": "new@mergington.edu"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_400(client):
    response = client.post(
        "/activities/Chess Club/signup", params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_from_activity_success(client):
    response = client.delete(
        "/activities/Chess Club/unregister", params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Unregistered michael@mergington.edu from Chess Club"
    }
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_from_nonexistent_activity_returns_404(client):
    response = client.delete(
        "/activities/Not A Real Club/unregister", params={"email": "michael@mergington.edu"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_email_not_signed_up_returns_400(client):
    response = client.delete(
        "/activities/Chess Club/unregister", params={"email": "not-signed-up@mergington.edu"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
