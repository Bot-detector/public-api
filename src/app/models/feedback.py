import logging

from sqlalchemy import func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import Select, select

from src.app.views.response.feedback import FeedbackScore
from src.core.database.models.feedback import DataModelPredictionFeedback as dbFeedback
from src.core.database.models.player import Player as dbPlayer

logger = logging.getLogger(__name__)


class Feedback:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_feedback_score(self, player_names: list[str], vote: bool):
        async with self.session:
            # dbFeedback
            feedback_voter: dbPlayer = aliased(dbPlayer, name="feedback_voter")
            feedback_subject: dbPlayer = aliased(dbPlayer, name="feedback_subject")

            select_columns = [
                func.count(func.distinct(feedback_subject.id)).label("count"),
                feedback_subject.possible_ban,
                feedback_subject.confirmed_ban,
                feedback_subject.confirmed_player,
            ]
            if vote:
                select_columns.append(dbFeedback.vote.label("vote"))

            query: Select = select(select_columns)
            query = query.select_from(dbFeedback)
            query = query.join(feedback_voter, dbFeedback.voter_id == feedback_voter.id)
            query = query.join(
                feedback_subject, dbFeedback.subject_id == feedback_subject.id
            )
            query = query.where(feedback_voter.name.in_(player_names))
            group_by_columns = [
                feedback_subject.possible_ban,
                feedback_subject.confirmed_ban,
                feedback_subject.confirmed_player,
            ]
            if vote:
                group_by_columns.append(dbFeedback.vote)

            query = query.group_by(*group_by_columns)
            result: Result = await self.session.execute(query)
            await self.session.commit()

        result_set = (
            result.mappings().all()
        )  # needs to be saved to get it into a list to properly iterate over it

        logger.debug(f"result_set: {result_set}")

        feedbackscore_responses = [
            FeedbackScore(
                **{
                    **{
                        "count": feedback["count"],
                        "possible_ban": feedback["possible_ban"],
                        "confirmed_ban": feedback["confirmed_ban"],
                        "confirmed_player": feedback["confirmed_player"],
                    },
                    **({"vote": feedback["vote"]} if vote else {}),
                }
            )
            for feedback in result_set
        ]
        return feedbackscore_responses
