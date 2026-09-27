import os
os.environ["DATABASE_URL"] = "sqlite:///./test_diet_planner.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-tests"
os.environ["STORAGE_BACKEND"] = "local"
os.environ["LOCAL_STORAGE_DIR"] = "./test_storage"

import pytest
from fastapi.testclient import TestClient
from app.database import Base, engine
from app.main import app

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def registered_user(client):
    response = client.post("/api/auth/register", json={
        "name": "Demo User",
        "email": "demo@example.com",
        "password": "Password123!"
    })
    if response.status_code == 409:
        response = client.post("/api/auth/login", json={
            "email": "demo@example.com",
            "password": "Password123!"
        })
    return response.json()["access_token"]
