from __future__ import annotations

from sqlalchemy.orm import Session

from app.incidents.incidents_model import Incident
from app.incidents.incidents_schema import IncidentCreate, IncidentUpdate


class IncidentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, incident_in: IncidentCreate) -> Incident:
        incident = Incident(**incident_in.model_dump())
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def create_from_payload(self, payload: dict) -> Incident:
        incident = Incident(**payload)
        self.db.add(incident)
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def get_all(self) -> list[Incident]:
        return self.db.query(Incident).order_by(Incident.id.asc()).all()

    def get_by_id(self, incident_id: int) -> Incident | None:
        return self.db.query(Incident).filter(Incident.id == incident_id).first()

    def update(self, incident: Incident, incident_in: IncidentUpdate) -> Incident:
        for field, value in incident_in.model_dump(exclude_unset=True).items():
            setattr(incident, field, value)
        self.db.commit()
        self.db.refresh(incident)
        return incident

    def delete(self, incident: Incident) -> None:
        self.db.delete(incident)
        self.db.commit()
