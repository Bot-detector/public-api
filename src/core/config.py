from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str