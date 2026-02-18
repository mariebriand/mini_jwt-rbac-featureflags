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
from typing import List, Literal

from pydantic import SecretStr, model_validator
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
    
    cors_allowed_origins: List[str] = [""]  # dev default
   

    @model_validator(mode="after") # runs after all other validation and parsing is done
    def check_prod_cors(self) -> "Settings":
        if self.env == "prod" and self.cors_allowed_origins == [""]:
            raise ValueError("cors_allowed_origins must be explicitly set in production")
        return self
    
    @property
    def is_production(self) -> bool:
        return self.env == "prod"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


# Must be a singleton
@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
