"""
ASCII art character system with mood-based expressions
"""
from datetime import datetime
from typing import Dict


class Character:
    """Manages the ASCII art character and its moods"""

    MOODS = {
        "energetic": """☕ TIME FOR MATH! ☕

    /\\_/\\
   ( ^.^ )
    > ^ <
   /|   |\\

 Let's learn!""",

        "thinking": """🤔 Hmm, interesting...

    /\\_/\\
   ( o.o )
    > ~ <
   /     \\

 Deep thoughts...""",

        "contemplative": """💭 Words of wisdom

    /\\_/\\
   ( -.-)
    > v <
   /     \\

 So wise~""",

        "sleepy": """😴 Sleepy time...

    /\\_/\\
   ( u.u )
    > - <
   /     \\

 *yawns* zzz""",

        "excited": """✨ NEW PROBLEM! ✨

    /\\_/\\
   ( *.* )
    > O <
   /|   |\\

 So exciting!!"""
    }

    def __init__(self):
        """Initialize the character"""
        self.current_mood = "thinking"

    def get_mood_for_time(self, hour: int) -> str:
        """
        Determine mood based on hour of day

        Args:
            hour: Hour in 24-hour format (0-23)

        Returns:
            Mood name as string
        """
        if 6 <= hour < 12:
            return "energetic"
        elif 12 <= hour < 18:
            return "thinking"
        elif 18 <= hour < 22:
            return "contemplative"
        else:  # 22-6
            return "sleepy"

    def get_current_mood(self) -> str:
        """Get mood based on current time"""
        current_hour = datetime.now().hour
        return self.get_mood_for_time(current_hour)

    def get_ascii_art(self, mood: str = None) -> str:
        """
        Get ASCII art for specified mood

        Args:
            mood: Mood name (or None to use current time-based mood)

        Returns:
            ASCII art string
        """
        if mood is None:
            mood = self.get_current_mood()

        self.current_mood = mood
        return self.MOODS.get(mood, self.MOODS["thinking"])

    def set_excited(self) -> str:
        """Set character to excited mood (for new problems)"""
        return self.get_ascii_art("excited")
