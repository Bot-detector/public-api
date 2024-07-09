from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PlayerCreate(BaseModel):
    name: str
    possible_ban: Optional[bool] = 0
    confirmed_ban: Optional[bool] = 0
    confirmed_player: Optional[bool] = 0
    label_id: Optional[int] = 0
    label_jagex: Optional[int] = 0
    ironman: Optional[bool] = None
    hardcore_ironman: Optional[bool] = None
    ultimate_ironman: Optional[bool] = None
    normalized_name: Optional[str] = None


class PlayerUpdate(BaseModel):
    name: Optional[str] = None
    possible_ban: Optional[bool] = None
    confirmed_ban: Optional[bool] = None
    confirmed_player: Optional[bool] = None
    label_id: Optional[int] = None
    label_jagex: Optional[int] = None
    ironman: Optional[bool] = None
    hardcore_ironman: Optional[bool] = None
    ultimate_ironman: Optional[bool] = None
    normalized_name: Optional[str] = None


class PlayerInDB(PlayerCreate):
    id: int
    created_at: datetime
    updated_at: datetime | None


class Player(PlayerInDB):
    pass
