from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ConversationCreate(BaseModel):
    title: str = "新对话"

class ConversationUpdate(BaseModel):
    title: str

class Conversation(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str

class MessageCreate(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class Message(BaseModel):
    id: int
    role: str
    content: str
    created_at: str

class ConversationWithMessages(BaseModel):
    id: int
    title: str
    created_at: str
    updated_at: str
    messages: List[Message]

class FileUploadResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    message: str