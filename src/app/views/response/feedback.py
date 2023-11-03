from pydantic import BaseModel


class FeedbackResponse(BaseModel):
    player_name: str
    vote: int
    prediction: str
    confidence: float
    subject_id: int
    feedback_text: str
    proposed_label: str
