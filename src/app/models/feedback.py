from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select

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

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_feedback(self, player_name) -> list[dict]:
        """
        Fetch feedback for a given player by their name.

        Args:
            player_name (str): The name of the player whose feedback is to be retrieved.

        Returns:
            list[dict]: A list of dictionaries containing feedback data.

        """
        async with self.session:
            query: Select = select(dbFeedback)
            query = query.select_from(dbFeedback)
            query = query.where(dbFeedback.player_name == player_name)
            result: Result = await self.session.execute(query)
            await self.session.commit()

        # transform output to json
        output = result.mappings().all()
        output = [o.get("Feedback") for o in output]
        output = jsonable_encoder(output)
        return output
