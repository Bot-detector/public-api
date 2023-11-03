from fastapi import APIRouter, Depends, HTTPException, status
from src.app.models.player import Player
from src.app.views.input.feedback import FeedbackIn, FeedbackOut
from src.core.fastapi.dependencies.session import get_session
from src.core.fastapi.dependencies.to_jagex_name import to_jagex_name

router = APIRouter(tags=["feedback"])


@router.post("/feedback", response_model=FeedbackOut)
async def post_feedback(
    feedback: FeedbackIn,
    session=Depends(get_session),
):
    """
    Post feedback data for a user.

    Args:
        feedback (FeedbackIn): The feedback data to post.

    Returns:
        FeedbackOut: An object containing the posted feedback data.

    Raises:
        HTTPException: Returns a 404 error with the message "Player not found" if no data is found for the user.

    """
    player = Player(session=session)
    data = await player.post_feedback(feedback=feedback)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )
    return data
