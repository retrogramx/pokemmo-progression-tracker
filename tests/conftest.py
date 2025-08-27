"""Pytest configuration and fixtures for PokeMMO Companion App."""

import pytest
from pathlib import Path
from sqlmodel import Session, create_engine
from pokemmo_companion.core.models import SQLModel


@pytest.fixture
def temp_db():
    """Create a temporary SQLite database for testing."""
    db_path = Path("test_pokemmo_tracker.db")
    
    # Create engine
    engine = create_engine(
        f"sqlite:///{db_path}",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    yield engine
    
    # Cleanup
    engine.dispose()
    if db_path.exists():
        db_path.unlink()


@pytest.fixture
def session(temp_db):
    """Create a database session for testing."""
    with Session(temp_db) as session:
        yield session
