from fastapi import APIRouter, HTTPException
from services.github.issue_suggestion_service import IssueSuggestionService
from config import GITHUB_TOKEN

router = APIRouter()

issue_service = IssueSuggestionService(GITHUB_TOKEN)


@router.get("/github/beginner-issues")
async def get_beginner_issues(
    language: str = "python",
    limit: int = 5
):
    """
    Fetch global beginner-friendly GitHub issues.
    """

    if not GITHUB_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="GitHub token not configured"
        )

    try:
        issues = await issue_service.fetch_beginner_issues(
            language=language,
            limit=limit
        )

        return {
            "language": language,
            "count": len(issues),
            "issues": issues
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch beginner issues"
        ) from e