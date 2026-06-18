from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

from fastapi import HTTPException, status
import torch
from sqlalchemy.orm import Session
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from app.incidents.incidents_repository import IncidentRepository
from app.incidents.incidents_model import IncidentUrgency
from app.incidents.incidents_schema import IncidentCreate, IncidentUpdate
from app.users.user_repository import UserRepository


TRAINED_MODELS_DIR = Path(__file__).resolve().parents[1] / "trained_models"
DEPARTMENT_MODEL_DIR = TRAINED_MODELS_DIR / "distilbert_incident_classifier"
URGENCY_MODEL_DIR = TRAINED_MODELS_DIR / "xgboost_urgency_binary_screening"
URGENCY_MODEL_PATH = URGENCY_MODEL_DIR / "model.pkl"
URGENCY_METADATA_PATH = URGENCY_MODEL_DIR / "metadata.json"


def load_trained_models() -> dict[str, Any]:
    department_tokenizer = AutoTokenizer.from_pretrained(
        DEPARTMENT_MODEL_DIR,
        local_files_only=True,
    )
    department_model = AutoModelForSequenceClassification.from_pretrained(
        DEPARTMENT_MODEL_DIR,
        local_files_only=True,
    )
    department_model.eval()
    department_label_mapping = {
        int(key): value for key, value in department_model.config.id2label.items()
    }

    with URGENCY_MODEL_PATH.open("rb") as model_file:
        urgency_model = pickle.load(model_file)

    metadata = json.loads(URGENCY_METADATA_PATH.read_text(encoding="utf-8"))

    return {
        "department_tokenizer": department_tokenizer,
        "department_model": department_model,
        "department_label_mapping": department_label_mapping,
        "urgency_model": urgency_model,
        "urgency_threshold": float(metadata["selected_threshold"]),
        "urgency_positive_class": str(metadata["positive_class"]),
        "urgency_negative_class": str(metadata["negative_class"]),
    }


class IncidentService:
    def __init__(self, db: Session, model_bundle: dict[str, Any]) -> None:
        self.incident_repository = IncidentRepository(db)
        self.user_repository = UserRepository(db)
        self.model_bundle = model_bundle

    def create_incident(self, incident_in: IncidentCreate):
        self._ensure_sender_exists(incident_in.send_by)

        assigned_department = self._predict_department(incident_in.incident)
        urgency = self._predict_urgency(incident_in.incident)

        incident_payload = IncidentCreate(
            incident=incident_in.incident,
            send_by=incident_in.send_by,
            action_taken=incident_in.action_taken,
            action_brief_description=incident_in.action_brief_description,
        ).model_dump()
        incident_payload["assigned_department"] = assigned_department
        incident_payload["urgency"] = urgency

        return self.incident_repository.create_from_payload(incident_payload)

    def get_incidents(self):
        return self.incident_repository.get_all()

    def get_incident(self, incident_id: int):
        incident = self.incident_repository.get_by_id(incident_id)
        if not incident:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Incident not found.",
            )
        return incident

    def update_incident(self, incident_id: int, incident_in: IncidentUpdate):
        incident = self.get_incident(incident_id)
        if incident_in.send_by is not None:
            self._ensure_sender_exists(incident_in.send_by)
        return self.incident_repository.update(incident, incident_in)

    def delete_incident(self, incident_id: int) -> None:
        incident = self.get_incident(incident_id)
        self.incident_repository.delete(incident)

    def _ensure_sender_exists(self, user_id: int) -> None:
        if not self.user_repository.get_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sender user not found.",
            )

    def _predict_department(self, incident_text: str) -> str:
        department_tokenizer = self.model_bundle.get("department_tokenizer")
        department_model = self.model_bundle.get("department_model")
        department_label_mapping = self.model_bundle.get("department_label_mapping")

        if (
            department_tokenizer is None
            or department_model is None
            or department_label_mapping is None
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Department classifier is not loaded.",
            )

        encoded = department_tokenizer(
            incident_text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512,
        )

        with torch.no_grad():
            logits = department_model(**encoded).logits

        predicted_label = int(torch.argmax(logits, dim=1).item())
        return department_label_mapping[predicted_label]

    def _predict_urgency(self, incident_text: str) -> IncidentUrgency:
        urgency_model = self.model_bundle.get("urgency_model")
        urgency_threshold = self.model_bundle.get("urgency_threshold")
        urgency_positive_class = self.model_bundle.get("urgency_positive_class")
        urgency_negative_class = self.model_bundle.get("urgency_negative_class")

        if (
            urgency_model is None
            or urgency_threshold is None
            or urgency_positive_class is None
            or urgency_negative_class is None
        ):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Urgency classifier is not loaded.",
            )

        probability = float(urgency_model.predict_proba([incident_text])[0][1])
        predicted_class = (
            urgency_positive_class
            if probability >= urgency_threshold
            else urgency_negative_class
        )
        return IncidentUrgency(predicted_class)
