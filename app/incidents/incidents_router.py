from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.incidents.incidents_schema import IncidentCreate, IncidentResponse, IncidentUpdate
from app.incidents.incidents_service import IncidentService


router = APIRouter(prefix="/incidents", tags=["Incidents"])


def get_incident_service(
    request: Request,
    db: Session = Depends(get_db),
) -> IncidentService:
    model_bundle = getattr(request.app.state, "incident_models", None)
    if model_bundle is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Incident models are not loaded.",
        )
    return IncidentService(db, model_bundle)


@router.post("/", response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
def create_incident(
    incident_in: IncidentCreate,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    return service.create_incident(incident_in)


@router.get("/", response_model=list[IncidentResponse])
def list_incidents(
    service: IncidentService = Depends(get_incident_service),
) -> list[IncidentResponse]:
    return service.get_incidents()


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(
    incident_id: int,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    return service.get_incident(incident_id)


@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    incident_in: IncidentUpdate,
    service: IncidentService = Depends(get_incident_service),
) -> IncidentResponse:
    return service.update_incident(incident_id, incident_in)


@router.delete("/{incident_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_incident(
    incident_id: int,
    service: IncidentService = Depends(get_incident_service),
) -> Response:
    service.delete_incident(incident_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
