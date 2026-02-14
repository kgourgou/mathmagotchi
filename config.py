"""
Configuration file handler
"""
import json
from pathlib import Path
from typing import Dict, Any


class Config:
    """Manages application configuration"""

    DEFAULT_CONFIG = {
        "timezone": "UTC",
        "window_always_on_top": False,
        "api_key": "",
        "problem_difficulty": "medium",
        "preferred_tags": ["analysis", "real-analysis"],
        "window_width": 450,
        "window_height": 500
    }

    def __init__(self, config_file: str = "config.json"):
        """
        Initialize configuration manager

        Args:
            config_file: Path to configuration JSON file
        """
        self.config_file = Path(config_file)
        self.config: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load configuration from file or create with defaults"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self.config = {**self.DEFAULT_CONFIG, **loaded_config}
            else:
                # Use defaults and save
                self.config = self.DEFAULT_CONFIG.copy()
                self.save()
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            self.config = self.DEFAULT_CONFIG.copy()

    def save(self) -> None:
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value and save

        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value
        self.save()

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return self.config.copy()
