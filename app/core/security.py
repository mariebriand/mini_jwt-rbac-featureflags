import hashlib
import unicodedata

from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=getattr(settings, "bcrypt_rounds", 12),
)


def _prehash(password: str) -> str:
    """
    Deterministically pre-hash the password to avoid bcrypt's 72-byte limit and
    normalize unicode to prevent equivalent-but-different inputs.
    """
    pw = unicodedata.normalize("NFKC", (password or ""))
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    if not password or len(password.strip()) == 0:
        raise ValueError("Password must not be empty")

    return pwd_context.hash(_prehash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(_prehash(plain_password), hashed_password)
    except Exception:
        return False
