from pydantic import BaseModel, EmailStr
from app.db.models.role import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: Role
