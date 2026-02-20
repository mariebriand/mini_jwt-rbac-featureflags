from pydantic import BaseModel, field_validator
import re


class FeatureFlagCreate(BaseModel):
    key: str
    enabled: bool

    @field_validator("key")
    @classmethod
    def validate_key(cls, value: str) -> str:
        stripped_value = value.strip().lower()

        if not value or len(stripped_value) == 0:
            raise ValueError("Key must not be empty")

        if len(stripped_value) > 100:
            raise ValueError("Key must not exceed 100 characters")

        if not re.match(r"^[a-z0-9_-]+$", stripped_value):  # slug-like validation
            raise ValueError(
                "Key must only contain lowercase letters, numbers, underscores, and hyphens"
            )

        return stripped_value


class FeatureFlagRead(BaseModel):
    id: int
    key: str
    enabled: bool
