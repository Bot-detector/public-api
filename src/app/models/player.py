from fastapi import HTTPException
from src.core.database.models.player import Player as dbPlayer
from src.core.database.models.report import Report as dbReport
from sqlalchemy import select, func
from sqlalchemy.sql.expression import Delete, Insert, Select, Update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.engine import Result

class Player:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_kc(self, player_names: list[str]):
        async with self.session:
            # Create aliases for the tables
            reporting_player: dbPlayer = aliased(dbPlayer, name="reporting_player")
            reported_player: dbPlayer = aliased(dbPlayer, name="reported_player")

            query: Select = select(
                [
                    func.count(func.distinct(reported_player.id)).label(
                        "count"
                    ),
                    reported_player.possible_ban,
                    reported_player.confirmed_ban,
                    reported_player.confirmed_player,
                ]
            )
            query = query.select_from(dbReport)
            query = query.join(
                reporting_player, dbReport.reportingID == reporting_player.id
            )
            query = query.join(
                reported_player, dbReport.reportedID == reported_player.id
            )
            query = query.where(reporting_player.name.in_(player_names))
            query = query.group_by(
                reported_player.possible_ban,
                reported_player.confirmed_ban,
                reported_player.confirmed_player,
            )
            result:Result = await self.session.execute(query)
            await self.session.commit()
        return tuple(result.mappings())
