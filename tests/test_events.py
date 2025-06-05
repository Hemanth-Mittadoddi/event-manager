from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_event():
    response = client.post("/events/", json={
        "name": "Workshop",
        "location": "Bangalore",
        "start_time": "2025-06-06T14:00:00",
        "end_time": "2025-06-06T16:00:00",
        "timezone": "Asia/Kolkata",
        "max_attendees": 50
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Workshop"

def test_register_attendee():
    event_id = 1
    response = client.post(f"/events/{event_id}/attendees/", json={
        "name": "Alice",
        "email": "alice@example.com"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"

def test_prevent_duplicate_registration():
    event_id = 1
    client.post(f"/events/{event_id}/attendees/", json={
        "name": "Bob",
        "email": "bob@example.com"
    })
    response = client.post(f"/events/{event_id}/attendees/", json={
        "name": "Bob",
        "email": "bob@example.com"
    })
    assert response.status_code == 400

def test_overbooking():
    event_id = 1
    for i in range(50):
        client.post(f"/events/{event_id}/attendees/", json={
            "name": f"User{i}",
            "email": f"user{i}@example.com"
        })
    response = client.post(f"/events/{event_id}/attendees/", json={
        "name": "Extra",
        "email": "extra@example.com"
    })
    assert response.status_code == 400