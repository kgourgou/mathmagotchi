"""
Math StackExchange API client
"""
import requests
import random
from typing import List, Dict, Optional
from html import unescape
import re


class MathStackClient:
    """Client for fetching math problems from Math StackExchange"""

    BASE_URL = "https://api.stackexchange.com/2.3"

    def __init__(self, api_key: str = "", preferred_tags: List[str] = None):
        """
        Initialize Math StackExchange client

        Args:
            api_key: Optional API key for higher rate limits
            preferred_tags: List of preferred tags for problems
        """
        self.api_key = api_key
        self.preferred_tags = preferred_tags or ["analysis", "real-analysis"]
        self.recent_question_ids: List[int] = []
        self.max_recent = 20  # Track recent questions to avoid repeats
        self.cache: List[Dict] = []

    def fetch_problems(self, tag: str = None, min_score: int = 50, page_size: int = 30) -> List[Dict]:
        """
        Fetch high-quality math problems from StackExchange

        Args:
            tag: Tag to filter by (e.g., 'analysis')
            min_score: Minimum question score
            page_size: Number of results to fetch

        Returns:
            List of question dictionaries
        """
        if tag is None:
            tag = random.choice(self.preferred_tags)

        params = {
            "site": "math.stackexchange.com",
            "tagged": tag,
            "sort": "votes",
            "order": "desc",
            "pagesize": page_size,
            "filter": "withbody"  # Include question body
        }

        if self.api_key:
            params["key"] = self.api_key

        try:
            response = requests.get(
                f"{self.BASE_URL}/search/advanced",
                params=params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()
            questions = data.get("items", [])

            # Filter by minimum score
            filtered = [q for q in questions if q.get("score", 0) >= min_score]

            return filtered

        except requests.exceptions.RequestException as e:
            print(f"Error fetching from StackExchange: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def get_random_problem(self, refresh_cache: bool = False) -> Optional[Dict]:
        """
        Get a random math problem, avoiding recent ones

        Args:
            refresh_cache: Force refresh the cache from API

        Returns:
            Formatted problem dictionary or None
        """
        # Refresh cache if needed
        if not self.cache or refresh_cache:
            self.cache = self.fetch_problems()

        if not self.cache:
            return None

        # Filter out recently shown problems
        available_problems = [
            q for q in self.cache
            if q.get("question_id") not in self.recent_question_ids
        ]

        # If all problems have been shown, reset recent tracking
        if not available_problems:
            self.recent_question_ids.clear()
            available_problems = self.cache

        # Select random problem
        problem = random.choice(available_problems)
        question_id = problem.get("question_id")

        # Track this question
        if question_id:
            self.recent_question_ids.append(question_id)
            if len(self.recent_question_ids) > self.max_recent:
                self.recent_question_ids.pop(0)

        return self.format_problem(problem)

    def format_problem(self, problem: Dict) -> Dict:
        """
        Format a problem for display

        Args:
            problem: Raw problem dictionary from API

        Returns:
            Formatted problem with title, body, link, tags
        """
        title = unescape(problem.get("title", "Untitled"))
        body = self.clean_html(problem.get("body", ""))
        link = problem.get("link", "")
        tags = problem.get("tags", [])
        score = problem.get("score", 0)

        # Truncate body if too long
        max_body_length = 800
        if len(body) > max_body_length:
            body = body[:max_body_length] + "..."

        return {
            "title": title,
            "body": body,
            "link": link,
            "tags": tags,
            "score": score
        }

    @staticmethod
    def clean_html(html_text: str) -> str:
        """
        Clean HTML tags and entities from text

        Args:
            html_text: HTML text

        Returns:
            Plain text
        """
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_text)

        # Unescape HTML entities
        text = unescape(text)

        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()

        return text

    def format_problem_display(self, problem: Dict) -> str:
        """
        Format problem for GUI display

        Args:
            problem: Formatted problem dictionary

        Returns:
            Display string
        """
        display = f"📚 {problem['title']}\n\n"
        display += f"{problem['body']}\n\n"
        display += f"Tags: {', '.join(problem['tags'])}\n"
        display += f"Score: ⭐ {problem['score']}\n\n"
        display += f"🔗 {problem['link']}"

        return display
