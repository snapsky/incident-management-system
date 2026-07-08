from __future__ import annotations


def test_health_check_returns_expected_payload(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "IMS API is running."}

