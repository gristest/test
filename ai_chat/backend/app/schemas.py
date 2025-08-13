
from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)

class UploadedFileBase(BaseModel):
    filename: str
    filepath: str

class UploadedFileCreate(UploadedFileBase):
    pass

class UploadedFile(UploadedFileBase):
    id: int
    chat_id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class ChatBase(BaseModel):
    name: str

class ChatCreate(BaseModel):
    name: Optional[str] = None

class ChatUpdate(BaseModel):
    name: str

class Chat(ChatBase):
    id: int
    created_at: datetime.datetime
    messages: List[Message] = []
    files: List[UploadedFile] = []

    model_config = ConfigDict(from_attributes=True)
