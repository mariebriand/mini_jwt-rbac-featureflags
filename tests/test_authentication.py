from app.db.models import User
from app.core.security import hash_password


def test_login_success(client, session):
    user_data = {"email": "alice@example.com", "password": "secret123"}
    hashed_pw = hash_password(user_data["password"])
    user = User(email=user_data["email"], hashed_password=hashed_pw)

    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.post(
        "/authn/login",
        data={"username": user_data["email"], "password": user_data["password"]},
    )

    assert response.status_code == 200
    json_data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"


def test_login_fail_invalid_password(client, session):
    user_data = {"email": "alice@example.com", "password": "secret123"}
    hashed_pw = hash_password(user_data["password"])
    user = User(email=user_data["email"], hashed_password=hashed_pw)

    session.add(user)
    session.commit()

    response = client.post(
        "/authn/login",
        data={"username": user_data["email"], "password": "wrongpassword"},
    )

    assert response.status_code == 401
    assert "access_token" not in response.json()


def test_login_fail_inactive_user(client, session):
    user_data = {"email": "alice@example.com", "password": "secret123"}
    hashed_pw = hash_password(user_data["password"])
    user = User(email=user_data["email"], hashed_password=hashed_pw, is_active=False)

    session.add(user)
    session.commit()

    response = client.post(
        "/authn/login",
        data={"username": user_data["email"], "password": "secret123"},
    )

    assert response.status_code == 403
    assert "access_token" not in response.json()


def test_login_fail_nonexistent_user(client, session):
    response = client.post(
        "/authn/login",
        data={"username": "nonexistent@example.com", "password": "password123"},
    )

    assert response.status_code == 401


def test_login_fail_missing_credentials(client, session):
    # Missing password
    response = client.post(
        "/authn/login",
        data={"username": "alice@example.com"},
    )
    assert response.status_code == 422

    # Missing email
    response = client.post(
        "/authn/login",
        data={"password": "secret123"},
    )
    assert response.status_code == 422


def test_login_fail_empty_password(client, session):
    """Login fail with empty email or password"""

    user_data = {"email": "alice@example.com", "password": "secret123"}
    hashed_pw = hash_password(user_data["password"])
    user = User(email=user_data["email"], hashed_password=hashed_pw)

    session.add(user)
    session.commit()

    # Empty password
    response = client.post(
        "/authn/login",
        data={"username": user_data["email"], "password": ""},
    )
    assert response.status_code == 422

    # Empty email
    response = client.post(
        "/authn/login",
        data={"username": "", "password": "secret123"},
    )
    assert response.status_code == 422


def test_sql_injection_attempt(client, session):
    user_data = {"email": "alice@example.com", "password": "secret123"}
    hashed_pw = hash_password(user_data["password"])
    user = User(email=user_data["email"], hashed_password=hashed_pw)

    session.add(user)
    session.commit()

    response = client.post(
        "/authn/login",
        data={
            "username": "alice@example.com' OR '1'='1",  # Malicious input
            "password": "anything",
        },
    )

    assert response.status_code == 401
