import jwt

from datetime import datetime, timedelta, timezone

SECRET_KEY = (
    "SUPER_SECRET_KEY"  # For signing tokens: will use ENV variable in production
)
ALGORITHM = "HS256"  # Same key will be used for encoding and decoding JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def create_access_token(data: dict, expires_delta: int | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
