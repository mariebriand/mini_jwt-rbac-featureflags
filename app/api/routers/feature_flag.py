from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select

from app.core.limiter import limiter
from app.db.models import FeatureFlag as Flag
from app.db.session import get_session
from app.schemas.feature_flag import (
    FeatureFlagCreate as FlagCreate,
    FeatureFlagRead as FlagRead,
)

router = APIRouter(prefix="/feature_flag", tags=["feature_flag"])


@router.post("/", response_model=FlagRead, status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
def create_flag(
    request: Request, flag_in: FlagCreate, session: Session = Depends(get_session)
):
    existing_flag = session.exec(select(Flag).where(Flag.key == flag_in.key)).first()
    if existing_flag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Key already registered"
        )

    db_flag = Flag(key=flag_in.key, enabled=flag_in.enabled)
    session.add(db_flag)
    session.commit()
    session.refresh(db_flag)
    return db_flag


@router.get("/{key}", response_model=FlagRead, status_code=status.HTTP_200_OK)
@limiter.limit("60/minute")
def read_flag(request: Request, key: str, session: Session = Depends(get_session)):
    existing_flag = session.exec(select(Flag).where(Flag.key == key)).first()
    if not existing_flag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Key does not exist"
        )
    return existing_flag
