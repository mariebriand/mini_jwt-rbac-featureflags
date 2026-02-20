from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
from app.core.config import settings


def get_rate_limit_key(request: Request) -> str:
    # if the user is authenticated, use their ID to prevent bypassing limits by rotating IPs
    user = getattr(request.state, "user", None)
    if user:
        return str(user.id)
    # otherwise fall back to IP
    ip_addr = get_remote_address(request)
    return ip_addr


limiter = Limiter(
    key_func=get_rate_limit_key, swallow_errors=False, enabled=not settings.testing
)


def setup_limiter(app: FastAPI) -> None:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
