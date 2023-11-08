import re
from typing import List, Optional

from pydantic import BaseModel, Field


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
    prediction: str = Field(
        ...,
        example="Real_Player",
        min_length=1,
        max_length=13,
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
        enum=[
            "real_player",
            "pvm_melee_bot",
            "smithing_bot",
            "magic_bot",
            "fishing_bot",
            "mining_bot",
            "crafting_bot",
            "pvm_ranged_magic_bot",
            "pvm_ranged_bot",
            "hunter_bot",
            "fletching_bot",
            "clue_scroll_bot",
            "lms_bot",
            "agility_bot",
            "wintertodt_bot",
            "runecrafting_bot",
            "zalcano_bot",
            "woodcutting_bot",
            "thieving_bot",
            "soul_wars_bot",
            "cooking_bot",
            "vorkath_bot",
            "barrows_bot",
            "herblore_bot",
            "unknown_bot",
        ],
    )