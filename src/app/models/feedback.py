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

    async def get_feedback_responses(self, player_names: list[str]):
        async with self.session:
            fv: dbFeedback = aliased(dbFeedback, name="feedback_voter")
            fs: dbFeedback = aliased(dbFeedback, name="feedback_subject")
            pn: dbPlayer = aliased(dbPlayer, name="player_name")

            query = select(
                [
                    fv.vote,
                    fv.prediction,
                    fv.confidence,
                    pn.name,
                    fv.feedback_text,
                    fv.proposed_label,
                ]
            )
            query = query.select_from(dbPlayer)
            query = query.join(fs, fs.subject_id == dbPlayer.id)
            query = query.join(fv, fv.voter_id == dbPlayer.id)
            query = query.where(pn.name.in_(player_names))

            # debug
            sql_statement = str(query)
            sql_parameters = query.compile().params
            self.logger.debug(f"SQL Statement: {sql_statement}")
            self.logger.debug(f"SQL Parameters: {sql_parameters}")

            result: Result = await self.session.execute(query)
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
        #     for feedback in result
        # ]
        # transform output to json
        output = result.mappings().all()
        logging.debug(f"Output result: {output}")
        # output = [o.get("Prediction") for o in output]
        # output = jsonable_encoder(output)
        return output
