from typing import Optional

from pydantic import BaseModel, Field, validator


class FeedbackInput(BaseModel):
    """
    Class representing prediction feedback input.
    """

    player_name: str = Field(
        ...,
        example="Player1",
        min_length=1,
        max_length=50,
        description="Name of the player",
    )
    vote: int = Field(..., ge=-1, le=1, description="Vote is -1, 0 or 1")
    prediction: str = Field(
        ...,
        example="real_player",
        description="Prediction for the player",
    )
    confidence: Optional[float] = Field(
        0, ge=0, le=1, description="Confidence level of the prediction"
    )
    subject_id: int = Field(..., example=1, description="ID of the subject")
    feedback_text: Optional[str] = Field(
        None, example="Test feedback", max_length=250, description="Feedback text"
    )
    proposed_label: Optional[str] = Field(
        None,
        example="real_player",
        description="Proposed label for the player",
    )

    @validator("player_name")
    def player_name_validator(cls, value: str):
        match value:
            case _ if 1 <= len(value) <= 12:
                return value
            case _ if value.lower().startswith("anonymoususer"):
                return value
            case _:
                raise ValueError("Invalid format for player_name")
