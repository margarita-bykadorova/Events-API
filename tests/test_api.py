import requests
import time
from tests.conftest import BASE_URL


# Happy path tests

def test_health_endpoint_returns_healthy():
    response = requests.get(f"{BASE_URL}/health")

    # Assert: check for a valid status code
    assert response.status_code == 200

    # Assert: check if status is healthy
    assert response.json()["status"] == "healthy"


def test_register_user_creates_new_user():
    # Arrange: create a random user
    timestamp = int(time.time() * 1000)
    new_user = {
        "username": f"user_{timestamp}",
        "password": "pass"
    }

    # Act: register the user
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user)

    # Assert: check for a valid status code
    assert response.status_code == 201

    # Assert: response includes the created user and a correct username
    assert response.json()["user"]["username"] == new_user["username"]


def test_login_returns_jwt_token():
    # Arrange: create a user and ensure it exists
    new_user = {
        "username": "test",
        "password": "pass"
    }

    requests.post(f"{BASE_URL}/auth/register", json=new_user)

    # Act: log in the user
    response = requests.post(f"{BASE_URL}/auth/login", json=new_user)

    # Assert: check for a valid status code
    assert response.status_code == 200

    # Assert: response contains an access token
    assert response.json()["access_token"]


def test_create_public_event_succeeds_with_token(auth_token):
    # Arrange: set a public event body
    new_event = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    # Act: create a public event
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/events", json=new_event, headers=headers)

    # Assert: check for a valid status code
    assert response.status_code == 201

    # Assert: check if response fields are correct
    assert response.json()["title"] == new_event["title"]
    assert response.json()["date"] == new_event["date"]
    assert response.json()["is_public"] is True


def test_rsvp_to_public_event_succeeds_without_auth(public_event_id):
    # Arrange: set RSVP attending
    new_rsvp = {
        "attending": True
    }

    # Act: RSVP to an event
    response = requests.post(f"{BASE_URL}/rsvps/event/{public_event_id}", json=new_rsvp)

    # Assert: check for a valid status code
    assert response.status_code == 201

    # Assert: check if event_id is correct
    assert response.json()["event_id"] == public_event_id


# Edge-case tests

def test_duplicate_username_registration():
    # Arrange: create a random user
    timestamp = int(time.time() * 1000)
    new_user = {
        "username": f"user1_{timestamp}",
        "password": "pass"
    }

    # Act: register the user
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user)

    # Assert: check for a valid status code
    assert response.status_code == 201

    # Act: register the same user a second time
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user)

    # Assert: check for a bad request status code
    assert response.status_code == 400


def test_login_fails_with_wrong_password():
    # Arrange: create a random user and wrong credentials
    timestamp = int(time.time() * 1000)
    new_user = {
        "username": f"user2_{timestamp}",
        "password": "pass"
    }

    wrong_credentials = {
        "username": new_user["username"],
        "password": "wrong"
    }

    # Act: register the user
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user)

    # Assert: check for a valid status code
    assert response.status_code == 201

    # Act: try to log in with a wrong password
    response = requests.post(f"{BASE_URL}/auth/login", json=wrong_credentials)

    # Assert: check for an unauthorized status code
    assert response.status_code == 401


def test_create_public_event_requires_auth():
    # Arrange: set a public event body
    new_event = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    # Act: create a public event without auth_token
    response = requests.post(f"{BASE_URL}/events", json=new_event)

    # Assert: check for an unauthorized status code
    assert response.status_code == 401


def test_rsvp_non_public_event_requires_auth(non_public_event_id):
    # Arrange: set RSVP attending
    new_rsvp = {
        "attending": True
    }

    # Act: RSVP to a non-public event without a token
    response = requests.post(f"{BASE_URL}/rsvps/event/{non_public_event_id}", json=new_rsvp)

    # Assert: check for an unauthorized status code
    assert response.status_code == 401
