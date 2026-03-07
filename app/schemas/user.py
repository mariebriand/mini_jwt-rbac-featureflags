import re

from pydantic import BaseModel, EmailStr, field_validator

from app.db.models.role import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        stripped_value = value.strip()

        if not value or len(stripped_value) == 0:
            raise ValueError("Password must not be empty")

        # Passphrases are encouraged by modern security guidelines (NIST, etc.),
        # so we allow spaces in the middle of the password, but not leading or trailing whitespace.
        if value != stripped_value:
            raise ValueError("Password must not start/end with a whitespace")

        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if len(value) > 128:
            raise ValueError("Password must not exceed 128 characters")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one number")

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")

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
