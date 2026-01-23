from sqlmodel import SQLModel, Field
from typing import Optional

from app.db.models.role import Role


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    is_active: bool = True
    role: Role = Field(default=Role.USER)
