from sqlalchemy import (
    TIMESTAMP,
    BigInteger,
    Column,
    Integer,
    MetaData,
    SmallInteger,
    Table,
)

from src.core.database.database import metadata

# Define the "Reports" table
Reports = Table(
    "Reports",
    metadata,
    Column("ID", BigInteger, primary_key=True, autoincrement=True),
    Column("created_at", TIMESTAMP),
    Column("reportedID", Integer),
    Column("reportingID", Integer),
    Column("region_id", Integer),
    Column("x_coord", Integer),
    Column("y_coord", Integer),
    Column("z_coord", Integer),
    Column("timestamp", TIMESTAMP),
    Column("manual_detect", SmallInteger),
    Column("on_members_world", Integer),
    Column("on_pvp_world", SmallInteger),
    Column("world_number", Integer),
    Column("equip_head_id", Integer),
    Column("equip_amulet_id", Integer),
    Column("equip_torso_id", Integer),
    Column("equip_legs_id", Integer),
    Column("equip_boots_id", Integer),
    Column("equip_cape_id", Integer),
    Column("equip_hands_id", Integer),
    Column("equip_weapon_id", Integer),
    Column("equip_shield_id", Integer),
    Column("equip_ge_value", BigInteger),
)
