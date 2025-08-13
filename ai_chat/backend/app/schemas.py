
from pydantic import BaseModel
from typing import List, Optional
import datetime

class MessageBase(BaseModel):
    content: str
    sender: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    chat_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class UploadedFileBase(BaseModel):
    filename: str
    filepath: str

class UploadedFileCreate(UploadedFileBase):
    pass

class UploadedFile(UploadedFileBase):
    id: int
    chat_id: int
    created_at: datetime.datetime

    class Config:
        orm_mode = True

class ChatBase(BaseModel):
    name: str

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    created_at: datetime.datetime
    messages: List[Message] = []
    files: List[UploadedFile] = []

    class Config:
        orm_mode = True
