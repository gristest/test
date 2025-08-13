
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default=f"New Chat {datetime.datetime.now()}")
    created_at = Column(DateTime, default=datetime.datetime.now)

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    files = relationship("UploadedFile", back_populates="chat", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    content = Column(String)
    sender = Column(String) # "user" or "ai"
    created_at = Column(DateTime, default=datetime.datetime.now)

    chat = relationship("Chat", back_populates="messages")

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    filename = Column(String)
    filepath = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.now)

    chat = relationship("Chat", back_populates="files")
