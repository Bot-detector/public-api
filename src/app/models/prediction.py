from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select

from src.core.database.models.prediction import Prediction as dbPrediction


class Prediction:
    """
    Represents a class for retrieving predictions from the database.

    Args:
        session (AsyncSession): An asynchronous SQLAlchemy session.

    Attributes:
        session (AsyncSession): The asynchronous SQLAlchemy session to use for database operations.

    Methods:
        get_prediction(user_name: str) -> list[dict]:
            Fetch predictions for a given user by their username.

    """
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_prediction(self, user_name) -> list[dict]:
        """
        Fetch predictions for a given user by their username.

        Args:
            user_name (str): The username of the user whose predictions are to be retrieved.

        Returns:
            list[dict]: A list of dictionaries containing prediction data.

        """
        async with self.session:
            query: Select = select(dbPrediction)
            query = query.select_from(dbPrediction)
            query = query.where(dbPrediction.name == user_name)
            result: Result = await self.session.execute(query)
            await self.session.commit()

        # transform output to json
        output = result.mappings().all()
        output = [o.get("Prediction") for o in output]
        output = jsonable_encoder(output)
        return output
