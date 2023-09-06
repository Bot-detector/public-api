from fastapi import APIRouter
from . import player, prediction, report

router = APIRouter()
router.include_router(player.router)
