from pydantic import BaseModel
from datetime import datetime

class PredictionResponse(BaseModel):
    name: str
    prediction: str
    id: int
    created: datetime
    predicted_confidence: float
    real_player: float
    unknown_bot: float
    pvm_melee_bot: float
    smithing_bot: float
    magic_bot: float
    fishing_bot: float
    mining_bot: float
    crafting_bot: float
    pvm_ranged_magic_bot: float
    pvm_ranged_bot: float
    hunter_bot: float
    fletching_bot: float
    clue_scroll_bot: float
    lms_bot: float
    agility_bot: float
    wintertodt_bot: float
    runecrafting_bot: float
    zalcano_bot: float
    woodcutting_bot: float
    thieving_bot: float
    soul_wars_bot: float
    cooking_bot: float
    vorkath_bot: float
    barrows_bot: float
    herblore_bot: float
    zulrah_bot: float