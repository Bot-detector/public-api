import asyncio

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DATABASE_URL: str
    KAFKA_HOST: str
    POOL_RECYCLE: int
    POOL_TIMEOUT: int


settings = Settings()
producer = None
send_queue = None
sd_event = asyncio.Event()
