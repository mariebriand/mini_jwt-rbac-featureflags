from sqlmodel import SQLModel, Field
from sqlalchemy import event
from typing import Optional, List

from app.db.models.role import Role


class FeatureFlag(SQLModel, table=True):
    __tablename__ = "feature_flag"

    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True)
    enabled: bool = Field(default=False)


@event.listens_for(FeatureFlag, "before_insert")
@event.listens_for(FeatureFlag, "before_update")
def normalize_flag(mapper, connection, target):
    if target.key:
        target.key = target.key.strip().lower()
