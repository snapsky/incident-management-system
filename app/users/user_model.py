from __future__ import annotations

import os
from enum import Enum

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


ENUM_VALUES = lambda enum_cls: [member.value for member in enum_cls]


class UserRole(str, Enum):
    STAFF = "staff"
    ADMIN = "admin"
    DEPARTMENT_ADMIN = "department_admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    designation: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str | None] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole, name="user_role", values_callable=ENUM_VALUES),
        nullable=False,
        default=UserRole.STAFF,
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)


def create_admin_user_from_env(db: Session) -> None:
    admin_full_name = os.getenv("ADMIN_FULL_NAME")
    admin_designation = os.getenv("ADMIN_DESIGNATION", "Administrator")
    admin_department = os.getenv("ADMIN_DEPARTMENT")
    admin_username = os.getenv("ADMIN_USERNAME") or os.getenv("ADMIN_USER_NAME")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_role = os.getenv("ADMIN_ROLE") or os.getenv("ROLE", UserRole.ADMIN.value)

    if not admin_full_name or not admin_username or not admin_password:
        return

    if db.query(User).filter(User.username == admin_username).first():
        return

    role = UserRole(admin_role.lower())

    admin_user = User(
        full_name=admin_full_name,
        designation=admin_designation,
        department=admin_department,
        username=admin_username,
        role=role,
        password=admin_password,
    )
    db.add(admin_user)
    db.commit()
