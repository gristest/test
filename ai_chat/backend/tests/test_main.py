from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.api.v1.endpoints.chats import get_db
import os
import io
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: ensure the database is clean before each test function
    Base.metadata.create_all(bind=engine)
    # Create uploads dir if not exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    yield
    # Teardown: clean up the database
    Base.metadata.drop_all(bind=engine)


def test_create_chat():
    response = client.post("/api/v1/chats/", json={"name": "Test Chat"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Chat"
    assert "id" in data

def test_create_chat_no_name():
    response = client.post("/api/v1/chats/", json={})
    assert response.status_code == 200, response.text
    data = response.json()
    assert "New Chat" in data["name"]
    assert "id" in data


def test_read_chats():
    client.post("/api/v1/chats/", json={"name": "Test Chat 1"})
    client.post("/api/v1/chats/", json={"name": "Test Chat 2"})
    response = client.get("/api/v1/chats/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_read_chat():
    res = client.post("/api/v1/chats/", json={"name": "Test Chat"})
    chat_id = res.json()["id"]
    response = client.get(f"/api/v1/chats/{chat_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Chat"
    assert data["id"] == chat_id

def test_read_chat_not_found():
    response = client.get("/api/v1/chats/999")
    assert response.status_code == 404

def test_update_chat_name():
    res = client.post("/api/v1/chats/", json={"name": "Old Name"})
    chat_id = res.json()["id"]
    response = client.put(f"/api/v1/chats/{chat_id}", json={"name": "New Name"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "New Name"
    assert data["id"] == chat_id

def test_delete_chat():
    res = client.post("/api/v1/chats/", json={"name": "To Be Deleted"})
    chat_id = res.json()["id"]
    response = client.delete(f"/api/v1/chats/{chat_id}")
    assert response.status_code == 200, response.text
    # Verify it's gone
    get_response = client.get(f"/api/v1/chats/{chat_id}")
    assert get_response.status_code == 404


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
    messages = response.json()

    # 端点现在返回一个包含两条消息的列表：用户的和AI的
    assert isinstance(messages, list)
    assert len(messages) == 2

    # 验证用户消息
    user_message = messages[0]
    assert user_message["content"] == "Hello"
    assert user_message["sender"] == "user"
    assert user_message["chat_id"] == chat_id

    # 验证AI消息
    ai_message = messages[1]
    assert isinstance(ai_message["content"], str)
    assert len(ai_message["content"]) > 0
    assert ai_message["sender"] == "ai"
    assert ai_message["chat_id"] == chat_id

def test_read_messages():
    res = client.post("/api/v1/chats/", json={"name": "Chat for Messages"})
    chat_id = res.json()["id"]
    client.post(f"/api/v1/chats/{chat_id}/messages/", json={"content": "Msg 1", "sender": "user"})
    client.post(f"/api/v1/chats/{chat_id}/messages/", json={"content": "Msg 2", "sender": "ai"})

    response = client.get(f"/api/v1/chats/{chat_id}/messages/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["content"] == "Msg 1"

def test_upload_file():
    res = client.post("/api/v1/chats/", json={"name": "Chat for File Upload"})
    chat_id = res.json()["id"]

    file_content = b"this is a test file"
    file_obj = ("test.txt", io.BytesIO(file_content), "text/plain")

    response = client.post(f"/api/v1/chats/{chat_id}/files/", files={"file": file_obj})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["chat_id"] == chat_id
    assert os.path.exists(data["filepath"])
    os.remove(data["filepath"]) # Clean up the created file
