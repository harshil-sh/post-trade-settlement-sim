from collections.abc import Generator

from app.infrastructure.db import SessionLocal


def get_db() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
