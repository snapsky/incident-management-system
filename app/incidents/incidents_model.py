from __future__ import annotations

from datetime import date, datetime, time
from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, Text, Time, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


ENUM_VALUES = lambda enum_cls: [member.value for member in enum_cls]


class IncidentUrgency(str, Enum):
    IMMEDIATE_ATTENTION = "immediate-attention"
    ROUTINE_REVIEW = "routine-review"


class IncidentStatus(str, Enum):
    PENDING = "pending"
    RESOLVED = "resolved"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, server_default=func.now())
    incident_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    incident_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    incident: Mapped[str] = mapped_column(Text, nullable=False)
    urgency: Mapped[IncidentUrgency] = mapped_column(
        SqlEnum(IncidentUrgency, name="incident_urgency", values_callable=ENUM_VALUES),
        nullable=False,
    )
    status: Mapped[IncidentStatus] = mapped_column(
        SqlEnum(IncidentStatus, name="incident_status", values_callable=ENUM_VALUES),
        nullable=False,
        default=IncidentStatus.PENDING,
    )
    send_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    assigned_department: Mapped[str] = mapped_column(String(255), nullable=False)
    action_taken: Mapped[str] = mapped_column(Text, nullable=False)
    action_brief_description: Mapped[str] = mapped_column(Text, nullable=False)
