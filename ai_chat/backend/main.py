from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import uuid
from typing import List
from database import Database
from models import (
    ConversationCreate, ConversationUpdate, Conversation, 
    MessageCreate, Message, ConversationWithMessages, FileUploadResponse
)

app = FastAPI(title="AI Chat API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:12000",
        "http://127.0.0.1:12000",
        "https://work-1-zrjouldkqnbapmiu.prod-runtime.all-hands.dev",
        "https://work-2-zrjouldkqnbapmiu.prod-runtime.all-hands.dev",
        "*"  # 允许所有来源（开发环境）
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
db = Database()

# 创建上传目录
UPLOAD_DIR = "../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 静态文件服务
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

@app.get("/")
async def root():
    return {"message": "AI Chat API is running"}

@app.get("/api/conversations", response_model=List[Conversation])
async def get_conversations():
    """获取所有对话列表"""
    try:
        conversations = db.get_conversations()
        return conversations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/conversations", response_model=Conversation)
async def create_conversation(conversation: ConversationCreate):
    """创建新对话"""
    try:
        conversation_id = db.create_conversation(conversation.title)
        new_conversation = db.get_conversation(conversation_id)
        if new_conversation:
            return new_conversation
        else:
            raise HTTPException(status_code=500, detail="Failed to create conversation")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{conversation_id}", response_model=ConversationWithMessages)
async def get_conversation(conversation_id: int):
    """获取特定对话及其消息"""
    try:
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.get_messages(conversation_id)
        
        return ConversationWithMessages(
            **conversation,
            messages=messages
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(conversation_id: int, conversation_update: ConversationUpdate):
    """更新对话标题"""
    try:
        success = db.update_conversation_title(conversation_id, conversation_update.title)
        if not success:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        updated_conversation = db.get_conversation(conversation_id)
        return updated_conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_messages(conversation_id: int):
    """获取对话的所有消息"""
    try:
        # 检查对话是否存在
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # 获取消息
        messages = db.get_messages(conversation_id)
        return messages
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/conversations/{conversation_id}/messages", response_model=Message)
async def add_message(conversation_id: int, message: MessageCreate):
    """向对话添加消息"""
    try:
        # 检查对话是否存在
        conversation = db.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # 添加消息
        message_id = db.add_message(conversation_id, message.role, message.content)
        
        # 获取添加的消息
        messages = db.get_messages(conversation_id)
        new_message = next((msg for msg in messages if msg["id"] == message_id), None)
        
        if new_message:
            return new_message
        else:
            raise HTTPException(status_code=500, detail="Failed to add message")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """上传文件"""
    try:
        # 检查文件大小（10MB限制）
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        
        # 读取文件内容以检查大小
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File size exceeds 10MB limit")
        
        # 生成唯一文件名
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # 保存文件
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # 保存文件信息到数据库
        file_id = db.save_file(
            filename=unique_filename,
            original_filename=file.filename or "unknown",
            file_path=file_path,
            file_size=file_size
        )
        
        return FileUploadResponse(
            id=file_id,
            filename=unique_filename,
            original_filename=file.filename or "unknown",
            file_size=file_size,
            message="File uploaded successfully"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)