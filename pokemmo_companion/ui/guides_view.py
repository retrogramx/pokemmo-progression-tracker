"""Guides view widget for displaying and navigating PokeMMO guides."""

from __future__ import annotations

from typing import List, Tuple
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QPushButton,
    QCheckBox,
    QTextEdit,
    QComboBox,
)
from sqlmodel import Session, select

from pokemmo_companion.core.models import Guide, GuideStep


class GuidesView(QWidget):
    """Main guides view widget with region selection and step navigation."""

    def __init__(self, session_factory, parent=None):
        super().__init__(parent)
        self.session_factory = session_factory

        # UI Components
        self.region_combo = QComboBox()
        self.section_list = QListWidget()
        self.step_text = QTextEdit()
        self.step_text.setReadOnly(True)
        self.done_check = QCheckBox("Mark section step as done")
        self.skip_btn = QPushButton("Skip")
        self.top_most = QCheckBox("Always on top")

        # Layout setup
        left = QVBoxLayout()
        left.addWidget(QLabel("Region"))
        left.addWidget(self.region_combo)
        left.addWidget(QLabel("Sections"))
        left.addWidget(self.section_list)

        right = QVBoxLayout()
        right.addWidget(QLabel("Step"))
        right.addWidget(self.step_text)
        right.addWidget(self.done_check)
        right.addWidget(self.skip_btn)
        right.addStretch()
        right.addWidget(self.top_most)

        root = QHBoxLayout(self)
        root.addLayout(left, 1)
        root.addLayout(right, 2)

        # Connect signals
        self.region_combo.currentTextChanged.connect(self._on_region_changed)
        self.section_list.currentItemChanged.connect(self._on_section_changed)
        self.done_check.toggled.connect(self._on_done_toggled)
        self.skip_btn.clicked.connect(self._on_skip)
        self.top_most.toggled.connect(self._on_top_most)

        # Initialize
        self._load_regions()

    def _load_regions(self):
        """Load available regions into the combo box."""
        with self.session_factory() as s:
            regions = [g for g in s.exec(select(Guide)).all()]
        
        self.region_combo.clear()
        for g in sorted(regions, key=lambda x: x.key):
            self.region_combo.addItem(g.key)

    @Slot(str)
    def _on_region_changed(self, key: str):
        """Handle region selection change."""
        self.section_list.clear()
        if not key:
            return
            
        with self.session_factory() as s:
            guide = s.exec(select(Guide).where(Guide.key == key)).first()
            if not guide:
                return
            steps = s.exec(
                select(GuideStep).where(GuideStep.guide_id == guide.id)
            ).all()
        
        sections = self._group_by_section(steps)
        for idx, title in sections:
            item = QListWidgetItem(f"{idx:03d} — {title}")
            item.setData(Qt.UserRole, (key, idx))
            self.section_list.addItem(item)
        
        if self.section_list.count() > 0:
            self.section_list.setCurrentRow(0)

    def _group_by_section(self, steps: List[GuideStep]) -> List[Tuple[int, str]]:
        """Group steps by section and return unique section titles."""
        grouped = {}
        for step in steps:
            if step.section_index is not None and step.title:
                grouped.setdefault(step.section_index, step.title)
            elif step.title and "—" in step.title:
                try:
                    idx_str, title = step.title.split("—", 1)
                    grouped.setdefault(int(idx_str.strip()), title.strip())
                except Exception:
                    pass
        return sorted(grouped.items())

    def _on_section_changed(self, current: QListWidgetItem, _prev: QListWidgetItem):
        """Handle section selection change."""
        self.step_text.clear()
        if not current:
            return
            
        key, idx = current.data(Qt.UserRole)
        with self.session_factory() as s:
            guide = s.exec(select(Guide).where(Guide.key == key)).first()
            if not guide:
                return
            steps = s.exec(
                select(GuideStep).where(GuideStep.guide_id == guide.id)
            ).all()
        
        lines = []
        for step in sorted(
            steps, key=lambda x: (x.section_index or 9999, x.step_index or 9999)
        ):
            if (step.section_index == idx) or (
                step.title.startswith(f"{idx:03d} —")
            ):
                lines.append(step.text or step.details or "")
        
        self.step_text.setPlainText("\n".join(lines))

    def _on_done_toggled(self, _checked: bool):
        """Handle done checkbox toggle - stubbed for future implementation."""
        pass  # wire to per-user progress later

    def _on_skip(self):
        """Skip to next section."""
        row = self.section_list.currentRow()
        if row < self.section_list.count() - 1:
            self.section_list.setCurrentRow(row + 1)

    def _on_top_most(self, checked: bool):
        """Toggle always on top window flag."""
        flags = self.window().windowFlags()
        if checked:
            self.window().setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.window().setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.window().show()
