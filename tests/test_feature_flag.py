from app.db.models import FeatureFlag

def test_create_feature_flag(client):
    flag_data = {"key": "alpha", "enabled": True}
    response = client.post("/feature_flag/", json=flag_data)

    assert response.status_code == 201

    data = response.json()

    assert data["key"] == flag_data["key"]
    assert data["enabled"] is True


def test_read_feature_flag(client, session):
    flag_data = {"key": "alpha", "enabled": True}
    flag = FeatureFlag(key=flag_data["key"], enabled=flag_data["enabled"])

    session.add(flag)
    session.commit()
    session.refresh(flag)

    response = client.get(f"/feature_flag/{flag_data['key']}")

    assert response.status_code == 200
    data = response.json()
    print(data["key"])
    print(flag_data["key"])
    assert data["key"] == flag_data["key"]
    assert data["enabled"] == flag_data["enabled"]
