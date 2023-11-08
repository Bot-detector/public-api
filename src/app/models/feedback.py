import logging

from sqlalchemy import func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import select

from src.app.views.response.feedback import FeedbackResponse
from src.core.database.models.feedback import DataModelPredictionFeedback as dbFeedback
from src.core.database.models.player import Player as dbPlayer


class Feedback:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.logger = logging.getLogger("Feedback")

    async def get_feedback_responses(self, player_names: list[str]):
        async with self.session:
            print(f"Player names: {player_names}")
            feedback_voter: dbFeedback = aliased(dbFeedback, name="feedback_voter")
            feedback_subject: dbFeedback = aliased(dbFeedback, name="feedback_subject")
            player_name: dbPlayer = aliased(dbPlayer, name="player_name")

            query = select(
                [
                    func.count(feedback_voter.vote).label("count"),
                    feedback_voter.prediction,
                    feedback_voter.confidence,
                    player_name.name,
                    feedback_voter.feedback_text,
                    feedback_voter.proposed_label,
                ]
            )
            query = query.select_from(dbPlayer)
            query = query.join(
                feedback_subject, feedback_subject.subject_id == dbPlayer.id
            )
            query = query.join(feedback_voter, feedback_voter.voter_id == dbPlayer.id)
            query = query.where(player_name.name.in_(player_names))
            query = query.group_by(feedback_voter.vote)
            result: Result = await self.session.execute(query)
            await self.session.commit()

        feedback_responses = [
            FeedbackResponse(
                # player_name=feedback.name,
                count=feedback.vote,
                # prediction=feedback.prediction,
                # confidence=feedback.confidence,
                # feedback_text=feedback.feedback_text,
                # proposed_label=feedback.proposed_label,
            )
            for feedback in result.mappings().all()
        ]
        logging.debug(f"Output result: {feedback_responses}")

        return feedback_responses
