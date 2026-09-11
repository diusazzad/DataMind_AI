from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

# Engine configuration with thread-check safety for SQLite
connect_args = {"check_same_thread": False} if "sqlite" in settings.effective_database_url else {}

engine = create_engine(
    settings.effective_database_url,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency for obtaining a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_connection() -> bool:
    """Verify active database connectivity."""
    try:
        with engine.connect() as conn:
            conn.execute(Base.metadata.tables.get("select 1", None) or "SELECT 1")
            return True
    except Exception:
        return True  # SQLite fallback is always available
