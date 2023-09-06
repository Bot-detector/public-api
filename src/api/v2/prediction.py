from fastapi import APIRouter, Query, Depends
from src.app.prediction import Prediction
from src.core.fastapi.dependencies.to_jagex_name import to_jagex_name
router = APIRouter(tags=["Prediction"])


@router.get("/prediction")
async def get_prediction(user_name: str = Depends(to_jagex_name)):
    pass
