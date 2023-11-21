import logging

from fastapi import APIRouter, Depends, HTTPException, status

from src.app.models.feedback import Feedback
from src.app.views.input.feedback import FeedbackInput
from src.app.views.response.ok import Ok
from src.core.fastapi.dependencies.session import get_session
from src.core.fastapi.dependencies.to_jagex_name import to_jagex_name

router = APIRouter(tags=["Feedback"])
logger = logging.getLogger(__name__)


@router.post("/feedback", response_model=Ok, status_code=status.HTTP_201_CREATED)
async def post_feedback(
    feedback: FeedbackInput,
    session=Depends(get_session),
):
    """ """
    _feedback = Feedback(session)

    feedback.player_name = await to_jagex_name(feedback.player_name)

    success, detail = await _feedback.insert_feedback(feedback=feedback)
    if not success:
        raise HTTPException(status_code=422, detail=detail)
    return Ok()
