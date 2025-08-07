from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatRecordBase(BaseModel):
    content: str

class ChatRecordCreate(ChatRecordBase):
    pass

class ChatRecord(ChatRecordBase):
    id: int
    chat_id: int
    timestamp: datetime

    class Config:
        orm_mode = True

class ChatBase(BaseModel):
    name: str

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    created_at: datetime
    records: List[ChatRecord] = []

    class Config:
        orm_mode = True
