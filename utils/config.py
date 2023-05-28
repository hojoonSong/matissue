from pydantic import BaseSettings


class Settings(BaseSettings):
    mongo_db_url: str = "mongodb+srv://shinyubin18:DDYxIIRc0DJKS1Cn@fast.tfq6irt.mongodb.net/"
    mongo_db_name: str = "FAST"

    class Config:
        env_file = ".env"


def get_settings() -> BaseSettings:
    return Settings()
