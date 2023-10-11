from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DATABASE_URL: str
    KAFKA_HOST: str
    pool_recycle: int
    pool_timeout: int

settings = Settings()