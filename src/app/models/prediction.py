from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, class_mapper
from sqlalchemy.sql.expression import Select

from src.core.database.models.prediction import Prediction as dbPrediction


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in class_mapper(obj.__class__).columns}


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

    async def get_prediction(self, user_name: str):
        """
        Fetch predictions for a given user by their username.

        Args:
            user_name (str): The username of the user whose predictions are to be retrieved.

        Returns:
            list[dict]: A list of dictionaries containing prediction data.

        """
        async with self.session:
            prediction_db: dbPrediction = aliased(dbPrediction, name="prediction_db")
            query: Select = select(prediction_db)
            query = query.select_from(prediction_db)
            query = query.where(prediction_db.name == user_name)
            result: Result = await self.session.execute(query)
            await self.session.commit()

        output = result.mappings().all()
        if output is None:
            return None
        output = [object_as_dict(o["prediction_db"]) for o in output]
        output = jsonable_encoder(output)

        return output
