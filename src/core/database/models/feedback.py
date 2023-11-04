from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
    ForeignKey,
    String,
    Float,
    Text,
    SmallInteger,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from src.core.database.database import Base
from src.core.database.models.player import Player as dbPlayer


class DataModelPredictionFeedback(Base):
    __tablename__ = "PredictionFeedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    voter_id = Column(Integer, ForeignKey("Players.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("Players.id"), nullable=False)
    prediction = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    vote = Column(Integer, nullable=False, server_default="0")
    feedback_text = Column(Text(collation="utf8mb4_0900_ai_ci"))
    reviewed = Column(SmallInteger, nullable=False, server_default="0")
    reviewer_id = Column(Integer)
    user_notified = Column(SmallInteger, nullable=False, server_default="0")
    proposed_label = Column(String(50))
    voter = relationship(
        "Player",  # Use the actual class name from Player model
        foreign_keys=[dbPlayer.id],
        back_populates="feedback_given",
    )
    subject = relationship(
        "Player",  # Use the actual class name from Player model
        foreign_keys=[dbPlayer.id],
        back_populates="feedback_received",
    )
