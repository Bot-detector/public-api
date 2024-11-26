import asyncio

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    ENV: str
    DATABASE_URL: str
    KAFKA_HOST: str
    POOL_RECYCLE: int
    POOL_TIMEOUT: int


settings = Settings()

DB_SEMAPHORE = asyncio.Semaphore(100)
