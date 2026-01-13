from sqlmodel import SQLModel, Field
from typing import Optional

class FeatureFlag(SQLModel, table=True):
    __tablename__ = "feature_flag"

    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    enabled: bool = Field(default=False)