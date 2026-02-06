from pydantic import BaseModel


class FeatureFlagCreate(BaseModel):
    key: str
    enabled: bool


class FeatureFlagRead(BaseModel):
    id: int
    key: str
    enabled: bool