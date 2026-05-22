import pytest
import requests
import time

BASE_URL = "http://localhost:5000/api"


@pytest.fixture
def auth_token():
    # create a random user
    timestamp = int(time.time() * 1000)
    new_user = {
        "username": f"user_{timestamp}",
        "password": "pass"
    }

    # register the user
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user)
    assert response.status_code == 201

    # log in the user
    response = requests.post(f"{BASE_URL}/auth/login", json=new_user)
    assert response.status_code == 200

    # return the token
    token = response.json()["access_token"]
    return token


@pytest.fixture
def public_event_id(auth_token):
    # set a public event body
    new_event = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    # create an event
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/events", json=new_event, headers=headers)
    assert response.status_code == 201

    # return event id
    return response.json()["id"]


@pytest.fixture
def non_public_event_id(auth_token):
    # set an event body
    new_event = {
        "title": "Team Building Workshop",
        "description": "Internal team building activities",
        "date": "2026-01-20T14:00:00",
        "location": "Conference Room A",
        "capacity": 30,
        "is_public": False,
        "requires_admin": False
    }

    # create an event
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/events", json=new_event, headers=headers)
    assert response.status_code == 201

    # return event id
    return response.json()["id"]
