import re
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, constr, validator

from src.core.fastapi.dependencies.player_label import PlayerLabel


class FeedbackInput(BaseModel):
    """
    Class representing prediction feedback input.
    """

    player_name: constr(strip_whitespace=True) = Field(
        ...,
        example="Player1",
        min_length=1,
        max_length=50,
        description="Name of the player",
    )
    vote: int = Field(..., ge=-1, le=1, description="Vote is -1, 0 or 1")
    prediction: PlayerLabel = Field(
        ...,
        example=PlayerLabel.real_player,
        description="Prediction for the player",
    )
    confidence: Optional[float] = Field(
        0, ge=0, le=1, description="Confidence level of the prediction"
    )
    subject_id: int = Field(..., example=1, description="ID of the subject")
    feedback_text: Optional[str] = Field(
        None, example="Test feedback", max_length=250, description="Feedback text"
    )
    proposed_label: Optional[PlayerLabel] = Field(
        None,
        example=PlayerLabel.real_player,
        description="Proposed label for the player",
    )

    @validator("player_name")
    def uuid_format(cls, value: str):
        pattern = r"^anonymoususer [0-9a-f]{8} [0-9a-f]{4} [0-9a-f]{4} [0-9a-f]{4} [0-9a-f]{12}$"
        if value.startswith("anonymoususer"):
            if not re.match(pattern, value):
                raise ValueError("Invalid format for anonymous user")
            if len(value) != 50:
                raise ValueError("Length of anonymous user name must be 50")
        else:
            if not (1 <= len(value) <= 13):
                raise ValueError("Length of player name must be between 1 and 13")
        return value
