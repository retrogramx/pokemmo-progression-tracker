"""Main application entry point for PokeMMO Companion App."""

import sys
from PySide6.QtWidgets import QApplication

from pokemmo_companion.core.db import init_db
from pokemmo_companion.ui.main_window import MainWindow


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Initialize database
    engine = init_db()
    
    # Create and show main window
    window = MainWindow(engine)
    window.resize(1000, 600)
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
