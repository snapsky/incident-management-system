from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from app.users.user_model import UserRole


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    designation: str = Field(..., min_length=1, max_length=255)
    username: str = Field(..., min_length=3, max_length=100)
    role: UserRole


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=255)


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=255)


class UserSession(BaseModel):
    token: str
    user: "UserResponse"


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    designation: str | None = Field(default=None, min_length=1, max_length=255)
    username: str | None = Field(default=None, min_length=3, max_length=100)
    role: UserRole | None = None
    password: str | None = Field(default=None, min_length=6, max_length=255)


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
