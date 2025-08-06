from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import sqlite3
import os

app = FastAPI()

# Database setup
DB_PATH = 'conversations.db'

# Ensure the database and table exist
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    content TEXT
)
''')
conn.commit()
conn.close()

@app.get("/conversations")
async def get_conversations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM conversations")
    conversations = cursor.fetchall()
    conn.close()
    return JSONResponse(content={"conversations": conversations})

@app.post("/conversations")
async def create_conversation(name: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (name, content) VALUES (?, '')", (name,))
    conn.commit()
    conn.close()
    return JSONResponse(content={"message": "Conversation created"})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return JSONResponse(content={"info": f"file '{file.filename}' saved at '{file_location}'"})

