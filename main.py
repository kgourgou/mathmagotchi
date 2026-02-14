"""
Mathmagotchi - Your friendly mathematical companion

Entry point for the application
"""
import sys
from PyQt6.QtWidgets import QApplication

from gui import MathmagotchiWindow
from config import Config


def main():
    """Main entry point"""
    # Load configuration
    config = Config()

    # Create Qt application
    app = QApplication(sys.argv)

    # Create and show main window
    window = MathmagotchiWindow(config)
    window.show()

    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
