from __future__ import annotations


def test_create_login_and_restore_session(api_client):
    create_response = api_client.post(
        "/users/",
        json={
            "full_name": "Alice Smith",
            "designation": "Engineer",
            "department": None,
            "username": "alice",
            "role": "staff",
            "password": "secret123",
        },
    )

    assert create_response.status_code == 201
    assert create_response.json()["username"] == "alice"

    login_response = api_client.post(
        "/users/login",
        json={"username": "alice", "password": "secret123"},
    )

    assert login_response.status_code == 200
    login_payload = login_response.json()
    assert login_payload["user"]["username"] == "alice"
    assert login_payload["token"]

    session_response = api_client.get(
        "/users/session",
        headers={"Authorization": f"Bearer {login_payload['token']}"},
    )

    assert session_response.status_code == 200
    assert session_response.json()["full_name"] == "Alice Smith"


def test_create_user_rejects_duplicate_username(api_client):
    payload = {
        "full_name": "Alice Smith",
        "designation": "Engineer",
        "department": None,
        "username": "alice",
        "role": "staff",
        "password": "secret123",
    }

    assert api_client.post("/users/", json=payload).status_code == 201
    duplicate_response = api_client.post("/users/", json=payload)

    assert duplicate_response.status_code == 409
    assert duplicate_response.json() == {"detail": "Username already exists."}
