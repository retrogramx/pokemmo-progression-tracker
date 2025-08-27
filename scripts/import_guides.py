"""Script to import PokeMMO guides from JSON files into the database."""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlmodel import Session

from pokemmo_companion.core.db import get_engine
from pokemmo_companion.core.services.guide_loader import load_guides_from_dir


if __name__ == "__main__":
    engine = get_engine()
    with Session(engine) as s:
        load_guides_from_dir(Path("data"), s, mode="replace")
