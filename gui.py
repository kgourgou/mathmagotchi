"""
PyQt6 GUI for Mathmagotchi
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QStatusBar, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from datetime import datetime

from character import Character
from quotes import QuotesManager
from mathstack import MathStackClient
from config import Config


class MathmagotchiWindow(QMainWindow):
    """Main application window"""

    def __init__(self, config: Config):
        """
        Initialize main window

        Args:
            config: Configuration object
        """
        super().__init__()

        self.config = config
        self.character = Character()
        self.quotes_manager = QuotesManager()
        self.math_client = MathStackClient(
            api_key=config.get("api_key", ""),
            preferred_tags=config.get("preferred_tags", ["analysis"])
        )

        self.init_ui()
        self.setup_timer()
        self.show_welcome()

    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Mathmagotchi 🧮")

        # Set window size from config (smaller default)
        width = self.config.get("window_width", 450)
        height = self.config.get("window_height", 500)
        self.resize(width, height)

        # Set always on top if configured
        if self.config.get("window_always_on_top", False):
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Create central widget and layout
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #e8e8e8;")
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(5)
        layout.setContentsMargins(10, 10, 10, 10)

        # Combined content frame (text + character in one box)
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Text content area
        self.content_text = QTextEdit()
        self.content_text.setReadOnly(True)
        self.content_text.setFont(QFont("Arial", 10))
        self.content_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: #333;
                padding: 15px;
                border: none;
            }
        """)
        content_layout.addWidget(self.content_text, stretch=1)

        # Character display (inside the same box, below the text)
        self.character_label = QLabel()
        self.character_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.character_label.setFont(QFont("Courier", 11))
        self.character_label.setStyleSheet("""
            QLabel {
                background-color: #f5f5f5;
                color: #333;
                padding: 10px;
                border-top: 2px solid #e0e0e0;
            }
        """)
        self.character_label.setMinimumHeight(140)
        content_layout.addWidget(self.character_label)

        layout.addWidget(content_frame, stretch=1)

        # Button row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)

        self.quote_button = QPushButton("📜 Quote")
        self.quote_button.clicked.connect(self.show_random_quote)
        self.quote_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(self.quote_button)

        self.problem_button = QPushButton("🧮 Problem")
        self.problem_button.clicked.connect(self.show_random_problem)
        self.problem_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        button_layout.addWidget(self.problem_button)

        layout.addLayout(button_layout)

        # Status bar
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("font-size: 10px;")
        self.setStatusBar(self.status_bar)

        # Update character display
        self.update_character()

    def setup_timer(self):
        """Setup timer to update character mood based on time"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_character)
        # Update every 5 minutes
        self.timer.start(5 * 60 * 1000)

    def update_character(self):
        """Update character display based on current mood"""
        current_mood = self.character.get_current_mood()
        ascii_art = self.character.get_ascii_art(current_mood)
        self.character_label.setText(ascii_art)

        # Update status bar
        current_time = datetime.now().strftime("%H:%M")
        self.status_bar.showMessage(f"Time: {current_time} | Mood: {current_mood.title()}")

    def show_welcome(self):
        """Show welcome message"""
        welcome_text = """
Welcome to Mathmagotchi! 🧮✨

Your friendly mathematical companion is here to brighten your day with:

📚 Challenging math problems from Math StackExchange
💭 Inspirational quotes from legendary mathematicians
🕐 A mood that changes with the time of day

Click a button below to get started!
        """.strip()

        self.content_text.setPlainText(welcome_text)

    def show_random_quote(self):
        """Display a random mathematician quote"""
        quote_dict = self.quotes_manager.get_random_quote()

        if quote_dict:
            formatted_quote = self.quotes_manager.format_quote(quote_dict)
            self.content_text.setPlainText(formatted_quote)

            # Set contemplative mood
            ascii_art = self.character.get_ascii_art("contemplative")
            self.character_label.setText(ascii_art)
        else:
            self.content_text.setPlainText("No quotes available. 😢")

    def show_random_problem(self):
        """Display a random math problem"""
        # Set excited mood
        ascii_art = self.character.set_excited()
        self.character_label.setText(ascii_art)

        # Show loading message
        self.content_text.setPlainText("Loading problem from Math StackExchange... ⏳")
        self.content_text.repaint()  # Force update

        # Disable button while loading
        self.problem_button.setEnabled(False)

        # Fetch and display problem
        try:
            problem = self.math_client.get_random_problem()

            if problem:
                display_text = self.math_client.format_problem_display(problem)
                self.content_text.setPlainText(display_text)
            else:
                self.content_text.setPlainText(
                    "Could not fetch problem. 😢\n\n"
                    "This might be due to:\n"
                    "- No internet connection\n"
                    "- API rate limiting\n"
                    "- No problems matching criteria\n\n"
                    "Try again in a moment!"
                )
        except Exception as e:
            self.content_text.setPlainText(f"Error loading problem: {e}")
        finally:
            # Re-enable button
            self.problem_button.setEnabled(True)

    def closeEvent(self, event):
        """Handle window close event"""
        # Save window size
        self.config.set("window_width", self.width())
        self.config.set("window_height", self.height())
        event.accept()
