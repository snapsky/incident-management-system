from __future__ import annotations

from app.users.user_router import get_user_service


def test_session_route_requires_authorization_header(client):
    client.app.dependency_overrides[get_user_service] = lambda: object()

    response = client.get("/users/session")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authorization header is required."}

