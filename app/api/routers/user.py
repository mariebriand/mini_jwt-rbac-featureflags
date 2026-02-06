from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db.session import get_session
from app.db.models import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    # Check if email exists
    existing_user = session.exec(
        select(User).where(User.email == user_in.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Hash the password
    hashed_pw = hash_password(user_in.password)
    db_user = User(email=user_in.email, hashed_password=hashed_pw)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def read_user(user_id: int, session: Session = Depends(get_session)):
    # Check if id exists
    existing_user = session.exec(select(User).where(User.id == user_id)).first()
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    return existing_user
