from __future__ import annotations

from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, Field

from app.incidents.incidents_model import IncidentStatus, IncidentUrgency


class IncidentBase(BaseModel):
    incident_date: date | None = None
    incident_time: time | None = None
    incident: str = Field(..., min_length=1)
    send_by: int


class IncidentCreate(IncidentBase):
    status: IncidentStatus = IncidentStatus.PENDING
    action_taken: str = Field(default="Pending", min_length=1)
    action_brief_description: str = Field(default="Awaiting action", min_length=1)


class IncidentUpdate(BaseModel):
    incident_date: date | None = None
    incident_time: time | None = None
    incident: str | None = Field(default=None, min_length=1)
    urgency: IncidentUrgency | None = None
    status: IncidentStatus | None = None
    send_by: int | None = None
    assigned_department: str | None = Field(default=None, min_length=1, max_length=255)
    action_taken: str | None = Field(default=None, min_length=1)
    action_brief_description: str | None = Field(default=None, min_length=1)


class IncidentResponse(IncidentBase):
    id: int
    created_at: datetime | None = None
    urgency: IncidentUrgency
    status: IncidentStatus
    assigned_department: str

    model_config = ConfigDict(from_attributes=True)
