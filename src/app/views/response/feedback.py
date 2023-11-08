from typing import Optional

from pydantic import BaseModel


class Feedback(BaseModel):
    player_name: str
    vote: int
    prediction: str
    confidence: Optional[float]
    feedback_text: Optional[str]
    proposed_label: Optional[str]


class FeedbackCount(BaseModel):
    count: int
    possible_ban: bool
    confirmed_ban: bool
    confirmed_player: bool
