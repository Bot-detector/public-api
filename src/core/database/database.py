import sqlalchemy
from databases import Database
from src.core.config import settings
from sqlalchemy import MetaData

# Create a SQLAlchemy engine
engine = sqlalchemy.create_engine(settings.DATABASE_URL, echo=True, future=True)

database = Database(settings.DATABASE_URL)

# Define a metadata object
metadata = MetaData()