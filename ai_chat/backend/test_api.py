import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI-Chat API!"}

def test_create_chat():
    response = client.post("/api/chats/", json={"name": "Test Chat"})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Test Chat"

def test_get_chats():
    response = client.get("/api/chats/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_upload_file():
    chat_response = client.post("/api/chats/", json={"name": "File Upload Chat"})
    chat_id = chat_response.json()["id"]
    file_content = b"Hello, this is a test file."
    response = client.post(
        f"/api/upload/",
        files={"file": ("test.txt", file_content)},
        data={"chat_id": chat_id}
    )
    assert response.status_code == 200
    assert "file 'test.txt' saved" in response.json()["info"]
