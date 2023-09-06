from sqlalchemy import Boolean, Column, DateTime, Integer, Table, Text

from src.core.database.database import metadata

players = Table(
    "Players",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", Text),
    Column("created_at", DateTime),
    Column("updated_at", DateTime),
    Column("possible_ban", Boolean),
    Column("confirmed_ban", Boolean),
    Column("confirmed_player", Boolean),
    Column("label_id", Integer),
    Column("label_jagex", Integer),
    Column("ironman", Boolean),
    Column("hardcore_ironman", Boolean),
    Column("ultimate_ironman", Boolean),
    Column("normalized_name", Text),
)
