# import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.app.models.prediction import Prediction
from src.app.views.response.prediction import PredictionResponse
from src.core.fastapi.dependencies.session import get_session
from src.core.fastapi.dependencies.to_jagex_name import to_jagex_name

router = APIRouter(tags=["Prediction"])
# logger = logging.getLogger(__name__)


@router.get("/prediction", response_model=list[PredictionResponse])
async def get_prediction(
    user_name: str = Depends(to_jagex_name),
    breakdown: bool = Query(...),
    session=Depends(get_session),
):
    """
    Retrieve prediction data for a user by their username.

    Args:
        user_name (str): The username of the user for whom predictions are requested.
        breakdown (bool): A flag indicating whether to include a breakdown of predictions.

    Returns:
        List[PredictionResponse]: A list of PredictionResponse objects containing prediction data.

    Raises:
        HTTPException: Returns a 404 error with the message "Player not found" if no data is found for the user.

    """
    prediction = Prediction(session=session)
    data = await prediction.get_prediction(user_name=user_name)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )  # raise error before trying to iterate
    # logger.debug(f"Retrieved prediction data {data} for {user_name} ")
    data = [PredictionResponse.from_data(d, breakdown) for d in data]
    return data
