import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.app.models.player import Player
from src.app.views.response.report_kc import KCResponse
from src.core.fastapi.dependencies.session import get_session
from src.core.fastapi.dependencies.to_jagex_name import to_jagex_name

router = APIRouter(tags=["Player"])


@router.get("/players/score", response_model=list[KCResponse])
async def get_players_kc(
    name: Annotated[list[str], Query(...)], session=Depends(get_session)
):
    player = Player(session)
    names = await asyncio.gather(*[to_jagex_name(n) for n in name])
    data = await player.get_kc(player_names=names)
    return data
