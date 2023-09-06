from fastapi import APIRouter, Query
from src.app.prediction import Prediction

router = APIRouter(tags=["Prediction"])

@router.get("/prediction")
async def get_prediction(user_name:str = Query(max_length=13)):
    pass