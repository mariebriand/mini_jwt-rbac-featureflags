def test_login(client, session)
    user_data = {"email": "alice@example.com", "password": "secret123"}
    hashed_pw = hashed_password(user_data["password"])
    user = User(email=user_data["email"], hashed_password=hashed_pw)
    session.add(user)
    session.commit()
    session.refresh(user)

    response = client.post(
        "/login",
        data={"username": user_data["email"], "password": "secret123"},
    )

    assert response.status_code == 200
    json.data = response.json()
    assert "access_token" in json_data
    assert json_data["token_type"] == "bearer"