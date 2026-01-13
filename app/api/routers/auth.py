from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.db.models import User
from app.db.session import get_session
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.dependencies import require_roles

router = APIRouter(tags=["auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
	statement = select(User).where(User.email == form_data.username)
	user = session.exec(statement).first()

	if not user or not verify_password(form_data.password, user.hashed_password):
		raise HTTPException(status_code=401, detail="Invalid credentials")

	token = create_access_token({
		"sub": user.email,
		"role": user.role.value
	})
	return {"access_token": token, "token_type": "bearer"}

@router.get("/superadmins-only")
def admin_endpoint(user: User = Depends(require_roles(["superadmin"]))):
	return {"message": f"Hello {user.email}, you are an superadmin!"}

@router.get("/admins-only")
def user_endpoint(user: User = Depends(require_roles(["superadmin", "admin"]))):
	return {"message": f"Hello {user.email}, you are a superadmin/admin!"}

@router.get("/users-only")
def user_endpoint(user: User = Depends(require_roles(["superadmin", "admin", "user"]))):
	return {"message": f"Hello {user.email}, you are a superadmin/admin/user!"}