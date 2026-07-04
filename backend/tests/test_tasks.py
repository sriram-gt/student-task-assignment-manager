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

def get_token():
    client.post("/auth/register", json={
        "name": "Task Tester",
        "email": "tasktest@example.com",
        "password": "testpass123"
    })
    res = client.post("/auth/login", json={
        "email": "tasktest@example.com",
        "password": "testpass123"
    })
    return res.json()["access_token"]

def test_create_task():
    token = get_token()
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "Test description",
        "priority": "high"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_get_tasks():
    token = get_token()
    response = client.get("/tasks", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_tasks_unauthorized():
    response = client.get("/tasks")
    assert response.status_code == 401