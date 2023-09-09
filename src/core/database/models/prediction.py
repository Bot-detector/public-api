from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL
from src.core.database.database import Base



class Prediction(Base):
    __tablename__ = "Predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(12))
    prediction = Column(String(50))
    created = Column(TIMESTAMP)
    predicted_confidence = Column(DECIMAL(5, 2))
    real_player = Column(DECIMAL(5, 2))
    unknown_bot = Column(DECIMAL(5, 2))
    pvm_melee_bot = Column(DECIMAL(5, 2))
    smithing_bot = Column(DECIMAL(5, 2))
    magic_bot = Column(DECIMAL(5, 2))
    fishing_bot = Column(DECIMAL(5, 2))
    mining_bot = Column(DECIMAL(5, 2))
    crafting_bot = Column(DECIMAL(5, 2))
    pvm_ranged_magic_bot = Column(DECIMAL(5, 2))
    pvm_ranged_bot = Column(DECIMAL(5, 2))
   
