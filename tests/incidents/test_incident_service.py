from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi import HTTPException, status

from app.incidents.incidents_model import IncidentUrgency
from app.incidents.incidents_schema import IncidentCreate
from app.incidents.incidents_service import IncidentService


def build_incident_create(**overrides) -> IncidentCreate:
    payload = {
        "incident": "Ward monitor is not functioning correctly.",
        "send_by": 1,
        "action_taken": "Pending",
        "action_brief_description": "Awaiting action",
    }
    payload.update(overrides)
    return IncidentCreate(**payload)


def test_create_incident_rejects_unknown_sender():
    service = IncidentService(db=None, model_bundle={})
    service.user_repository = SimpleNamespace(get_by_id=lambda user_id: None)

    with pytest.raises(HTTPException) as exc:
        service.create_incident(build_incident_create())

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == "Sender user not found."


def test_create_incident_assigns_predictions_and_persists_payload():
    captured = {}
    service = IncidentService(db=None, model_bundle={})
    service.user_repository = SimpleNamespace(
        get_by_id=lambda user_id: SimpleNamespace(id=user_id)
    )
    service.incident_repository = SimpleNamespace(
        create_from_payload=lambda payload: captured.setdefault("payload", payload)
    )
    service._predict_department = lambda text: "IT"
    service._predict_urgency = lambda text: IncidentUrgency.IMMEDIATE_ATTENTION

    result = service.create_incident(build_incident_create())

    assert result["assigned_department"] == "IT"
    assert result["urgency"] == IncidentUrgency.IMMEDIATE_ATTENTION
    assert captured["payload"]["incident"] == "Ward monitor is not functioning correctly."

