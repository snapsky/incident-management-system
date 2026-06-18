from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.users.user_repository import UserRepository
from app.users.user_schema import UserCreate, UserUpdate


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
