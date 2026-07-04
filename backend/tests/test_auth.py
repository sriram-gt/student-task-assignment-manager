from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345@localhost:5432/stam_test")

engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_register():
    response = client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    })
    assert response.status_code in [200, 400]

def test_login_invalid():
    response = client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401

def test_login_valid():
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "logintest@example.com",
        "password": "testpass123"
    })
    response = client.post("/auth/login", json={
        "email": "logintest@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()