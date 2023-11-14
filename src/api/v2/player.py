import asyncio
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic.fields import Field

from src.app.models.player import Player
from src.app.views.input.feedback import FeedbackInput
from src.app.views.response.feedback_score import FeedbackScoreResponse
from src.app.views.response.ok import Ok
from src.app.views.response.prediction import PredictionResponse
from src.app.views.response.report_score import ReportScoreResponse
from src.core.fastapi.dependencies.session import get_session
from src.core.fastapi.dependencies.to_jagex_name import to_jagex_name

router = APIRouter(tags=["Player"])
logger = logging.getLogger(__name__)


@router.get("/player/report/score", response_model=list[ReportScoreResponse])
async def get_players_kc(
    name: list[Annotated[str, Field(..., min_length=1, max_length=13)]] = Query(
        ...,
        min_length=1,
        max_length=5,
        description="Name of the player",
        example=["Player1", "Player2"],
    ),
    session=Depends(get_session),
):
    """
    Get the report score for one or multiple players.

    Args:
        name (str): can be provided multiple times

    Returns:
        list[ReportScoreResponse]: A list of dictionaries containing KC data for each player.
    """
    player = Player(session)
    names = await asyncio.gather(*[to_jagex_name(n) for n in name])
    data = await player.get_report_score(player_names=names)
    return data


@router.get("/player/feedback/score", response_model=list[FeedbackScoreResponse])
async def get_feedback_score(
    name: list[Annotated[str, Field(..., min_length=1, max_length=13)]] = Query(
        ...,
        min_length=1,
        max_length=5,
        description="Name of the player",
        example=["Player1", "Player2"],
    ),
    session=Depends(get_session),
):
    """
    Get the feedback score for one or multiple players.

    Args:
        name (str): can be provided multiple times

    Returns:
        list[FeedbackScoreResponse]: A list of dictionaries containing KC data for each player.
    """
    player = Player(session)
    names = await asyncio.gather(*[to_jagex_name(n) for n in name])
    data = await player.get_feedback_score(player_names=names)
    return data


@router.get("/player/prediction", response_model=list[PredictionResponse])
async def get_prediction(
    name: list[Annotated[str, Field(..., min_length=1, max_length=13)]] = Query(
        ...,
        min_length=1,
        max_length=5,
        description="Name of the player",
        example=["Player1", "Player2"],
    ),
    breakdown: bool = Query(...),
    session=Depends(get_session),
):
    """
    Get prediction data for one or multiple users.

    Args:
        name (str): The username of the user for whom predictions are requested.
        breakdown (bool): A flag indicating whether to include a breakdown of predictions.

    Returns:
        List[PredictionResponse]: A list of PredictionResponse objects containing prediction data.

    Raises:
        HTTPException: Returns a 404 error with the message "Player not found" if no data is found for the user.

    """
    player = Player(session)
    names = await asyncio.gather(*[to_jagex_name(n) for n in name])
    data = await player.get_prediction(player_names=names)
    logger.info(data)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )
    return [PredictionResponse.from_data(d, breakdown) for d in data]


@router.get("/player/feedback", response_model=Ok, status_code=status.HTTP_201_CREATED)
async def get_feedback(
    feedback: FeedbackInput,
    session=Depends(get_session),
):
    """
    Submit feedback for a player.

    Args:
        feedback (FeedbackInput): A FeedbackInput object containing the feedback data.

    Returns:
        Ok: An Ok object containing the message "Feedback submitted successfully".

    Raises:
        HTTPException: Returns a 400 error with the message "Invalid feedback" if the feedback is invalid.

    """
    player = Player(session)
    data = await player.parse_feedback(feedback)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid feedback"
        )
    await player.post_feedback(feedback)
    return Ok()
