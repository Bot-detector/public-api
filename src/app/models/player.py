from sqlalchemy import func, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import Select

from src.core.database.models.player import Player as dbPlayer
from src.core.database.models.report import Report as dbReport


class Player:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_kc(self, player_names: tuple[str]):
        """
        Retrieve Kill Count (KC) data for a list of player names.

        Args:
            player_names (list[str]): A list of player names for which KC data is requested.

        Returns:
            tuple: A tuple of dictionaries containing KC data for each player name. Each dictionary
                includes the following keys:
                - "count": The distinct count of reported players.
                - "possible_ban": Whether the player has a possible ban (True or False).
                - "confirmed_ban": Whether the player has a confirmed ban (True or False).
                - "confirmed_player": Whether the player is confirmed as a valid player (True or False).
                - "manual_detect": Wheter the detection was manual (True or False)
        """
        async with self.session:
            # Create aliases for the tables
            reporting_player: dbPlayer = aliased(dbPlayer, name="reporting_player")
            reported_player: dbPlayer = aliased(dbPlayer, name="reported_player")

            query: Select = select(
                [
                    func.count(func.distinct(reported_player.id)).label("count"),
                    reported_player.possible_ban,
                    reported_player.confirmed_ban,
                    reported_player.confirmed_player,
                    dbReport.manual_detect,
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
                dbReport.manual_detect,
            )
            result: Result = await self.session.execute(query)
            await self.session.commit()
        return tuple(result.mappings())
