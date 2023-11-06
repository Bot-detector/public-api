from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select
from sqlalchemy.orm import aliased
from sqlalchemy.engine import Result
from src.core.database.models.feedback import DataModelPredictionFeedback as dbFeedback
from src.core.database.models.player import Player as dbPlayer
from src.app.views.response.feedback import PredictionFeedbackResponse
import logging


class AppModelFeedback:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.logger = logging.getLogger("AppModelFeedback")

    async def get_feedback_responses(self, player_names: tuple[str]):
        async with self.session:
            feedback_voter: dbFeedback = aliased(dbFeedback, name="feedback_voter")
            feedback_subject: dbFeedback = aliased(dbFeedback, name="feedback_subject")
            player_name: dbPlayer = aliased(dbPlayer, name="player_name")

            query = select(
                [
                    feedback_voter.vote,
                    feedback_voter.prediction,
                    feedback_voter.confidence,
                    player_name.name.label(
                        "player_name"
                    ),  # Alias it with 'player_name'
                    feedback_voter.feedback_text,
                    feedback_voter.proposed_label,
                ]
            )
            query = query.select_from(dbPlayer)
            query = query.join(
                feedback_subject, feedback_subject.subject_id == dbPlayer.id
            )
            query = query.join(feedback_voter, feedback_voter.voter_id == dbPlayer.id)
            query = query.where(dbPlayer.name.in_(player_names))

            # debug
            sql_statement = str(query)
            sql_parameters = query.compile().params
            self.logger.debug(f"SQL Statement: {sql_statement}")
            self.logger.debug(f"SQL Parameters: {sql_parameters}")

            result: Result = await self.session.execute(query)
            self.logger.debug(f"Result: {result.scalars().all()}")
            await self.session.commit()
            # feedback_responses = [
            #     PredictionFeedbackResponse(
            #         player_name=feedback.name,
            #         vote=feedback.vote,
            #         prediction=feedback.prediction,
            #         confidence=feedback.confidence,
            #         feedback_text=feedback.feedback_text,
            #         proposed_label=feedback.proposed_label,
            #     )
            #     for feedback in result.scalars().all()
            # ]

        return tuple(result.mappings())
