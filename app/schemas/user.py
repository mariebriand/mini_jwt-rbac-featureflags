from pydantic import BaseModel, EmailStr, field_validator
from app.db.models.role import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value or len(value.strip()) == 0:
            raise ValueError("Password cannot be empty")
        return value


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: Role


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None
    role: Role | None = None
