from pydantic import BaseModel


class KCResponse(BaseModel):
    count: int
    possible_ban: bool
    confirmed_ban: bool
    confirmed_player: bool
    manual_detect: bool
