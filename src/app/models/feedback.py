import logging
from sqlalchemy import select
from src.app.views.input.feedback import FeedbackIn
from src.core.kafka.engine import AioKafkaEngine

logger = logging.getLogger(__name__)

from src.core.database.models.feedback import Feedback as dbFeedback


class Feedback:
    """
    Represents a class for retrieving feedback from the database.

    Args:
        session (AsyncSession): An asynchronous SQLAlchemy session.

    Attributes:
        session (AsyncSession): The asynchronous SQLAlchemy session to use for database operations.

    Methods:
        get_feedback(player_name: str) -> list[dict]:
            Fetch feedback for a given player by their name.

    """

    def __init__(self, kafka_engine: AioKafkaEngine, session) -> None:
        self.kafka_engine = kafka_engine
        self.session = session
        pass

    async def get_feedback(self, player_names: tuple[str]) -> list[dict]:
        """
        Fetch feedback for given players by their names.

        Args:
            player_names (tuple[str]): The names of the players whose feedback is to be retrieved.

        Returns:
            list[dict]: A list of dictionaries containing feedback data.

        """
        async with self.session:
            query: select = select(dbFeedback).where(
                dbFeedback.player_name.in_(player_names)
            )
            result = await self.session.execute(query)
            feedback_data = result.scalars().all()

        return [feedback.to_dict() for feedback in feedback_data]

    def _check_data_size(self, data: list[FeedbackIn]) -> list[FeedbackIn] | None:
        return None if len(data) > 5000 else data

    def _check_unique_voter(self, data: list[FeedbackIn]) -> list[FeedbackIn] | None:
        return None if len(set(d.voter_id for d in data)) > 1 else data

    async def parse_data(self, data: list[dict]) -> list[FeedbackIn] | None:
        """
        Parse and validate a list of feedback data.
        """
        data = self._check_data_size(data)
        if not data:
            logger.warning("invalid data size")
            return None

        data = self._check_unique_voter(data)
        if not data:
            logger.warning("invalid unique voter")
            return None
        return data

    async def send_to_kafka(self, data: list[FeedbackIn]) -> None:
        for feedback in data:
            feedback = feedback.model_dump_json()
            self.kafka_engine.message_queue.put_nowait(feedback)
        return
