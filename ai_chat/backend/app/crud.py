
import random
import os
import shutil
from sqlalchemy.orm import Session
from . import models, schemas

def get_chat(db: Session, chat_id: int):
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()

def get_chats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Chat).order_by(models.Chat.created_at.desc()).offset(skip).limit(limit).all()

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
        # 在删除数据库记录前，先删除关联的物理文件和目录
        upload_dir = f"uploads/chat_{chat_id}"
        if os.path.isdir(upload_dir):
            shutil.rmtree(upload_dir)

        db.delete(db_chat)
        db.commit()
    return db_chat

def get_messages(db: Session, chat_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Message).filter(models.Message.chat_id == chat_id).offset(skip).limit(limit).all()

def create_chat_message(db: Session, message: schemas.MessageCreate, chat_id: int, locale: str = "en"):
    # 1. 保存用户的消息
    db_message = models.Message(**message.model_dump(), chat_id=chat_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    # 2. 根据 locale 生成并保存一条模拟的AI回复
    ai_responses = {
        "en": [
            "I need to think about this.",
            "That's an interesting question, let me think.",
            "I'm analyzing your question, please wait.",
            "That's a great question!"
        ],
        "zh-CN": [
            "这个问题我需要考虑一下。",
            "这个问题很有意思，让我想想。",
            "我正在分析您的问题，请稍候。",
            "这是一个很好的问题！"
        ],
        "zh-TW": [
            "這個問題我需要考慮一下。",
            "這個問題很有意思，讓我想想。",
            "我正在分析您的問題，請稍候。",
            "這是一個很好的問題！"
        ]
    }
    
    response_list = ai_responses.get(locale, ai_responses["en"])
    ai_content = random.choice(response_list)
    db_ai_message = models.Message(content=ai_content, sender="ai", chat_id=chat_id)
    db.add(db_ai_message)
    db.commit()
    db.refresh(db_ai_message)

    return [db_message, db_ai_message]

def create_uploaded_file(db: Session, file: schemas.UploadedFileCreate, chat_id: int):
    db_file = models.UploadedFile(filename=file.filename, filepath=file.filepath, chat_id=chat_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_uploaded_file(db: Session, file_id: int):
    return db.query(models.UploadedFile).filter(models.UploadedFile.id == file_id).first()

def delete_uploaded_file(db: Session, db_file: models.UploadedFile):
    """
    Deletes a file from the filesystem and the database.
    Assumes ownership has already been verified.
    """
    if os.path.exists(db_file.filepath):
        os.remove(db_file.filepath)
    db.delete(db_file)
    db.commit()
