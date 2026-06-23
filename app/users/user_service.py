from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.users.user_repository import UserRepository
from app.users.user_schema import UserCreate, UserLogin, UserSession, UserUpdate
from app.users.user_session import create_session_token, decode_session_token


class UserService:
    def __init__(self, db: Session) -> None:
        self.repository = UserRepository(db)

    def create_user(self, user_in: UserCreate):
        existing_user = self.repository.get_by_username(user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists.",
            )
        return self.repository.create(user_in)

    def login_user(self, credentials: UserLogin) -> UserSession:
        user = self.repository.get_by_username(credentials.username)
        if not user or user.password != credentials.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )
        return UserSession(
            token=create_session_token(user_id=user.id, username=user.username),
            user=user,
        )

    def get_user_from_session(self, token: str):
        try:
            payload = decode_session_token(token)
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(exc),
            ) from exc

        user = self.repository.get_by_id(int(payload["user_id"]))
        if not user or user.username != payload["username"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid session token.",
            )
        return user

    def get_users(self):
        return self.repository.get_all()

    def get_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )
        return user

    def update_user(self, user_id: int, user_in: UserUpdate):
        user = self.get_user(user_id)

        if user_in.username and user_in.username != user.username:
            existing_user = self.repository.get_by_username(user_in.username)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists.",
                )

        return self.repository.update(user, user_in)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.repository.delete(user)
