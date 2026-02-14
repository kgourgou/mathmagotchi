"""
Mathematician quotes manager
"""
import json
import random
from pathlib import Path
from typing import List, Dict, Optional


class QuotesManager:
    """Manages mathematician quotes with random selection"""

    def __init__(self, quotes_file: str = "data/quotes.json"):
        """
        Initialize quotes manager

        Args:
            quotes_file: Path to quotes JSON file
        """
        self.quotes_file = Path(quotes_file)
        self.quotes: List[Dict[str, str]] = []
        self.recent_indices: List[int] = []
        self.max_recent = 10  # Track last 10 quotes to avoid repeats

        self.load_quotes()

    def load_quotes(self) -> None:
        """Load quotes from JSON file"""
        try:
            if self.quotes_file.exists():
                with open(self.quotes_file, 'r', encoding='utf-8') as f:
                    self.quotes = json.load(f)
            else:
                # Create default quotes if file doesn't exist
                self.quotes = self._get_default_quotes()
                self.save_quotes()
        except Exception as e:
            print(f"Error loading quotes: {e}")
            self.quotes = self._get_default_quotes()

    def save_quotes(self) -> None:
        """Save quotes to JSON file"""
        try:
            self.quotes_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.quotes_file, 'w', encoding='utf-8') as f:
                json.dump(self.quotes, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving quotes: {e}")

    def get_random_quote(self) -> Optional[Dict[str, str]]:
        """
        Get a random quote, avoiding recent selections

        Returns:
            Dictionary with 'author', 'quote', and optionally 'era'
        """
        if not self.quotes:
            return None

        # Get available indices (excluding recent ones)
        available_indices = [
            i for i in range(len(self.quotes))
            if i not in self.recent_indices
        ]

        # If all have been used recently, reset the tracking
        if not available_indices:
            self.recent_indices.clear()
            available_indices = list(range(len(self.quotes)))

        # Select random quote
        selected_index = random.choice(available_indices)
        self.recent_indices.append(selected_index)

        # Keep only the last N recent indices
        if len(self.recent_indices) > self.max_recent:
            self.recent_indices.pop(0)

        return self.quotes[selected_index]

    def format_quote(self, quote_dict: Dict[str, str]) -> str:
        """
        Format quote for display

        Args:
            quote_dict: Quote dictionary with author and quote

        Returns:
            Formatted string
        """
        quote = quote_dict.get('quote', '')
        author = quote_dict.get('author', 'Unknown')
        era = quote_dict.get('era', '')

        formatted = f'"{quote}"\n\n— {author}'
        if era:
            formatted += f' ({era})'

        return formatted

    def _get_default_quotes(self) -> List[Dict[str, str]]:
        """Get default mathematician quotes"""
        return [
            {
                "author": "Leonhard Euler",
                "quote": "Mathematicians have tried in vain to this day to discover some order in the sequence of prime numbers, and we have reason to believe that it is a mystery into which the human mind will never penetrate.",
                "era": "18th century"
            },
            {
                "author": "Carl Friedrich Gauss",
                "quote": "Mathematics is the queen of sciences and number theory is the queen of mathematics.",
                "era": "19th century"
            },
            {
                "author": "Srinivasa Ramanujan",
                "quote": "An equation means nothing to me unless it expresses a thought of God.",
                "era": "20th century"
            },
            {
                "author": "Paul Erdős",
                "quote": "A mathematician is a device for turning coffee into theorems.",
                "era": "20th century"
            },
            {
                "author": "Henri Poincaré",
                "quote": "Mathematics is the art of giving the same name to different things.",
                "era": "19th-20th century"
            },
            {
                "author": "Emmy Noether",
                "quote": "My methods are really methods of working and thinking; this is why they have crept in everywhere anonymously.",
                "era": "20th century"
            },
            {
                "author": "G.H. Hardy",
                "quote": "A mathematician, like a painter or poet, is a maker of patterns. If his patterns are more permanent than theirs, it is because they are made with ideas.",
                "era": "20th century"
            },
            {
                "author": "Bertrand Russell",
                "quote": "Mathematics, rightly viewed, possesses not only truth, but supreme beauty—a beauty cold and austere, like that of sculpture.",
                "era": "20th century"
            },
            {
                "author": "Sofia Kovalevskaya",
                "quote": "It is impossible to be a mathematician without being a poet in soul.",
                "era": "19th century"
            },
            {
                "author": "John von Neumann",
                "quote": "In mathematics you don't understand things. You just get used to them.",
                "era": "20th century"
            },
            {
                "author": "David Hilbert",
                "quote": "Mathematics is a game played according to certain simple rules with meaningless marks on paper.",
                "era": "19th-20th century"
            },
            {
                "author": "Blaise Pascal",
                "quote": "Mathematics is the science of patterns, and nature exploits just about every pattern that there is.",
                "era": "17th century"
            },
            {
                "author": "René Descartes",
                "quote": "Each problem that I solved became a rule which served afterwards to solve other problems.",
                "era": "17th century"
            },
            {
                "author": "Isaac Newton",
                "quote": "If I have seen further it is by standing on the shoulders of Giants.",
                "era": "17th-18th century"
            },
            {
                "author": "Pythagoras",
                "quote": "Number rules the universe.",
                "era": "Ancient Greece"
            },
            {
                "author": "Archimedes",
                "quote": "Give me a place to stand, and I shall move the earth.",
                "era": "Ancient Greece"
            },
            {
                "author": "Évariste Galois",
                "quote": "I have no time. I must hurry.",
                "era": "19th century"
            },
            {
                "author": "George Cantor",
                "quote": "The essence of mathematics lies in its freedom.",
                "era": "19th-20th century"
            },
            {
                "author": "Kurt Gödel",
                "quote": "I don't believe in natural science.",
                "era": "20th century"
            },
            {
                "author": "Alan Turing",
                "quote": "We can only see a short distance ahead, but we can see plenty there that needs to be done.",
                "era": "20th century"
            }
        ]
