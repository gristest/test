from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.api.v1.endpoints.chats import get_db
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_chat():
    response = client.post("/api/v1/chats/", json={"name": "Test Chat"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Chat"
    assert "id" in data


def test_read_chats():
    response = client.get("/api/v1/chats/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)


def test_create_message():
    # First create a chat to add a message to
    response = client.post("/api/v1/chats/", json={"name": "Chat for Message Test"})
    assert response.status_code == 200
    chat_id = response.json()["id"]

    # Now create a message in that chat
    response = client.post(
        f"/api/v1/chats/{chat_id}/messages/",
        json={"content": "Hello", "sender": "user"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["content"] == "Hello"
    assert data["sender"] == "user"
    assert data["chat_id"] == chat_id
