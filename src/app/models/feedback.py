from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import Select
from src.app.models.player import Player as dbPlayer
from src.core.database.models.feedback import DataModelPredictionFeedback as dbFeedback
from src.app.views.response.feedback import PredictionFeedbackResponse


class AppModelFeedback:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_feedback_responses(
        self, player_names: list[str]
    ) -> list[PredictionFeedbackResponse]:
        """
        Retrieve feedback responses for a list of player names.

        Args:
            player_names (list[str]): A list of player names for which feedback responses are requested.

        Returns:
            list[FeedbackResponse]: A list of Pydantic BaseModel dictionaries containing feedback responses.
        """
        async with self.session:
            query: Select = select(
                [
                    dbFeedback.vote,
                    dbFeedback.prediction,
                    dbFeedback.confidence,
                    dbFeedback.subject_id,
                    dbFeedback.feedback_text,
                    dbFeedback.proposed_label,
                ]
            )
            query = query.where(dbFeedback.subject_id.in_(player_names))
            result: Result = await self.session.execute(query)
            await self.session.commit()

        feedback_responses = [
            PredictionFeedbackResponse(
                vote=feedback.vote,
                prediction=feedback.prediction,
                confidence=feedback.confidence,
                subject_id=feedback.subject_id,
                feedback_text=feedback.feedback_text,
                proposed_label=feedback.proposed_label,
            )
            for feedback in result.scalars()
        ]

        return feedback_responses
