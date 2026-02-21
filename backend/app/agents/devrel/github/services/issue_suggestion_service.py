import httpx
from typing import List, Dict

GITHUB_API_BASE = "https://api.github.com"


class IssueSuggestionService:

    def __init__(self, token: str):
        self.token = token

    async def fetch_global_beginner_issues(
        self,
        user_query: str,
        limit: int = 5
    ) -> List[Dict]:

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json"
        }

        # Base GitHub search query
        search_query = 'label:"good first issue" is:issue state:open'

        query_lower = user_query.lower()

        # Language filter
        if "python" in query_lower:
            search_query += " language:python"

        # Org filter
        if "django" in query_lower:
            search_query += " org:django"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{GITHUB_API_BASE}/search/issues",
                    headers=headers,
                    params={
                        "q": search_query,
                        "per_page": limit
                    }
                )

                if response.status_code != 200:
                    return []

                data = response.json()

            return [
                {
                    "repo": item.get("repository_url", "").split("/")[-1],
                    "number": item.get("number"),
                    "title": item.get("title"),
                    "url": item.get("html_url")
                }
                for item in data.get("items", [])
            ]

        except Exception:
            # Fail gracefully
            return []