import pytest

from app.db.models import User
from app.core.security import hash_password

from app.db.models.role import Role


@pytest.fixture
def test_user(client):
    response = client.post(
        "/user/",
        json={"email": "test_user@example.com", "password": "Secret123!"},
    )
    return response.json()


@pytest.fixture
def auth_token(client, session):
    user_data = {"email": "test_superadmin@example.com", "password": "Secret123!"}
    hashed_pw = hash_password(user_data["password"])
    user = User(
        email=user_data["email"], hashed_password=hashed_pw, role=Role.SUPERADMIN
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.post(
        "/authn/login",
        data={"username": user_data["email"], "password": user_data["password"]},
    )
    return response.json()["access_token"]


@pytest.fixture
def test_flag(client):
    response = client.post(
        "/feature_flag/",
        json={"key": "test_flag", "enabled": True},
    )
    return response.json()


def test_authn_rate_limit(client, test_user):
    for _ in range(6):# limit is 5/minute
        response = client.post(
            "/authn/login",
            data={"username": "test_user@example.com", "password": "Secret123!"},
        )

    assert response.status_code == 429


def test_authz_users_only_rate_limit(client, auth_token):
    for _ in range(61):
        response = client.get(
            "/authz/users-only",
            headers={"Authorization": f"Bearer {auth_token}"},
        )

    assert response.status_code == 429


def test_authz_admins_only_rate_limit(client, auth_token):
    for _ in range(61):
        response = client.get(
            "/authz/admins-only",
            headers={"Authorization": f"Bearer {auth_token}"},
        )

    assert response.status_code == 429


def test_authz_superadmins_only_rate_limit(client, auth_token):
    for _ in range(61):
        response = client.get(
            "/authz/superadmins-only",
            headers={"Authorization": f"Bearer {auth_token}"},
        )

    assert response.status_code == 429


def test_create_flag_rate_limit(client):
    for i in range(31):
        response = client.post(
            "/feature_flag/",
            json={"key": f"flag_{i}", "enabled": True},
        )
    assert response.status_code == 429


def test_read_flag_rate_limit(client, test_flag):
    for i in range(61):
        response = client.get(f"/feature_flag/{test_flag['key']}")
    assert response.status_code == 429


def test_health_rate_limit(client):
    for i in range(61):
        response = client.get("/health")
    assert response.status_code == 429


def test_create_user_rate_limit(client):
    for i in range(6):
        response = client.post(
            "/user/",
            json={"email": f"user_{i}@example.com", "password": "Secret123!"},
        )
    assert response.status_code == 429


def test_read_all_users_rate_limit(client):
    for _ in range(61):
        response = client.get("/user/all")
    assert response.status_code == 429


def test_read_user_rate_limit(client, test_user):
    for _ in range(61):
        response = client.get(f"/user/{test_user['id']}")
    assert response.status_code == 429


def test_delete_user_rate_limit(client, auth_token):
    response = client.post(
        "/user/",
        json={"email": "delete_me@example.com", "password": "Secret123!"},
    )
    user_id = response.json()["id"]

    for _ in range(31):
        response = client.delete(
            f"/user/{user_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )
    assert response.status_code == 429


def test_update_user_rate_limit(client, test_user, auth_token):
    for i in range(31):
        response = client.patch(
            f"/user/update/{test_user['id']}",
            json={"email": f"updated_{i}@example.com"},
            headers={"Authorization": f"Bearer {auth_token}"},
        )
    assert response.status_code == 429
