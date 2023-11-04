from sqlalchemy import Boolean, Column, DateTime, Integer, Text
from sqlalchemy.orm import relationship  # Import relationship

from src.core.database.database import Base
from src.core.database.models.feedback import (
    DataModelPredictionFeedback as dbDataModelPredictionFeedback,
)


class Player(Base):
    __tablename__ = "Players"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    possible_ban = Column(Boolean)
    confirmed_ban = Column(Boolean)
    confirmed_player = Column(Boolean)
    label_id = Column(Integer)
    label_jagex = Column(Integer)
    ironman = Column(Boolean)
    hardcore_ironman = Column(Boolean)
    ultimate_ironman = Column(Boolean)
    normalized_name = Column(Text)

    # Define the relationship in the Player model
    feedback_given = relationship(
        "DataModelPredictionFeedback",
        foreign_keys=[dbDataModelPredictionFeedback.voter_id],
        back_populates="voter",
    )
    feedback_received = relationship(
        "DataModelPredictionFeedback",
        foreign_keys=[dbDataModelPredictionFeedback.subject_id],
        back_populates="subject",
    )
