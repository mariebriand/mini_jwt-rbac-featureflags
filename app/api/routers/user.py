from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, delete

from app.core.security import hash_password
from app.db.models import User
from app.db.session import get_session
from app.schemas.user import UserCreate, UserRead, UserUpdate

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


@router.get("/all", response_model=List[UserRead], status_code=status.HTTP_200_OK)
def read_all_users(session: Session = Depends(get_session)):
    all_users = session.exec(select(User)).all()
    return all_users


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def read_user(user_id: int, session: Session = Depends(get_session)):
    # Check if id exists
    existing_user = session.get(User, user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    return existing_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    # Check if id exists
    existing_user = session.get(User, user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    session.delete(existing_user)
    session.commit()


@router.patch(
    "/update/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK
)
def update_user(
    user_id: int, user_in: UserUpdate, session: Session = Depends(get_session)
):
    # Check if id exists
    existing_user = session.get(User, user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    update_data = user_in.model_dump(exclude_unset=True)

    # Handle email uniqueness if email is being updated
    if "email" in update_data and update_data["email"] != existing_user.email:
        email_exists = session.exec(
            select(User).where(User.email == update_data["email"].lower())
        ).first()
        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        update_data["email"] = update_data["email"].lower()

    # Apply rest of updates
    for key, value in update_data.items():
        setattr(existing_user, key, value)

    session.add(existing_user)
    session.commit()
    session.refresh(existing_user)

    return existing_user
