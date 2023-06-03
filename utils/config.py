from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_db_url: str
    mongo_db_name: str
    redis_url: str
    smtp_server: str
    smtp_port: int
    sender_email: str
    smtp_password: str

    class Config:
        env_file = ".env"


def get_settings() -> BaseSettings:
    return Settings()
