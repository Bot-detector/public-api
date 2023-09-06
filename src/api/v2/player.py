from fastapi import APIRouter, Query
from src.app.player import Player

router = APIRouter(tags=["Player"])

@router.get("/player/kc")
async def get_player_kc(user_name:str = Query(max_length=13)):
    pass