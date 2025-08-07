from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.chat import Chat as DBChat, ChatRecord as DBChatRecord
from models.schemas import Chat, ChatCreate, ChatRecord, ChatRecordCreate
from services.database import get_db
from typing import List
from fastapi import UploadFile

router = APIRouter()

@router.post('/chats/', response_model=Chat)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    new_chat = DBChat(name=chat.name)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

@router.get('/chats/', response_model=List[Chat])
def get_chats(db: Session = Depends(get_db)):
    return db.query(Chat).all()

@router.get('/chats/{chat_id}/', response_model=Chat)
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail='Chat not found')
    return chat

@router.post('/chats/{chat_id}/records/', response_model=ChatRecord)
def add_chat_record(chat_id: int, record: ChatRecordCreate, db: Session = Depends(get_db)):
    chat = db.query(DBChat).filter(DBChat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail='Chat not found')
    new_record = DBChatRecord(chat_id=chat_id, content=record.content)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.post('/upload/')
def upload_file(chat_id: int, file: UploadFile, db: Session = Depends(get_db)):
    chat = db.query(Chat).filter(Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail='Chat not found')
    file_location = f"uploads/chat_{chat_id}/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

    db.refresh(new_record)
    return new_record
