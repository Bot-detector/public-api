from fastapi import APIRouter, Query, Depends
from src.app.player import Player
from src.core.fastapi.dependencies.to_jagex_name import to_jagex_name

router = APIRouter(tags=["Player"])

@router.get("/player/kc")
async def get_player_kc(user_name: str = Depends(to_jagex_name)):
    return {"name": user_name}