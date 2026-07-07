from __future__ import annotations

import os
from pathlib import Path
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)

DB_DRIVER = os.getenv("DB_DRIVER", "mysql+pymysql")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "incidents_management_system")

DATABASE_URL = URL.create(
    drivername=DB_DRIVER,
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def initialize_database() -> None:
    server_url = URL.create(
        drivername=DB_DRIVER,
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )
    server_engine = create_engine(server_url, isolation_level="AUTOCOMMIT")

    with server_engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))

    server_engine.dispose()
    Base.metadata.create_all(bind=engine)
    _sync_mysql_enum_columns()

    from app.users.user_model import create_admin_user_from_env

    db = SessionLocal()
    try:
        create_admin_user_from_env(db)
    finally:
        db.close()


def _sync_mysql_enum_columns() -> None:
    if not DB_DRIVER.startswith("mysql"):
        return

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                ALTER TABLE incidents
                MODIFY COLUMN urgency VARCHAR(64) NOT NULL
                """
            )
        )
        connection.execute(
            text(
                """
                UPDATE incidents
                SET urgency = CASE
                    WHEN urgency = 'IMMEDIATE_ATTENTION' THEN 'immediate-attention'
                    WHEN urgency = 'ROUTINE_REVIEW' THEN 'routine-review'
                    ELSE urgency
                END
                """
            )
        )
        connection.execute(
            text(
                """
                ALTER TABLE incidents
                MODIFY COLUMN urgency ENUM('immediate-attention', 'routine-review')
                NOT NULL
                """
            )
        )
        connection.execute(
            text(
                """
                ALTER TABLE incidents
                MODIFY COLUMN status VARCHAR(32) NOT NULL
                """
            )
        )
        connection.execute(
            text(
                """
                UPDATE incidents
                SET status = CASE
                    WHEN status = 'PENDING' THEN 'pending'
                    WHEN status = 'RESOLVED' THEN 'resolved'
                    ELSE status
                END
                """
            )
        )
        connection.execute(
            text(
                """
                ALTER TABLE incidents
                MODIFY COLUMN status ENUM('pending', 'resolved')
                NOT NULL DEFAULT 'pending'
                """
            )
        )
        connection.execute(
            text(
                """
                ALTER TABLE users
                MODIFY COLUMN role ENUM('staff', 'admin', 'department_admin')
                NOT NULL DEFAULT 'staff'
                """
            )
        )
