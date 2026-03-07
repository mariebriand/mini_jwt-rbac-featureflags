from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, text

from app.core.limiter import limiter
from app.db.session import get_session

router = APIRouter(tags=["health"])


@router.get("/health")
@limiter.limit("60/minute")
def health(request: Request, session: Session = Depends(get_session)):
    try:
        session.execute(text("SELECT 1"))
        return {
            "status": "OK",
            "database": "OK",
        }
    except Exception:
        return {
            "status": "degraded",
            "database": "error",
        }
