from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)


def test_signup_and_unregister_flow():
    activity = "Soccer Team"
    email = "pytest_user+1@example.com"

    # Ensure email not present initially
    res = client.get("/activities")
    assert res.status_code == 200
    assert email not in res.json()[activity]["participants"]

    # Sign up
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # Now participant should be present
    res = client.get("/activities")
    assert email in res.json()[activity]["participants"]

    # Duplicate signup should fail
    res = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert res.status_code == 400

    # Unregister
    res = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert res.status_code == 200
    assert "Unregistered" in res.json().get("message", "")

    # Ensure removal
    res = client.get("/activities")
    assert email not in res.json()[activity]["participants"]
