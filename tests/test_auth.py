from app.db.models import User
from app.core.security import hash_password


def test_login(client, session):
	user_data = {"email": "alice@example.com", "password": "secret123"}
	hashed_pw = hash_password(user_data["password"])
	user = User(email=user_data["email"], hashed_password=hashed_pw)
	session.add(user)
	session.commit()
	session.refresh(user)

	response = client.post(
		"/login",
		data={"username": user_data["email"], "password": user_data["password"]},
	)

	assert response.status_code == 200
	json_data = response.json()
	assert "access_token" in json_data
	assert json_data["token_type"] == "bearer"

def test_can_access_user(client, session):
	user_data = {"email": "alice@example.com", "password": "secret123"}
	hashed_pw = hash_password(user_data["password"])
	user = User(email=user_data["email"], hashed_password=hashed_pw)
	session.add(user)
	session.commit()
	session.refresh(user)

	response_login = client.post(
		"/login",
		data={"username": user_data["email"], "password": user_data["password"]},
	)

	token = response_login.json()["access_token"]

	response_access = client.get(
		"/users-only",
		headers={"Authorization": f"Bearer {token}"}
	)

	assert response_access.status_code == 200
