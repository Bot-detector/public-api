from pydantic import BaseModel
from pydantic.fields import Field
from typing import Optional


class PredictionFeedbackResponse(BaseModel):
    player_name: str
    vote: int
    prediction: str
    confidence: Optional[float]
    subject_id: int
    feedback_text: Optional[str]
    proposed_label: Optional[str]
