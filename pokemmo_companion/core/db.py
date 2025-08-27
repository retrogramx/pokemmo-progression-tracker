"""Database utilities for the PokeMMO Companion App."""

from pathlib import Path
from sqlmodel import SQLModel, create_engine

DB_PATH = Path("pokemmo_tracker.db")


def get_engine(echo: bool = False):
    """Get a SQLAlchemy engine instance."""
    return create_engine(
        f"sqlite:///{DB_PATH}",
        echo=echo,
        connect_args={"check_same_thread": False},
    )


def init_db(engine=None):
    """Initialize the database with all models.
    
    Prefer Alembic migrations; this is a fallback for a fresh DB.
    """
    from pokemmo_companion.core import models  # ensure models register metadata
    
    engine = engine or get_engine()
    SQLModel.metadata.create_all(engine)
    return engine
