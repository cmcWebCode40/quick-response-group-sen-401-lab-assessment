"""Database engine and session configuration."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./db/inventory.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
