from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# 1. Database Engine
# Agar SQLite use ho raha ho to 'check_same_thread: False' zaroori hota hai
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,  # Console me queries dekhni hon to True karein
)

# 2. Database Session Factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


# 3. get_db Dependency
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency: Har API request ke liye fresh database session create karta hai,
    aur request complete hone par session ko automatically close kar deta hai.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
