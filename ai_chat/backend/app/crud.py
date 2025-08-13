
from sqlalchemy.orm import Session
from . import models, schemas

def get_chat(db: Session, chat_id: int):
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()

def get_chats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chat).offset(skip).limit(limit).all()

def create_chat(db: Session, chat: schemas.ChatCreate):
    db_chat = models.Chat(name=chat.name)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def update_chat_name(db: Session, chat_id: int, name: str):
    db_chat = get_chat(db, chat_id)
    if db_chat:
        db_chat.name = name
        db.commit()
        db.refresh(db_chat)
    return db_chat

def delete_chat(db: Session, chat_id: int):
    db_chat = get_chat(db, chat_id)
    if db_chat:
        db.delete(db_chat)
        db.commit()
    return db_chat

def get_messages(db: Session, chat_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).offset(skip).limit(limit).all()

def create_chat_message(db: Session, message: schemas.MessageCreate, chat_id: int):
    db_message = models.Message(**message.model_dump(), chat_id=chat_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def create_uploaded_file(db: Session, file: schemas.UploadedFileCreate, chat_id: int):
    db_file = models.UploadedFile(filename=file.filename, filepath=file.filepath, chat_id=chat_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file
