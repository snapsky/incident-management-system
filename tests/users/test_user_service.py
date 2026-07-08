from __future__ import annotations

from types import SimpleNamespace

import pytest
from fastapi import HTTPException, status

from app.users.user_model import UserRole
from app.users.user_schema import UserCreate, UserLogin
from app.users.user_service import UserService


def build_user_create(**overrides) -> UserCreate:
    payload = {
        "full_name": "Alice Smith",
        "designation": "Engineer",
        "department": None,
        "username": "alice",
        "role": UserRole.STAFF,
        "password": "secret123",
    }
    payload.update(overrides)
    return UserCreate(**payload)


def test_create_user_rejects_duplicate_username():
    service = UserService(db=None)
    service.repository = SimpleNamespace(
        get_by_username=lambda username: SimpleNamespace(id=1, username=username),
        create=lambda user_in: user_in,
    )

    with pytest.raises(HTTPException) as exc:
        service.create_user(build_user_create())

    assert exc.value.status_code == status.HTTP_409_CONFLICT
    assert exc.value.detail == "Username already exists."


def test_create_user_requires_department_for_department_admin():
    service = UserService(db=None)
    service.repository = SimpleNamespace(
        get_by_username=lambda username: None,
        create=lambda user_in: user_in,
    )

    with pytest.raises(HTTPException) as exc:
        service.create_user(build_user_create(role=UserRole.DEPARTMENT_ADMIN))

    assert exc.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert exc.value.detail == "Department admin users must have a department."


def test_login_user_rejects_invalid_credentials():
    service = UserService(db=None)
    service.repository = SimpleNamespace(
        get_by_username=lambda username: SimpleNamespace(
            id=1,
            username=username,
            password="different-password",
        )
    )

    with pytest.raises(HTTPException) as exc:
        service.login_user(UserLogin(username="alice", password="secret123"))

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.detail == "Invalid username or password."

