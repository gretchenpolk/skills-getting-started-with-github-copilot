from src.app import activities


def test_successful_signup(client):
    email = "testuser@example.com"
    resp = client.post("/activities/Chess%20Club/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert resp.json()["message"] == f"Signed up {email} for Chess Club"


def test_already_signed_up(client):
    resp = client.post("/activities/Chess%20Club/signup", params={"email": "michael@mergington.edu"})
    assert resp.status_code == 400


def test_nonexistent_activity(client):
    resp = client.post("/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    assert resp.status_code == 404


def test_full_capacity(client):
    activities["Tiny Club"] = {
        "description": "Tiny",
        "schedule": "Now",
        "max_participants": 1,
        "participants": ["full@mergington.edu"],
    }
    resp = client.post("/activities/Tiny%20Club/signup", params={"email": "new@mergington.edu"})
    assert resp.status_code == 400
