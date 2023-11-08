import logging

from sqlalchemy import func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import select

from src.app.views.response.feedback import Feedback, FeedbackCount
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
                    feedback_voter.vote,
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

            result: Result = await self.session.execute(query)
            await self.session.commit()

        feedback_responses = [
            Feedback(
                player_name=feedback.name,
                vote=feedback.vote,
                prediction=feedback.prediction,
                confidence=feedback.confidence,
                feedback_text=feedback.feedback_text,
                proposed_label=feedback.proposed_label,
            )
            for feedback in result.mappings().all()
        ]

        logging.debug(f"Output result: {feedback_responses}")

        return feedback_responses

    async def get_feedback_count(self, player_names: list[str]):
        async with self.session:
            print(f"Player names: {player_names}")
            feedback_voter: dbFeedback = aliased(dbFeedback, name="feedback_voter")
            # feedback_subject: dbFeedback = aliased(dbFeedback, name="feedback_subject")
            # player_name: dbPlayer = aliased(dbPlayer, name="player_name")
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
            query = query.where(reported_player.name.in_(player_names))

            result: Result = await self.session.execute(query)
            await self.session.commit()

        result_set = (
            result.mappings().all()
        )  # needs to be saved to get it into a list to properly iterate over it
        # logging.debug(f"Output result mappings: {result_set}")
        # logging.debug(f"Output result count: {len(result_set)}")
        # logging.debug(f"Output result type: {type(result_set)}")
        # for feedback in result_set:
        #     # get each fields
        #     logging.debug(
        #         f'count: {feedback["count"]}, type: {type(feedback["count"])}'
        #     )
        #     logging.debug(
        #         f'possible_ban: {feedback["possible_ban"]}, type: {type(feedback["possible_ban"])}'
        #     )
        #     logging.debug(
        #         f'confirmed_ban: {feedback["confirmed_ban"]}, type: {type(feedback["confirmed_ban"])}'
        #     )
        #     logging.debug(
        #         f'confirmed_player: {feedback["confirmed_player"]}, type: {type(feedback["confirmed_player"])}'
        #     )

        feedbackcount_responses = [
            FeedbackCount(
                count=feedback["count"],
                possible_ban=feedback["possible_ban"],
                confirmed_ban=feedback["confirmed_ban"],
                confirmed_player=feedback["confirmed_player"],
            )
            for feedback in result_set
        ]
        logging.debug(f"Output result feedbackcount model: {feedbackcount_responses}")

        return feedbackcount_responses
