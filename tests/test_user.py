import pytest

from fastapi.testclient import TestClient


@pytest.fixture
def test_user(client):
    response = client.post(
        "/user/",
        json={"email": "testuser@example.com", "password": "secret123"},
    )
    return response.json()


# ============================================================================
# CREATE USER TESTS
# ============================================================================


def test_create_user_success(client):
    user_data = {"email": "alice@example.com", "password": "secret123"}
    response = client.post("/user/", json=user_data)

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["email"] == "alice@example.com"
    assert data["is_active"] is True
    assert "hashed_password" not in data


def test_create_user_fail_duplicate_email(client, test_user):
    response = client.post(
        "/user/",
        json={"email": test_user["email"], "password": "secret123"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_create_user_fail_invalid_email(client):
    response = client.post(
        "/user/",
        json={"email": "not-an-email", "password": "secret123"},
    )

    assert response.status_code in [400, 422]


def test_create_user_fail_missing_password(client):
    response = client.post(
        "/user/",
        json={"email": "nopassword@example.com"},
    )

    assert response.status_code == 422


def test_create_user_fail_missing_email(client):
    response = client.post(
        "/user/",
        json={"password": "secret123"},
    )

    assert response.status_code == 422


def test_create_user_fail_empty_email(client):
    response = client.post(
        "/user/",
        json={"email": "", "password": "secret123"},
    )

    assert response.status_code == 422


def test_create_user_fail_empty_password(client):
    response = client.post(
        "/user/",
        json={"email": "user@example.com", "password": ""},
    )

    assert response.status_code == 422


# ============================================================================
# READ USER TESTS
# ============================================================================


def test_read_user_success(client, test_user):
    user_id = test_user["id"]

    response = client.get(f"/user/{user_id}")
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == test_user["email"]
    assert data["id"] == user_id


def test_read_user_fail_not_found(client):
    response = client.get("/user/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User does not exist"


def test_read_user_fail_invalid_id(client):
    response = client.get("/user/invalid")

    assert response.status_code == 422


def test_read_user_fail_negative_id(client):
    response = client.get("/user/-1")

    assert response.status_code == 404


# ============================================================================
# READ ALL USERS TESTS
# ============================================================================


def test_read_all_users_success(client):
    client.post("/user/", json={"email": "user1@example.com", "password": "pass1"})
    client.post("/user/", json={"email": "user2@example.com", "password": "pass2"})
    client.post("/user/", json={"email": "user3@example.com", "password": "pass3"})

    response = client.get("/user/all")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 3
    assert any(user["email"] == "user1@example.com" for user in data)
    assert any(user["email"] == "user2@example.com" for user in data)
    assert any(user["email"] == "user3@example.com" for user in data)


def test_read_all_users_sucess_single(client, test_user):
    response = client.get("/user/all")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["id"] == test_user["id"]


def test_read_all_users_sucess_empty(client):
    response = client.get("/user/all")
    data = response.json()

    assert response.status_code == 200
    assert data == []


# ============================================================================
# UPDATE USER TESTS
# ============================================================================


def test_update_user_email_success(client, test_user):
    user_id = test_user["id"]

    response = client.patch(
        f"/user/update/{user_id}",
        json={"email": "newemail@example.com"},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "newemail@example.com"
    assert data["id"] == user_id


def test_update_user_fail_email_already_exist(client, test_user):
    client.post("/user/", json={"email": "existing@example.com", "password": "pass"})

    response = client.patch(
        f"/user/update/{test_user['id']}",
        json={"email": "existing@example.com"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_update_user_fail_email_case_insensitive(client, test_user):
    client.post("/user/", json={"email": "case@example.com", "password": "pass"})

    response = client.patch(
        f"/user/update/{test_user['id']}",
        json={"email": "CASE@example.com"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_update_user_fail_same_email(client, test_user):
    response = client.patch(
        f"/user/update/{test_user['id']}",
        json={"email": test_user["email"]},
    )

    assert response.status_code == 200


def test_update_user_fail_not_found(client):
    response = client.patch(
        "/user/update/9999",
        json={"email": "notfound@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "User does not exist"


def test_update_user_fail_empty_payload(client, test_user):
    response = client.patch(
        f"/user/update/{test_user['id']}",
        json={},
    )

    assert response.status_code == 200
    assert response.json()["email"] == test_user["email"]


def test_update_user_fail_invalid_email(client, test_user):
    response = client.patch(
        f"/user/update/{test_user['id']}",
        json={"email": "not-valid-email"},
    )

    assert response.status_code in [400, 422]


# ============================================================================
# DELETE USER TESTS
# ============================================================================


def test_delete_user_success(client, test_user):
    user_id = test_user["id"]

    response = client.delete(f"/user/{user_id}")

    assert response.status_code == 204
    assert response.content == b""

    get_response = client.get(f"/user/{user_id}")
    assert get_response.status_code == 404


def test_delete_user_fail_not_found(client):
    response = client.delete("/user/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User does not exist"


def test_delete_user_fail_twice(client: TestClient, test_user):
    user_id = test_user["id"]

    response1 = client.delete(f"/user/{user_id}")
    assert response1.status_code == 204

    response2 = client.delete(f"/user/{user_id}")
    assert response2.status_code == 404


def test_delete_user_fail_invalid_id(client: TestClient):
    response = client.delete("/user/invalid")

    assert response.status_code == 422
