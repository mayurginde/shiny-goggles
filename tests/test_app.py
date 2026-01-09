import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def get_initial_activities():
    return {
        "Basketball": {
            "description": "Team sport focusing on basketball skills and competitive play",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis techniques and participate in friendly matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 10,
            "participants": ["alex@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking and critical thinking through competitive debate",
            "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Build and program robots for competitions and projects",
            "schedule": "Tuesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["ethan@mergington.edu"]
        },
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities dictionary before each test"""
    global activities
    activities.clear()
    activities.update(get_initial_activities())

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Basketball" in data
    assert "participants" in data["Basketball"]


def test_signup_for_activity():
    response = client.post("/activities/Basketball/signup?email=testuser@mergington.edu")
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Basketball" in response.json()["message"]
    # Try signing up again (should fail)
    response = client.post("/activities/Basketball/signup?email=testuser@mergington.edu")
    assert response.status_code == 400


def test_unregister_participant():
    # First, sign up a user
    client.post("/activities/Tennis Club/signup?email=deleteuser@mergington.edu")
    # Now, unregister
    response = client.post(
        "/activities/Tennis Club/unregister",
        json={"email": "deleteuser@mergington.edu"}
    )
    assert response.status_code == 200
    assert "Removed deleteuser@mergington.edu from Tennis Club" in response.json()["message"]
    # Try unregistering again (should fail)
    response = client.post(
        "/activities/Tennis Club/unregister",
        json={"email": "deleteuser@mergington.edu"}
    )
    assert response.status_code == 400
