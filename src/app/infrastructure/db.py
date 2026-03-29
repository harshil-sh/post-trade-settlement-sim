from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.domain.models import Base
from app.infrastructure.config import settings

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
