"""Guide loading service for importing PokeMMO guides from JSON files."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Literal
from sqlmodel import Session, select

from pokemmo_companion.core.models import Guide, GuideStep

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class LoadedStep:
    """A step loaded from a guide JSON file."""
    
    section_index: int
    section_title: str
    step_index: int
    text: str


def _iter_steps(payload: dict) -> Iterable[LoadedStep]:
    """Iterate over all steps in a guide payload."""
    for s_idx, section in enumerate(payload.get("sections", []), start=1):
        title = str(section.get("title", f"Section {s_idx}"))
        for t_idx, line in enumerate(section.get("steps", []), start=1):
            yield LoadedStep(s_idx, title, t_idx, str(line))


def _load_json(path: Path) -> dict:
    """Load and parse a JSON file."""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _guide_key(region: str) -> str:
    """Generate a guide key from a region name."""
    return region.strip().lower()


def load_guides_from_dir(
    data_dir: Path | str,
    session: Session,
    mode: Literal["replace", "merge"] = "replace",
) -> None:
    """Load all guide files from a directory into the database.
    
    Args:
        data_dir: Directory containing guide_*.json files
        session: Database session
        mode: Whether to replace existing guides or merge with them
    """
    data_dir = Path(data_dir)
    
    for path in sorted(data_dir.glob("guide_*.json")):
        try:
            payload = _load_json(path)
            region = str(payload.get("region", "")).strip()
            
            if not region:
                log.warning("Skipping %s (no 'region')", path.name)
                continue

            key, title = _guide_key(region), f"{region} Guide"

            # Find or create guide
            guide = session.exec(select(Guide).where(Guide.key == key)).first()
            if guide is None:
                guide = Guide(key=key, title=title, tags=[f"region:{key}"])
                session.add(guide)
                session.commit()
                session.refresh(guide)
            else:
                # Update guide if needed
                changed = False
                if guide.title != title:
                    guide.title = title
                    changed = True
                
                tags = set(guide.tags or [])
                if f"region:{key}" not in tags:
                    guide.tags = sorted(tags | {f"region:{key}"})
                    changed = True
                
                if changed:
                    session.add(guide)
                    session.commit()

            # Handle existing steps based on mode
            if mode == "replace":
                for existing_step in session.exec(
                    select(GuideStep).where(GuideStep.guide_id == guide.id)
                ).all():
                    session.delete(existing_step)
                session.commit()

            # Insert new steps
            inserted = merged = 0
            for step in _iter_steps(payload):
                tags = [f"region:{key}", f"section:{step.section_index}"]
                
                if mode == "merge":
                    # Check for duplicates
                    duplicate = session.exec(
                        select(GuideStep).where(
                            GuideStep.guide_id == guide.id,
                            GuideStep.section_index == step.section_index,
                            GuideStep.step_index == step.step_index,
                        )
                    ).first()
                    if duplicate:
                        merged += 1
                        continue

                session.add(
                    GuideStep(
                        guide_id=guide.id,
                        section_index=step.section_index,
                        step_index=step.step_index,
                        title=step.section_title,
                        text=step.text,
                        tags=tags,
                    )
                )
                inserted += 1

            session.commit()
            log.info(
                "Imported %s: %d inserted, %d merged (mode=%s)",
                region,
                inserted,
                merged,
                mode,
            )
            
        except Exception as e:
            log.error("Failed to import guide from %s: %s", path, e)
            session.rollback()
            continue
