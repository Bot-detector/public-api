from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import DB_SEMAPHORE
from src.core.database.database import SessionFactory


# Dependency to get an asynchronous session
async def get_session() -> AsyncSession:
    async with DB_SEMAPHORE:  # Acquire semaphore before accessing the session
        async with SessionFactory() as session:
            yield session  # Provide the session to the calling function
