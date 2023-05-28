from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_db_url: str
    mongo_db_name: str

    class Config:
        env_file = ".env"


def get_settings() -> BaseSettings:
    return Settings()
