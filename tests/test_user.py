def test_create_user(client):
    pass
    user_data = {"email": "alice@example.com", "password": "secret123"}
    response = client.post("/user/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert data["is_active"] is True
    assert "hashed_password" not in data