"""Main window for the PokeMMO Companion App."""

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QToolBar
from PySide6.QtGui import QAction
from sqlmodel import Session

from pokemmo_companion.ui.guides_view import GuidesView


class MainWindow(QMainWindow):
    """Main application window with navigation and content areas."""

    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setWindowTitle("PokeMMO Companion")

        # Central widget setup
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create views
        self.guides_view = GuidesView(lambda: Session(self.engine))
        self.stack.addWidget(self.guides_view)

        # Toolbar setup
        tb = QToolBar("Navigation")
        self.addToolBar(tb)

        act_guides = QAction("Guides", self)
        act_guides.triggered.connect(
            lambda: self.stack.setCurrentWidget(self.guides_view)
        )
        tb.addAction(act_guides)
