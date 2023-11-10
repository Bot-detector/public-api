import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic.fields import Field

from src.app.models.player import Player
from src.app.views.response.report_kc import KCResponse
from src.core.fastapi.dependencies.session import get_session
from src.core.fastapi.dependencies.to_jagex_name import to_jagex_name

router = APIRouter(tags=["Player"])


@router.get("/player/report/score", response_model=list[KCResponse])
async def get_players_kc(
    name: list[Annotated[str, Field(..., min_length=1, max_length=13)]] = Query(
        ...,
        min_length=1,
        description="Name of the player",
        example=["Player1", "Player2"],
    ),
    session=Depends(get_session),
):
    """
    Get Kill Count (KC) data for multiple player names.

    Args:
        name (str): can be provided multiple times

    Returns:
        list[KCResponse]: A list of dictionaries containing KC data for each player.
    """
    player = Player(session)
    names = await asyncio.gather(*[to_jagex_name(n) for n in name])
    data = await player.get_kc(player_names=names)
    return data
