import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.core.config import settings

# Create an async SQLAlchemy engine
engine = create_async_engine(settings.DATABASE_URL, pool_timeout=settings.POOL_TIMEOUT, pool_recycle=settings.POOL_RECYCLE, echo=(settings.ENV != "PRD"))
# Create a session factory
SessionFactory = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,  # Use AsyncSession for asynchronous operations
)

Base = declarative_base()
