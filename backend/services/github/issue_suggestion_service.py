import httpx
from typing import List, Dict

GITHUB_API_BASE = "https://api.github.com"


class IssueSuggestionService:
    def __init__(self, token: str):
        self.token = token

    async def fetch_beginner_issues(
        self,
        language: str = "python",
        limit: int = 5
    ) -> List[Dict]:
        """
        Fetch beginner-friendly (good first issue) GitHub issues globally
        filtered by programming language.
        """

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

        query = f'label:"good first issue" language:{language} state:open'

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{GITHUB_API_BASE}/search/issues",
                    headers=headers,
                    params={
                        "q": query,
                        "per_page": limit
                    }
                )

                if response.status_code != 200:
                    return []

                data = response.json()

            items = data.get("items", [])

            return [
                {
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "url": issue.get("html_url"),
                    "repo": issue.get("repository_url", "").split("/")[-1]
                }
                for issue in items
            ]

        except Exception:
            # Fail gracefully — do not crash API
            return []