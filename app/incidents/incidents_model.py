from __future__ import annotations

from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class IncidentUrgency(str, Enum):
    IMMEDIATE_ATTENTION = "immediate-attention"
    ROUTINE_REVIEW = "routine-review"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    incident: Mapped[str] = mapped_column(Text, nullable=False)
    urgency: Mapped[IncidentUrgency] = mapped_column(
        SqlEnum(IncidentUrgency, name="incident_urgency"),
        nullable=False,
    )
    send_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    assigned_department: Mapped[str] = mapped_column(String(255), nullable=False)
    action_taken: Mapped[str] = mapped_column(Text, nullable=False)
    action_brief_description: Mapped[str] = mapped_column(Text, nullable=False)
