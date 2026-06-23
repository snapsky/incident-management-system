from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.users.user_schema import UserCreate, UserLogin, UserResponse, UserSession, UserUpdate
from app.users.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.create_user(user_in)


@router.post("/login", response_model=UserSession)
def login_user(
    credentials: UserLogin,
    service: UserService = Depends(get_user_service),
) -> UserSession:
    return service.login_user(credentials)


@router.get("/session", response_model=UserResponse)
def get_current_session_user(
    authorization: str | None = Header(default=None),
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required.",
        )

    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session token is required.",
        )

    return service.get_user_from_session(token)


@router.get("/", response_model=list[UserResponse])
def list_users(service: UserService = Depends(get_user_service)) -> list[UserResponse]:
    return service.get_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return service.update_user(user_id, user_in)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> Response:
    service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
