"""Tests for the guide loader service."""

import json
from pathlib import Path
from pokemmo_companion.core.services.guide_loader import (
    load_guides_from_dir,
    _guide_key,
    _iter_steps,
)
from pokemmo_companion.core.models import Guide, GuideStep


def test_guide_key():
    """Test guide key generation."""
    assert _guide_key("Kanto") == "kanto"
    assert _guide_key("  Johto  ") == "johto"
    assert _guide_key("HOENN") == "hoenn"


def test_iter_steps():
    """Test step iteration from guide payload."""
    payload = {
        "sections": [
            {"title": "Section 1", "steps": ["Step 1", "Step 2"]},
            {"title": "Section 2", "steps": ["Step 3"]},
        ]
    }
    
    steps = list(_iter_steps(payload))
    assert len(steps) == 3
    
    assert steps[0].section_index == 1
    assert steps[0].section_title == "Section 1"
    assert steps[0].step_index == 1
    assert steps[0].text == "Step 1"
    
    assert steps[1].section_index == 1
    assert steps[1].step_index == 2
    assert steps[1].text == "Step 2"
    
    assert steps[2].section_index == 2
    assert steps[2].step_index == 1
    assert steps[2].text == "Step 3"


def test_load_guides_from_dir_fresh_db(session, tmp_path):
    """Test loading guides into a fresh database."""
    # Create test guide data
    guide_data = {
        "region": "TestRegion",
        "sections": [
            {"title": "Test Section", "steps": ["Test Step 1", "Test Step 2"]}
        ],
    }
    
    guide_file = tmp_path / "guide_test.json"
    with guide_file.open("w") as f:
        json.dump(guide_data, f)
    
    # Load guides
    load_guides_from_dir(tmp_path, session, mode="replace")
    
    # Verify guide was created
    guide = session.exec(
        session.query(Guide).where(Guide.key == "testregion")
    ).first()
    assert guide is not None
    assert guide.title == "TestRegion Guide"
    assert "region:testregion" in guide.tags
    
    # Verify steps were created
    steps = session.exec(
        session.query(GuideStep).where(GuideStep.guide_id == guide.id)
    ).all()
    assert len(steps) == 2
    
    # Check first step
    step1 = next(s for s in steps if s.step_index == 1)
    assert step1.section_index == 1
    assert step1.title == "Test Section"
    assert step1.text == "Test Step 1"
    assert "region:testregion" in step1.tags
    assert "section:1" in step1.tags


def test_load_guides_from_dir_merge_mode(session, tmp_path):
    """Test loading guides in merge mode."""
    # Create initial guide
    guide = Guide(key="testregion", title="Test Guide", tags=["region:testregion"])
    session.add(guide)
    session.commit()
    session.refresh(guide)
    
    # Create initial step
    step = GuideStep(
        guide_id=guide.id,
        section_index=1,
        step_index=1,
        title="Existing Section",
        text="Existing Step",
        tags=["region:testregion", "section:1"],
    )
    session.add(step)
    session.commit()
    
    # Create new guide data with overlapping and new content
    guide_data = {
        "region": "TestRegion",
        "sections": [
            {"title": "Existing Section", "steps": ["Existing Step", "New Step"]},
            {"title": "New Section", "steps": ["Another Step"]},
        ],
    }
    
    guide_file = tmp_path / "guide_test.json"
    with guide_file.open("w") as f:
        json.dump(guide_data, f)
    
    # Load guides in merge mode
    load_guides_from_dir(tmp_path, session, mode="merge")
    
    # Verify existing step wasn't duplicated
    existing_steps = session.exec(
        session.query(GuideStep).where(
            GuideStep.guide_id == guide.id,
            GuideStep.section_index == 1,
            GuideStep.step_index == 1,
        )
    ).all()
    assert len(existing_steps) == 1
    
    # Verify new steps were added
    all_steps = session.exec(
        session.query(GuideStep).where(GuideStep.guide_id == guide.id)
    ).all()
    assert len(all_steps) == 3


def test_load_guides_from_dir_replace_mode(session, tmp_path):
    """Test loading guides in replace mode."""
    # Create initial guide with steps
    guide = Guide(key="testregion", title="Test Guide", tags=["region:testregion"])
    session.add(guide)
    session.commit()
    session.refresh(guide)
    
    step = GuideStep(
        guide_id=guide.id,
        section_index=1,
        step_index=1,
        title="Old Section",
        text="Old Step",
        tags=["region:testregion", "section:1"],
    )
    session.add(step)
    session.commit()
    
    # Create new guide data
    guide_data = {
        "region": "TestRegion",
        "sections": [
            {"title": "New Section", "steps": ["New Step"]}
        ],
    }
    
    guide_file = tmp_path / "guide_test.json"
    with guide_file.open("w") as f:
        json.dump(guide_data, f)
    
    # Load guides in replace mode
    load_guides_from_dir(tmp_path, session, mode="replace")
    
    # Verify old step was replaced
    old_steps = session.exec(
        session.query(GuideStep).where(GuideStep.text == "Old Step")
    ).all()
    assert len(old_steps) == 0
    
    # Verify new step was added
    new_steps = session.exec(
        session.query(GuideStep).where(GuideStep.text == "New Step")
    ).all()
    assert len(new_steps) == 1


def test_load_guides_from_dir_invalid_json(session, tmp_path, caplog):
    """Test handling of invalid JSON files."""
    # Create invalid JSON file
    guide_file = tmp_path / "guide_invalid.json"
    guide_file.write_text("invalid json content")
    
    # Create valid guide file
    guide_data = {
        "region": "ValidRegion",
        "sections": [{"title": "Section", "steps": ["Step"]}],
    }
    valid_file = tmp_path / "guide_valid.json"
    with valid_file.open("w") as f:
        json.dump(guide_data, f)
    
    # Load guides
    load_guides_from_dir(tmp_path, session, mode="replace")
    
    # Verify error was logged
    assert "Failed to import guide from" in caplog.text
    
    # Verify valid guide was still loaded
    guide = session.exec(
        session.query(Guide).where(Guide.key == "validregion")
    ).first()
    assert guide is not None


def test_load_guides_from_dir_missing_region(session, tmp_path, caplog):
    """Test handling of guide files without region field."""
    # Create guide data without region
    guide_data = {
        "sections": [{"title": "Section", "steps": ["Step"]}],
    }
    
    guide_file = tmp_path / "guide_no_region.json"
    with guide_file.open("w") as f:
        json.dump(guide_data, f)
    
    # Load guides
    load_guides_from_dir(tmp_path, session, mode="replace")
    
    # Verify warning was logged
    assert "Skipping" in caplog.text
    assert "no 'region'" in caplog.text
    
    # Verify no guide was created
    guides = session.exec(session.query(Guide)).all()
    assert len(guides) == 0
