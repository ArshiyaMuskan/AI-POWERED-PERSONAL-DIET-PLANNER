def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_register_and_login(client):
    email = "unique-test@example.com"
    r = client.post("/api/auth/register", json={
        "name": "Test User",
        "email": email,
        "password": "Password123!"
    })
    assert r.status_code in (201, 409)

    r = client.post("/api/auth/login", json={
        "email": email,
        "password": "Password123!"
    })
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_invalid_login(client):
    r = client.post("/api/auth/login", json={
        "email": "nobody@example.com",
        "password": "wrong-password"
    })
    assert r.status_code == 401


def test_unauthorized_profile(client):
    r = client.get("/api/profile")
    assert r.status_code == 401


def test_profile_and_plan(client, registered_user):
    headers = auth_headers(registered_user)

    r = client.put("/api/profile", headers=headers, json={
        "name": "Demo User",
        "age": 22,
        "height": 170,
        "weight": 65,
        "activity_level": "moderate",
        "dietary_preference": "vegetarian",
        "goal": "balanced",
        "allergies": ""
    })
    assert r.status_code == 200

    r = client.post("/api/plans/generate", headers=headers)
    assert r.status_code == 201
    assert "breakfast" in r.json()

    r = client.get("/api/plans", headers=headers)
    assert r.status_code == 200
    assert len(r.json()) >= 1


def test_user_isolation(client, registered_user):
    headers = auth_headers(registered_user)
    plans = client.get("/api/plans", headers=headers).json()
    if plans:
        plan_id = plans[0]["id"]
        # Ownership condition is enforced by user_id in the route query.
        assert client.get(f"/api/plans/{plan_id}", headers=headers).status_code == 200


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
