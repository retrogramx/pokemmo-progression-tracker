"""Core data models for the PokeMMO Companion App."""

from typing import Optional, List
from sqlmodel import SQLModel, Field, Column, JSON


class Guide(SQLModel, table=True):
    """A guide for a specific region in PokeMMO."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    title: str
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))


class GuideStep(SQLModel, table=True):
    """A step within a guide section."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    guide_id: int = Field(foreign_key="guide.id", index=True)
    section_index: Optional[int] = None
    step_index: Optional[int] = None
    title: str
    details: Optional[str] = None
    text: Optional[str] = None
    tags: List[str] = Field(default_factory=list, sa_column=Column(JSON))
