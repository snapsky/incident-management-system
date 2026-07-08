from __future__ import annotations

from contextlib import asynccontextmanager

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.database import Base, get_db
from app.incidents.incidents_router import get_incident_service
from app.incidents.incidents_service import IncidentService
from app.main import app


@pytest.fixture
def client():
    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def noop_lifespan(_app):
        yield

    app.router.lifespan_context = noop_lifespan
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.router.lifespan_context = original_lifespan
        app.dependency_overrides.clear()


@pytest.fixture
def sqlite_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def api_client(sqlite_session):
    original_lifespan = app.router.lifespan_context

    @asynccontextmanager
    async def noop_lifespan(_app):
        yield

    def override_get_db():
        try:
            yield sqlite_session
        finally:
            pass

    app.router.lifespan_context = noop_lifespan
    app.state.incident_models = {"stub": True}
    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.router.lifespan_context = original_lifespan
        app.dependency_overrides.clear()
        if hasattr(app.state, "incident_models"):
            delattr(app.state, "incident_models")


@pytest.fixture
def mock_incident_service(api_client, sqlite_session, monkeypatch):
    def build_service():
        service = IncidentService(sqlite_session, {"stub": True})
        monkeypatch.setattr(service, "_predict_department", lambda text: "IT")
        monkeypatch.setattr(service, "_predict_urgency", lambda text: "routine-review")
        return service

    app.dependency_overrides[get_incident_service] = build_service
    return build_service
