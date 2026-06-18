from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.database import initialize_database
from app.incidents.incidents_service import load_trained_models
from app.incidents.incidents_router import router as incidents_router
from app.users.user_router import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.incident_models = load_trained_models()
    initialize_database()
    yield


app = FastAPI(title="IMS API", lifespan=lifespan)
app.include_router(user_router)
app.include_router(incidents_router)


@app.get("/")
def health_check() -> dict[str, str]:
    return {"message": "IMS API is running."}
