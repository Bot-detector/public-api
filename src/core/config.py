from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str
    DATABASE_URL: str
    KAFKA_HOST: str = "localhost:9094"

settings = Settings()