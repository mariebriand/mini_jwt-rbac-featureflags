from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Mini Auth Service"
    app_version: str = "0.1.0"
    debug: bool = True
    database_url: str = "sqlite:///./auth.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
