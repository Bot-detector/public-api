from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.app.models.feedback import Feedback
from src.app.views.input.feedback import FeedbackIn
from src.app.views.response.feedback import FeedbackResponse
from src.core.database import get_db
from src.core.fastapi.dependencies.to_jagex_name import to_jagex_name

router = APIRouter(tags=["feedback"])


@router.get("/feedback/score", response_model=list[FeedbackResponse])
async def get_feedback_score(
    names: list[str] = Query(..., max_length=13),  # Update the query parameter
    db: Session = Depends(get_db),  # Use the SQLAlchemy session dependency
):
    """
    Get feedback scores for one or more players.

    Args:
        names (list[str]): List of player names to retrieve feedback scores for.

    Returns:
        list[FeedbackResponse]: List of feedback scores for the specified players.
    """
    feedback = Feedback(db)

    # Use the to_jagex_name function to get normalized names
    normalized_names = await asyncio.gather(*[to_jagex_name(name) for name in names])

    # Get feedback scores for the normalized names
    feedback_scores = feedback.get_feedback(player_names=normalized_names)

    # Convert the feedback scores to a list of FeedbackResponse objects
    feedback_response_list = [
        FeedbackResponse(
            id=score.id,
            ts=str(score.ts),  # Convert the timestamp to a string
            voter_id=score.voter_id,
            subject_id=score.subject_id,
            prediction=score.prediction,
            confidence=score.confidence,
            vote=score.vote,
            feedback_text=score.feedback_text,
            reviewed=score.reviewed,
            reviewer_id=score.reviewer_id,
            user_notified=score.user_notified,
            proposed_label=score.proposed_label,
        )
        for score in feedback_scores
    ]

    return feedback_response_list
