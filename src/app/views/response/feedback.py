from typing import Optional

from pydantic import BaseModel
from pydantic.fields import Field


class FeedbackResponse(BaseModel):
    player_name: str
    vote: int
    prediction: str
    confidence: Optional[float]
    feedback_text: Optional[str]
    proposed_label: Optional[str]
