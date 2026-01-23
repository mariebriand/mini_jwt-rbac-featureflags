import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prehash(password: str) -> bytes:
    """
    Pre-hash the password to avoid bcrypt's 72-byte limit and unicode-related issues.
    """
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()  # to avoid returning raw bytes that can include NULL as bcrypt does not allow them in pw input


def hash_password(password: str) -> str:
    return pwd_context.hash(_prehash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_prehash(plain_password), hashed_password)
