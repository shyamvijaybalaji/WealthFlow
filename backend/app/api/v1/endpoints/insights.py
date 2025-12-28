"""AI Insights API endpoints."""
from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.services.ai_insights import AIInsightsService

router = APIRouter()


@router.get("/", response_model=List[dict])
def get_financial_insights(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get AI-powered financial insights for the current user.

    Returns:
        List of insight objects with type, title, message, and icon.
    """
    # Analyze user's spending patterns
    financial_data = AIInsightsService.analyze_spending_patterns(
        db=db,
        user_id=current_user.id
    )

    # Generate insights based on the analysis
    insights = AIInsightsService.generate_insights(financial_data)

    return insights
