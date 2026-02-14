"""
PyQt6 GUI for Mathmagotchi
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QStatusBar, QFrame
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtGui import QFont, QIcon
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

        # Set cute tamagotchi icon
        import os
        icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Set window size from config (smaller default)
        width = self.config.get("window_width", 450)
        height = self.config.get("window_height", 500)
        self.resize(width, height)

        # Set always on top if configured
        if self.config.get("window_always_on_top", False):
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Create central widget and layout
        central_widget = QWidget()
        # Tamagotchi-style gradient background (soft pastels)
        central_widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #FFB6D9, stop:0.5 #D5AAFF, stop:1 #85E3FF);
            border-radius: 20px;
        """)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(8)
        layout.setContentsMargins(20, 20, 20, 20)

        # Combined content frame (text + character in one box)
        # Tamagotchi-style screen with thick rounded border
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: #E8F5E9;
                border: 6px solid #4A148C;
                border-radius: 20px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
        """)
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(5, 5, 5, 5)

        # Web view for rendering math with MathJax
        self.content_view = QWebEngineView()
        self.content_view.setStyleSheet("""
            QWebEngineView {
                background-color: #FFF9C4;
                border: 3px solid #7B1FA2;
                border-radius: 12px;
            }
        """)
        content_layout.addWidget(self.content_view, stretch=1)

        # Character display (inside the same box, below the text)
        self.character_label = QLabel()
        self.character_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.character_label.setFont(QFont("Courier New", 12))
        self.character_label.setWordWrap(False)  # Critical: prevent wrapping
        self.character_label.setStyleSheet("""
            QLabel {
                background-color: #C8E6C9;
                color: #1B5E20;
                padding: 15px;
                border-top: 3px solid #7B1FA2;
                border-bottom-left-radius: 12px;
                border-bottom-right-radius: 12px;
                white-space: pre;
            }
        """)
        self.character_label.setMinimumHeight(160)
        self.character_label.setMaximumHeight(180)
        content_layout.addWidget(self.character_label)

        layout.addWidget(content_frame, stretch=1)

        # Button row - Tamagotchi style cute buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.quote_button = QPushButton("📜 Quote")
        self.quote_button.clicked.connect(self.show_random_quote)
        self.quote_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFD54F, stop:1 #FFA726);
                color: #4A148C;
                border: 4px solid #6A1B9A;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 20px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFE082, stop:1 #FFB74D);
                border: 4px solid #8E24AA;
            }
            QPushButton:pressed {
                background: #FF9800;
                padding-top: 14px;
                padding-bottom: 10px;
            }
        """)
        button_layout.addWidget(self.quote_button)

        self.problem_button = QPushButton("🧮 Problem")
        self.problem_button.clicked.connect(self.show_random_problem)
        self.problem_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #81D4FA, stop:1 #4FC3F7);
                color: #01579B;
                border: 4px solid #0277BD;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 20px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #B3E5FC, stop:1 #81D4FA);
                border: 4px solid #0288D1;
            }
            QPushButton:pressed {
                background: #29B6F6;
                padding-top: 14px;
                padding-bottom: 10px;
            }
        """)
        button_layout.addWidget(self.problem_button)

        layout.addLayout(button_layout)

        # Status bar - cute tamagotchi style
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: rgba(255, 255, 255, 0.3);
                color: #4A148C;
                font-size: 11px;
                font-weight: bold;
                border-radius: 8px;
                padding: 4px;
            }
        """)
        self.setStatusBar(self.status_bar)

        # Update character display
        self.update_character()

    def render_html_content(self, content: str) -> None:
        """
        Render content as HTML with MathJax support

        Args:
            content: Text content (can include LaTeX math)
        """
        # Convert plain text to HTML, preserving line breaks
        html_content = content.replace('\n', '<br>')

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
            <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
            <script>
                MathJax = {{
                    tex: {{
                        inlineMath: [['$', '$'], ['\\(', '\\)']],
                        displayMath: [['$$', '$$'], ['\\[', '\\]']]
                    }}
                }};
            </script>
            <style>
                body {{
                    font-family: 'Comic Sans MS', 'Arial Rounded MT Bold', Arial, sans-serif;
                    font-size: 14px;
                    color: #4A148C;
                    background-color: #FFF9C4;
                    padding: 15px;
                    margin: 0;
                    line-height: 1.6;
                }}
                .quote {{
                    font-style: italic;
                    font-size: 16px;
                    line-height: 1.8;
                    color: #6A1B9A;
                }}
                .author {{
                    font-weight: bold;
                    margin-top: 15px;
                    color: #7B1FA2;
                }}
                .problem-title {{
                    font-size: 16px;
                    font-weight: bold;
                    color: #0277BD;
                    margin-bottom: 10px;
                }}
                .tags {{
                    color: #6A1B9A;
                    font-size: 12px;
                }}
                .link {{
                    color: #0277BD;
                    text-decoration: none;
                    font-weight: bold;
                }}
                .link:hover {{
                    text-decoration: underline;
                    color: #01579B;
                }}
                h2 {{
                    color: #6A1B9A;
                }}
                strong {{
                    color: #7B1FA2;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        self.content_view.setHtml(html)

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
<h2>Welcome to Mathmagotchi! 🧮✨</h2>

<p>Your friendly mathematical companion is here to brighten your day with:</p>

<p>📚 Challenging math problems from Math StackExchange<br>
💭 Inspirational quotes from legendary mathematicians<br>
🕐 A mood that changes with the time of day</p>

<p><strong>Click a button below to get started!</strong></p>

<p style="margin-top: 20px; color: #666; font-size: 12px;">
Math is rendered beautifully with LaTeX support!<br>
Try clicking "🧮 Problem" to see formulas like $\\int_0^\\infty e^{-x^2}dx = \\frac{\\sqrt{\\pi}}{2}$
</p>
        """.strip()

        self.render_html_content(welcome_text)

    def show_random_quote(self):
        """Display a random mathematician quote"""
        quote_dict = self.quotes_manager.get_random_quote()

        if quote_dict:
            quote = quote_dict.get('quote', '')
            author = quote_dict.get('author', 'Unknown')
            era = quote_dict.get('era', '')

            html_content = f"""
            <div class="quote">"{quote}"</div>
            <div class="author">— {author}"""

            if era:
                html_content += f" ({era})"

            html_content += "</div>"

            self.render_html_content(html_content)

            # Set contemplative mood
            ascii_art = self.character.get_ascii_art("contemplative")
            self.character_label.setText(ascii_art)
        else:
            self.render_html_content("No quotes available. 😢")

    def show_random_problem(self):
        """Display a random math problem"""
        # Set excited mood
        ascii_art = self.character.set_excited()
        self.character_label.setText(ascii_art)

        # Show loading message
        self.render_html_content("Loading problem from Math StackExchange... ⏳")

        # Disable button while loading
        self.problem_button.setEnabled(False)

        # Fetch and display problem
        try:
            problem = self.math_client.get_random_problem()

            if problem:
                # Format as HTML with proper styling
                html_content = f"""
                <div class="problem-title">📚 {problem['title']}</div>
                <div style="margin: 15px 0;">{problem['body']}</div>
                <div class="tags">Tags: {', '.join(problem['tags'])}</div>
                <div style="margin-top: 10px;">Score: ⭐ {problem['score']}</div>
                <div style="margin-top: 10px;">
                    <a href="{problem['link']}" class="link">🔗 View on Math StackExchange</a>
                </div>
                """
                self.render_html_content(html_content)
            else:
                self.render_html_content(
                    "<p>Could not fetch problem. 😢</p>"
                    "<p>This might be due to:</p>"
                    "<ul>"
                    "<li>No internet connection</li>"
                    "<li>API rate limiting</li>"
                    "<li>No problems matching criteria</li>"
                    "</ul>"
                    "<p>Try again in a moment!</p>"
                )
        except Exception as e:
            self.render_html_content(f"<p>Error loading problem: {e}</p>")
        finally:
            # Re-enable button
            self.problem_button.setEnabled(True)

    def closeEvent(self, event):
        """Handle window close event"""
        # Save window size
        self.config.set("window_width", self.width())
        self.config.set("window_height", self.height())
        event.accept()
