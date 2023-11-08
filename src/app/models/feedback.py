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
            player_name: dbPlayer = aliased(dbPlayer, name="player_name")

            query = select(
                [
                    feedback_voter.vote,
                    feedback_voter.prediction,
                    feedback_voter.confidence,
                    player_name.name,
                    feedback_voter.feedback_text,
                    feedback_voter.proposed_label,
                ]
            )
            query = query.select_from(player_name)
            query = query.join(
                feedback_subject, feedback_subject.subject_id == player_name.id
            )
            query = query.join(
                feedback_voter, feedback_voter.voter_id == player_name.id
            )
            query = query.where(
                text("player_name.name IN :names").bindparams(
                    names=player_names
                )  # prevent sql injection
            )
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

    async def get_feedback_count(self, player_names: list[str]):
        async with self.session:
            # print(f"Player names: {player_names}")
            feedback_voter: dbFeedback = aliased(dbFeedback, name="feedback_voter")
            reported_player: dbPlayer = aliased(dbPlayer, name="reported_player")

            # Revised code
            subquery = (
                select(
                    [
                        func.count(feedback_voter.vote).label("count"),
                        feedback_voter.voter_id,
                    ]
                )
                .group_by(feedback_voter.voter_id)
                .subquery()
            )

            query = select(
                [
                    subquery.c.count,
                    reported_player.possible_ban,
                    reported_player.confirmed_ban,
                    reported_player.confirmed_player,
                ]
            )
            query = query.join(
                reported_player, subquery.c.voter_id == reported_player.id
            )
            query = query.where(
                text("reported_player.name IN :names").bindparams(names=player_names)
            )  # prevent sql injection

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
