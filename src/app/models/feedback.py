# import logging

from sqlalchemy import func, text
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import select

from src.app.views.response.feedback import Feedback as ResponseFeedback
from src.app.views.response.feedback import FeedbackCount
from src.core.database.models.feedback import DataModelPredictionFeedback as dbFeedback
from src.core.database.models.player import Player as dbPlayer


class Feedback:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        # self.logger = logging.getLogger("Feedback")

    async def get_feedback(self, player_names: list[str]):
        async with self.session:
            # print(f"Player names: {player_names}")
            feedback_voter: dbFeedback = aliased(dbFeedback, name="feedback_voter")
            feedback_subject: dbFeedback = aliased(dbFeedback, name="feedback_subject")
            player_db: dbPlayer = aliased(dbPlayer, name="player_db")

            query = select(
                [
                    feedback_voter.vote,
                    feedback_voter.prediction,
                    feedback_voter.confidence,
                    player_db.name,
                    feedback_voter.feedback_text,
                    feedback_voter.proposed_label,
                ]
            )
            query = query.select_from(player_db)
            query = query.join(
                feedback_subject, player_db.id == feedback_subject.subject_id
            )
            query = query.join(feedback_voter, player_db.id == feedback_voter.voter_id)
            query = query.where(player_db.name.in_(player_names))
            result: Result = await self.session.execute(query)
            await self.session.commit()

        result_set = result.mappings().all()
        feedback_responses = [
            ResponseFeedback(
                player_name=feedback.name,
                vote=feedback.vote,
                prediction=feedback.prediction,
                confidence=feedback.confidence,
                feedback_text=feedback.feedback_text,
                proposed_label=feedback.proposed_label,
            )
            for feedback in result_set
        ]

        # logging.debug(f"Output result: {feedback_responses}")

        return feedback_responses

    async def get_feedback_score(self, player_names: list[str]):
        async with self.session:
            # print(f"Player names: {player_names}")
            feedback_db: dbFeedback = aliased(dbFeedback, name="feedback_db")
            player_db: dbPlayer = aliased(dbPlayer, name="player_db")

            # Revised code
            subquery_feedback_db = (
                select(
                    [
                        func.count(feedback_db.vote).label("count"),
                        feedback_db.voter_id,
                    ]
                )
                .group_by(feedback_db.voter_id)
                .subquery()
            )

            query = select(
                [
                    subquery_feedback_db.c.count,
                    player_db.possible_ban,
                    player_db.confirmed_ban,
                    player_db.confirmed_player,
                ]
            )
            query = query.join(
                player_db, subquery_feedback_db.c.voter_id == player_db.id
            )
            query = query.where(player_db.name.in_(player_names))
            result: Result = await self.session.execute(query)
            await self.session.commit()

        result_set = (
            result.mappings().all()
        )  # needs to be saved to get it into a list to properly iterate over it

        feedbackcount_responses = [
            FeedbackCount(
                count=feedback["count"],
                possible_ban=feedback["possible_ban"],
                confirmed_ban=feedback["confirmed_ban"],
                confirmed_player=feedback["confirmed_player"],
            )
            for feedback in result_set
        ]
        # logging.debug(f"Output result feedbackcount model: {feedbackcount_responses}")

        return feedbackcount_responses
