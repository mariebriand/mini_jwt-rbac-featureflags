"""
Single source of truth for static runtime configuration:
- Infrastructure/environment
- Security/auth
- App behavior flags
- Performance/limits

Order of priority:
- Runtime env variables
- .env file
- Defaults in code
"""

from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---------------- App ---------------------
    app_name: str = "Mini Auth Service"
    app_version: str = "0.1.0"

    env: Literal["dev", "prod"] = "dev"
    debug: bool = False
    testing: bool = False

    # ---------------- Database ----------------
    database_url: str = "sqlite:////data/dev.db"

    # ---------------- Security ----------------
    jwt_secret_key: SecretStr = SecretStr("change-me-in-production")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 10
    bcrypt_rounds: int = 12

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def is_production(self) -> bool:
        return self.env == "prod"


# Must be a singleton
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
