from fastapi import APIRouter, Depends
from sqlmodel import Session, text

from app.db.session import get_session

router = APIRouter(tags=["health"])

@router.get("/health")
def health(session: Session = Depends(get_session)):
	try:
		session.exec(text("SELECT 1"))
		return {
			"status": "OK",
			"database": "OK",
		}
	except Exception:
		return {
			"status": "degraded",
			"database": "error",
		}