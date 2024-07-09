import asyncio
import logging

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from src.app.repositories.player import Player
from src.app.repositories.report import Report
from src.app.views.input.report import Detection, ParsedDetection
from src.app.views.response.ok import Ok
from src.core._cache import SimpleALRUCache
from src.core.fastapi.dependencies.session import get_session

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Report"])

player_cache = SimpleALRUCache(max_size=10_000)


@router.post("/report", status_code=status.HTTP_201_CREATED, response_model=Ok)
async def post_reports(detections: list[Detection], session=Depends(get_session)):
    report_repo = Report()
    player_repo = Player(session=session, cache=player_cache)

    data = await report_repo.parse_data(detections)
    if not data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="invalid data")
    logger.debug(f"Working: {len(data)}")

    # get unique list of names
    player_names = list(set([d.reported for d in data] + [d.reporter for d in data]))
    players = await asyncio.gather(
        *[player_repo.get_or_insert(player_name=p) for p in player_names]
    )
    players = {p.name: p.id for p in players}

    _data = []
    for d in data:
        _d = d.model_dump()
        _d["reported_id"] = players.get(_d.pop("reported"))
        _d["reporter_id"] = players.get(_d.pop("reporter"))
        _data.append(ParsedDetection(**_d))
    await report_repo.send_to_kafka(data=_data)
    return Ok()
