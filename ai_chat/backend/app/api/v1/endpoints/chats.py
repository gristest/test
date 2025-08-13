
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from .... import crud, models, schemas
from ....database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Chat)
def create_chat(chat: schemas.ChatCreate, db: Session = Depends(get_db)):
    return crud.create_chat(db=db, chat=chat)

@router.get("/", response_model=List[schemas.Chat])
def read_chats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    chats = crud.get_chats(db, skip=skip, limit=limit)
    return chats

@router.get("/{chat_id}", response_model=schemas.Chat)
def read_chat(chat_id: int, db: Session = Depends(get_db)):
    db_chat = crud.get_chat(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat

@router.put("/{chat_id}", response_model=schemas.Chat)
def update_chat_name(chat_id: int, name: str, db: Session = Depends(get_db)):
    db_chat = crud.update_chat_name(db, chat_id=chat_id, name=name)
    if db_chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat

@router.delete("/{chat_id}", response_model=schemas.Chat)
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    db_chat = crud.delete_chat(db, chat_id=chat_id)
    if db_chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")
    return db_chat

@router.post("/{chat_id}/messages/", response_model=schemas.Message)
def create_message_for_chat(chat_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_chat_message(db=db, message=message, chat_id=chat_id)

@router.get("/{chat_id}/messages/", response_model=List[schemas.Message])
def read_messages(chat_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    messages = crud.get_messages(db, chat_id=chat_id, skip=skip, limit=limit)
    return messages

@router.post("/{chat_id}/files/", response_model=schemas.UploadedFile)
def upload_file(chat_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    upload_dir = f"uploads/chat_{chat_id}"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    db_file = schemas.UploadedFileCreate(filename=file.filename, filepath=file_path)
    return crud.create_uploaded_file(db=db, file=db_file, chat_id=chat_id)
