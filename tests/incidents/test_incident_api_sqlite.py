from __future__ import annotations


def test_create_and_list_incident(api_client, mock_incident_service):
    user_response = api_client.post(
        "/users/",
        json={
            "full_name": "Reporter One",
            "designation": "Nurse",
            "department": None,
            "username": "reporter",
            "role": "staff",
            "password": "secret123",
        },
    )
    user_id = user_response.json()["id"]

    create_response = api_client.post(
        "/incidents/",
        json={
            "incident_date": "2026-07-07",
            "incident_time": "08:30:00",
            "incident": "Medication fridge is intermittently losing power.",
            "send_by": user_id,
            "action_taken": "Pending",
            "action_brief_description": "Awaiting maintenance review",
        },
    )

    assert create_response.status_code == 201
    incident_payload = create_response.json()
    assert incident_payload["assigned_department"] == "IT"
    assert incident_payload["urgency"] == "routine-review"
    assert incident_payload["send_by"] == user_id

    list_response = api_client.get("/incidents/")

    assert list_response.status_code == 200
    incidents = list_response.json()
    assert len(incidents) == 1
    assert incidents[0]["incident"] == "Medication fridge is intermittently losing power."


def test_create_incident_rejects_unknown_sender(api_client, mock_incident_service):
    response = api_client.post(
        "/incidents/",
        json={
            "incident": "Server room alarm is active.",
            "send_by": 999,
            "action_taken": "Pending",
            "action_brief_description": "Awaiting action",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Sender user not found."}
