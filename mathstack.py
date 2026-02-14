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
        self.preferred_tags = preferred_tags or ["analysis", "real-analysis", "calculus",
                                                   "linear-algebra", "abstract-algebra",
                                                   "probability", "combinatorics"]
        self.recent_question_ids: List[int] = []
        self.max_recent = 50  # Track more recent questions
        self.cache: List[Dict] = []

    def fetch_problems(self, tag: str = None, min_score: int = 20, page_size: int = 50) -> List[Dict]:
        """
        Fetch high-quality math problems from StackExchange

        Args:
            tag: Tag to filter by (e.g., 'analysis')
            min_score: Minimum question score
            page_size: Number of results to fetch

        Returns:
            List of question dictionaries
        """
        all_problems = []

        # Fetch from multiple tags for more variety
        tags_to_fetch = random.sample(self.preferred_tags, min(3, len(self.preferred_tags)))

        for tag in tags_to_fetch:
            # Randomize between different sort methods for variety
            sort_methods = ["votes", "activity"]
            sort_method = random.choice(sort_methods)

            # For votes, use different pages to get variety
            page_number = random.randint(1, 10) if sort_method == "votes" else 1

            params = {
                "site": "math.stackexchange.com",
                "tagged": tag,
                "sort": sort_method,
                "order": "desc",
                "page": page_number,
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

                # Use lower minimum score threshold for more variety
                filtered = [q for q in questions if q.get("score", 0) >= min_score]
                all_problems.extend(filtered)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching from StackExchange: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

        # Remove duplicates based on question_id
        seen_ids = set()
        unique_problems = []
        for problem in all_problems:
            qid = problem.get("question_id")
            if qid and qid not in seen_ids:
                seen_ids.add(qid)
                unique_problems.append(problem)

        return unique_problems

    def get_random_problem(self, refresh_cache: bool = False) -> Optional[Dict]:
        """
        Get a random math problem, avoiding recent ones

        Args:
            refresh_cache: Force refresh the cache from API

        Returns:
            Formatted problem dictionary or None
        """
        # Refresh cache if needed or if we've seen most problems
        seen_ratio = len(self.recent_question_ids) / max(len(self.cache), 1)
        should_refresh = not self.cache or refresh_cache or seen_ratio > 0.7

        if should_refresh:
            print(f"Refreshing cache... (seen {len(self.recent_question_ids)}/{len(self.cache)} problems)")
            self.cache = self.fetch_problems()
            # Clear some recent IDs when refreshing to allow old favorites to reappear
            if len(self.recent_question_ids) > self.max_recent // 2:
                self.recent_question_ids = self.recent_question_ids[-self.max_recent // 2:]

        if not self.cache:
            return None

        # Filter out recently shown problems
        available_problems = [
            q for q in self.cache
            if q.get("question_id") not in self.recent_question_ids
        ]

        # If all problems have been shown, clear some old ones
        if not available_problems:
            print("All problems shown, clearing old history...")
            # Keep only the most recent 10
            self.recent_question_ids = self.recent_question_ids[-10:] if len(self.recent_question_ids) > 10 else []
            available_problems = [
                q for q in self.cache
                if q.get("question_id") not in self.recent_question_ids
            ]
            if not available_problems:
                available_problems = self.cache

        # Select random problem
        problem = random.choice(available_problems)
        question_id = problem.get("question_id")

        # Track this question
        if question_id:
            self.recent_question_ids.append(question_id)
            if len(self.recent_question_ids) > self.max_recent:
                self.recent_question_ids.pop(0)

        print(f"Cache: {len(self.cache)} problems, Recent: {len(self.recent_question_ids)}, Available: {len(available_problems)}")
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
        Clean and preserve HTML for MathJax rendering

        Args:
            html_text: HTML text from Stack Exchange

        Returns:
            Cleaned HTML suitable for display with MathJax
        """
        # Unescape HTML entities first
        text = unescape(html_text)

        # Remove potentially dangerous tags but keep formatting
        dangerous_tags = ['script', 'iframe', 'object', 'embed']
        for tag in dangerous_tags:
            text = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', text, flags=re.DOTALL | re.IGNORECASE)

        # Convert some common Stack Exchange elements
        text = re.sub(r'<pre><code>(.*?)</code></pre>', r'<pre>\1</pre>', text, flags=re.DOTALL)

        # Clean up excessive whitespace within tags
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
