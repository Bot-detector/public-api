from sqlalchemy import (
    TIMESTAMP,
    Column,
    Float,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Feedback(Base):
    __tablename__ = "Feedback"

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
        "Player", foreign_keys=[voter_id], back_populates="feedback_given"
    )
    subject = relationship(
        "Player", foreign_keys=[subject_id], back_populates="feedback_received"
    )

    __table_args__ = (
        UniqueConstraint("prediction", "subject_id", "voter_id", name="Unique_Vote"),
    )
