# Mathmagotchi 🧮✨

PS: Most of this README was written by Claude Code. <D-s>

Your friendly mathematical companion - a Tamagotchi-style desktop app that combines the charm of a virtual pet with mathematical enrichment!

## Features

- 🎭 **Mood System**: ASCII art character that changes expression based on time of day
- 📚 **Math Problems**: High-quality problems from Math StackExchange (analysis, real-analysis, etc.)
- 💭 **Inspirational Quotes**: Wisdom from legendary mathematicians
- ⏰ **Time-Based Behavior**: Different moods for morning, afternoon, evening, and night
- 🎨 **Clean GUI**: Simple, distraction-free PyQt6 interface

## Installation

This project uses `uv` for fast, reliable Python package management.

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager

Install uv if you don't have it:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup

1. **Clone or navigate to the project directory**:
```bash
cd mathmagotchi
```

2. **Create virtual environment and install dependencies**:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r pyproject.toml
```

3. **Install development dependencies (optional, for type checking)**:
```bash
uv pip install -e ".[dev]"
```

## Usage

### Running the Application

```bash
python main.py
```

Or with uv:
```bash
uv run python main.py
```

### Buttons

- **📜 New Quote**: Display a random mathematician quote
- **🧮 New Problem**: Fetch a new math problem from Math StackExchange

### Mood System

Your Mathmagotchi changes mood based on the time of day:

- **Morning (6-12)**: ☕ Energized - Ready for the day!
- **Afternoon (12-18)**: 🤔 Pondering - Deep thinking mode
- **Evening (18-22)**: 💭 Reflecting - Contemplative wisdom
- **Night (22-6)**: 😴 Sleepy - Time to rest

## Configuration

Edit `config.json` to customize settings:

```json
{
  "timezone": "UTC",
  "window_always_on_top": false,
  "api_key": "",
  "problem_difficulty": "medium",
  "preferred_tags": ["analysis", "real-analysis"],
  "window_width": 500,
  "window_height": 600
}
```

### Configuration Options

- **timezone**: Your timezone (e.g., "America/New_York", "Europe/London")
- **window_always_on_top**: Keep window above other windows
- **api_key**: Optional Stack Exchange API key for higher rate limits
- **preferred_tags**: Math topics to fetch problems from
- **window_width/height**: Window dimensions

## Development

### Type Checking

Run mypy for type checking:
```bash
uv run mypy character.py quotes.py config.py mathstack.py gui.py main.py
```

### Project Structure

```
mathmagotchi/
├── main.py              # Entry point
├── gui.py               # PyQt6 GUI
├── character.py         # ASCII art and mood system
├── mathstack.py         # Math StackExchange API client
├── quotes.py            # Quotes manager
├── config.py            # Configuration handler
├── config.json          # User settings (auto-generated)
├── data/
│   └── quotes.json      # Mathematician quotes (auto-generated)
├── pyproject.toml       # Project dependencies
└── requirements.txt     # Legacy requirements file
```

## Customization

### Adding More Quotes

Quotes are stored in `data/quotes.json`. The file is auto-generated on first run, but you can add more:

```json
[
  {
    "author": "Mathematician Name",
    "quote": "Inspiring quote here",
    "era": "Time period"
  }
]
```

### Changing ASCII Art

Edit `character.py` to modify or add new character moods. Each mood is a multi-line string in the `MOODS` dictionary.

## API Rate Limits

The Math StackExchange API has rate limits:
- **Without API key**: 300 requests per day
- **With API key**: 10,000 requests per day

To get an API key:
1. Register at [Stack Apps](https://stackapps.com/)
2. Create an application
3. Add the key to `config.json`

## Troubleshooting

**Problem: "Could not fetch problem"**
- Check your internet connection
- You may have hit the API rate limit (wait a few hours or add an API key)
- Try changing `preferred_tags` in config.json

**Problem: Window is too small/large**
- Resize the window and close the app - it will remember your preferred size
- Or edit `window_width` and `window_height` in config.json

**Problem: Character doesn't match time of day**
- Check the `timezone` setting in config.json
- Make sure your system time is correct
