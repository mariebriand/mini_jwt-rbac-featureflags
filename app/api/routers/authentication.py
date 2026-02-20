from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.jwt import create_access_token
from app.core.limiter import limiter
from app.core.security import verify_password
from app.db.models import User
from app.db.session import get_session


router = APIRouter(prefix="/authn", tags=["authn"])


@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Account is not active"
        )

    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return {"access_token": token, "token_type": "bearer"}
