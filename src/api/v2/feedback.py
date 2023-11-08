import asyncio

# import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic.fields import Field

from src.app.models.feedback import Feedback
from src.app.views.input.feedback import FeedbackInput
from src.app.views.response.feedback import Feedback as FeedbackResponse
from src.app.views.response.feedback import FeedbackCount as FeedbackCountResponse
from src.app.views.response.ok import Ok
from src.core.fastapi.dependencies.session import get_session
from src.core.fastapi.dependencies.to_jagex_name import to_jagex_name

router = APIRouter(tags=["feedback"])

# logger = logging.getLogger(__name__)


@router.get("/players/feedback", response_model=list[FeedbackResponse])
async def get_feedback(
    name: list[Annotated[str, Field(..., min_length=1, max_length=13)]] = Query(
        ...,
        min_length=1,
        description="Name of the player",
        example=["Player1", "Player2"],
    ),
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
    feedback = Feedback(session)
    names = await asyncio.gather(*[to_jagex_name(n) for n in name])
    data = await feedback.get_feedback(player_names=names)

    return data


@router.get("/players/feedback/count", response_model=list[FeedbackCountResponse])
async def get_feedback_count(
    name: list[Annotated[str, Field(..., min_length=1, max_length=13)]] = Query(
        ...,
        min_length=1,
        description="Name of the player",
        example=["Player1", "Player2"],
    ),
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
    feedback = Feedback(session)
    names = await asyncio.gather(*[to_jagex_name(n) for n in name])
    data = await feedback.get_feedback_count(player_names=names)

    return data


# @router.post("/players/feedback", status_code=status.HTTP_201_CREATED, response_model=Ok)
# async def post_feedbacks(feedback: list[PredictionFeedbackIn]):
#     feedback_obj = Feedback(kafka_engine=feedback_engine)
#     data = await feedback_obj.parse_data(feedback)
#     if not data:
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="invalid data")
#     await feedback_obj.send_to_kafka(data)
#     return Ok()
