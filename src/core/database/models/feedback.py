from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    SmallInteger,
    TIMESTAMP,
    ForeignKey,
)

# from sqlalchemy.sql import text
# from sqlalchemy.orm import relationship
from src.core.database.database import Base


class Feedback(Base):
    __tablename__ = "Feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts = Column(TIMESTAMP)
    voter_id = Column(Integer, ForeignKey("Players.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("Players.id"), nullable=False)
    prediction = Column(String(50), nullable=False)
    confidence = Column(Float, nullable=False)
    vote = Column(Integer, server_default="0", nullable=False)
    feedback_text = Column(Text(collation="utf8mb4_0900_ai_ci"))
    reviewed = Column(SmallInteger, server_default="0", nullable=False)
    reviewer_id = Column(Integer)
    user_notified = Column(SmallInteger, server_default="0", nullable=False)
    proposed_label = Column(String(50))

    # voter = relationship("Player", foreign_keys=[voter_id])
    # subject = relationship("Player", foreign_keys=[subject_id])
