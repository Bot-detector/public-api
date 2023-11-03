from pydantic import BaseModel

class FeedbackResponse(BaseModel):
    id: int
    ts: str
    voter_id: int
    subject_id: int
    prediction: str
    confidence: float
    vote: int
    feedback_text: str
    reviewed: int
    reviewer_id: int
    user_notified: int
    proposed_label: str