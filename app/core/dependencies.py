from fastapi import Depends, HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer

from app.db.session import get_session
from app.db.models import User
from app.core.jwt import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
	""" Extract the user from the JWT """
	try:
		payload = decode_access_token(token)
		email = payload.get("sub")
		if email is None:
			raise HTTPException(status_code=401, detail="Invalid token")
	except Exception:
		raise HTTPException(status_code=401, detail="Invalid token")
	user = session.exec(select(User).where(User.email == email)).first()
	if not user:
		raise HTTPException(status_code=401, detail="User not found")
	return user

def require_roles(required_roles: list[str]) ->  User:
	def dependency(user: User = Depends(get_current_user)):
		if not any (role in user.role for role in required_roles):
			raise HTTPException(status_code=403, detail="Forbidden")
		return user
	return dependency
