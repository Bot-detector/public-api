import re
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from src.core.fastapi.dependencies.player_label import PlayerLabel


class FeedbackInput(BaseModel):
    """
    Class representing prediction feedback input.
    """

    player_name: str = Field(
        ...,
        example="Player1",
        min_length=1,
        max_length=13,
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
